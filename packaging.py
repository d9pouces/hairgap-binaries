#!/usr/bin/env python3
# ##############################################################################
#  This file is part of Hairgap                                                #
#                                                                              #
#  Copyright (C) 2020 Matthieu Gallet <github@19pouces.net>                    #
#  All Rights Reserved                                                         #
#                                                                              #
#  You may use, distribute and modify this code under the                      #
#  terms of the (BSD-like) CeCILL-B license.                                   #
#                                                                              #
#  You should have received a copy of the CeCILL-B license with                #
#  this file. If not, please visit:                                            #
#  https://cecill.info/licences/Licence_CeCILL-B_V1-en.txt (English)           #
#  or https://cecill.info/licences/Licence_CeCILL-B_V1-fr.txt (French)         #
#                                                                              #
# ##############################################################################
"""Generate official distributions (source and compiled ones, as well as Docker images).

Operations:
- create a temp directory
- copy `COPIED_FILES` to this directory
- from all Django apps beginning by `interdiode`, copy the content of `templates` and `static` folders
- compile interdiode via Nuitka

Script called by `tox -e packaging`.

# !!! this script must be executed from the main source directory
"""
import argparse
import glob
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from distutils import util
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger("hairgap")

COPIED_FILES = [
    "LICENSE",
    "MANIFEST.in",
    "README.md",
    "setup.cfg",
    "setup.py",
    "hairgap_binaries",
]

DOCKER_FILE_ALPINE = """FROM {docker_image}
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /source
ADD ./{package_file} /source/
# git-lfs gnupg npm: required by Interdiode
# postgresql-dev gcc python3-dev musl-dev: required by postgresql-dev gcc python3-dev musl-dev
# libressl-dev musl-dev libffi-dev rust cargo: required by cryptography
# libxml2-dev libxslt-dev: required by lxml
RUN apk - no-cache update \
    && apk add --no-cache git-lfs gnupg npm openssh-keygen openssh-client \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev \
    && apk add --no-cache libressl-dev musl-dev libffi-dev rust cargo \
    && apk add --no-cache libxml2-dev libxslt-dev \
    && python3 -m pip --no-cache-dir install /source/*.whl \
    && rm -rf /source/* \
    && apk del gcc python3-dev musl-dev \
    && apk del rust cargo \
    && rm -rf /etc/apk/cache
RUN adduser --home /home/interdiode --disabled-password --gecos "" --shell /bin/sh interdiode
ADD ./local_settings.py /home/interdiode/local_settings.py
WORKDIR /home/interdiode
USER interdiode
RUN npm install puppeteer
"""
LOCAL_SETTINGS_ALPINE = """
HEADLESS_CHROME_PATH="/usr/bin/google-chrome"
NODE_MODULES_PATH="/home/interdiode/node_modules"
"""

# mv "hairgapr" "/vagrant/hairgap_binaries/manylinux2014_x86_64-hairgapr"
# mv "hairgaps" "/vagrant/hairgap_binaries/manylinux2014_x86_64-hairgaps"


def install_dependencies():
    subprocess.check_call(
        ["apk", "add", "--no-cache", "git", "gcc", "curl", "make", "clang"]
    )
    try:
        # noinspection PyPackageRequirements
        import wheel
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--user", "wheel"]
        )


def copy_files(src_directory: Path, temp_directory: Path):
    for name in COPIED_FILES:
        src_path = src_directory / name
        dst_path = temp_directory / name
        if os.path.isdir(src_path):
            shutil.copytree(
                src_path,
                dst_path,
                ignore=lambda __, x: [y for y in x if y == "__pycache__"],
            )
        else:
            shutil.copy2(src_path, dst_path)


def compile_module(src_directory: Path, temp_directory: Path):
    # noinspection PyUnusedLocal
    src_directory = src_directory
    cmd = [
        "git",
        "clone",
        "--recursive",
        "https://github.com/cea-sec/hairgap.git",
        "/tmp/hairgap",
    ]
    subprocess.check_call(cmd, cwd=temp_directory)
    os.makedirs("/tmp/hairgap/include/wirehair", exist_ok=True)
    for name in ("include/wirehair/wirehair.h", "gf256.h", "wirehair.cpp", "gf256.cpp"):
        cmd = [
            "curl",
            "-so",
            "/tmp/hairgap/%s" % name,
            "https://raw.githubusercontent.com/catid/wirehair/master/%s" % name,
        ]
        subprocess.check_call(cmd, cwd=temp_directory)
    subprocess.check_call(["make"], cwd="/tmp/hairgap/wirehair")
    subprocess.check_call(["make"], cwd="/tmp/hairgap")


def create_package(src_directory: Path, temp_directory: Path) -> Optional[Path]:
    version = (sys.version_info[0], sys.version_info[1])
    cmd = [
        sys.executable,
        "setup.py",
        "bdist_wheel",
        "--python-tag=py%d%d" % version,
        "--plat-name=%s" % util.get_platform(),
        "--py-limited-api=cp%d%d" % version,
        "--dist-dir=%s" % (src_directory / "dist").absolute(),
    ]
    return execute_command(cmd, src_directory, temp_directory)


def run_in_docker(
    src_directory: Path,
    temp_directory: Path,
    base_image: str = "python:3.9-slim-buster",
) -> Optional[Path]:
    cmd = [
        "docker",
        "run",
        "--rm",
        "--mount",
        "type=bind,source=%s,target=/source" % src_directory.absolute(),
        base_image,
        "python3",
        "/source/tools/packaging.py",
    ]
    return execute_command(cmd, src_directory, temp_directory)


def execute_command(cmd: List[str], src_directory: Path, temp_directory: Path):
    name_to_mtime = {}
    if (src_directory / "dist").exists():
        for name in os.listdir(src_directory / "dist"):
            name_to_mtime[name] = os.stat(src_directory / "dist" / name).st_mtime
    subprocess.check_call(cmd, cwd=temp_directory)
    new_names = {
        name
        for name in os.listdir(src_directory / "dist")
        if os.stat(src_directory / "dist" / name).st_mtime > name_to_mtime.get(name, 0)
    }
    if len(new_names) == 1:
        return src_directory / "dist" / new_names.pop()
    return None


def build_docker_image(
    package_path: Path,
    docker_image: str = "python:3.9-slim-buster",
    tags: Optional[List[str]] = None,
):
    """Build an Interdiode Docker image.

    Allow to use alpine as base image, but hairgap is not working and build is slow.
    Maybe https://www.python.org/dev/peps/pep-0656/ could be useful.

    :param package_path: absolute path to the interdiode.whl
    :param docker_image: Docker base image
    :param tags: tags to add to the built image
    """
    if re.match(r"^python:(3.\d(\.\d+)?|rc|latest)-alpine$", docker_image):
        docker_file_content = DOCKER_FILE_ALPINE
        local_settings_content = LOCAL_SETTINGS_ALPINE
    elif re.match(
        r"^python:(3.\d(\.\d+)?|rc|latest)(-(buster|slim-buster|slim))?$", docker_image
    ):
        docker_file_content = DOCKER_FILE_DEBIAN
        local_settings_content = LOCAL_SETTINGS_DEBIAN
    else:
        logger.error("unknown Docker base image: %s" % docker_image)
        return

    with tempfile.TemporaryDirectory() as temp_directory:
        temp_path = Path(temp_directory)
        basename = package_path.name
        shutil.copy2(package_path, temp_path / basename)
        content = docker_file_content.format(
            package_file=basename, docker_image=docker_image
        )
        with open(temp_path / "Dockerfile", "w") as fd:
            fd.write(content)
        with open(temp_path / "local_settings.py", "w") as fd:
            fd.write(local_settings_content)
        cmd = ["docker", "build", "."]
        if tags:
            for tag in tags:
                cmd += ["-t", tag]
        subprocess.check_call(cmd, cwd=temp_path)
    for tag in tags:
        cmd = [
            "docker",
            "run",
            "--rm",
            tag,
            "interdiode-ctl",
            "configuration",
            "check",
        ]
        subprocess.check_call(cmd)


def main():
    src_directory = Path(__file__).parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--in-docker-image",
        help="Name of a Docker image to run this script into (must look like 'python:3.x-alpine')",
        default=None,
    )
    parser.add_argument(
        "--build-docker-image",
        help="Use the built package to build a Docker image",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()
    if args.in_docker_image:
        package_path = run_in_docker(src_directory, src_directory, args.in_docker_image)
        if args.build_docker_image:
            if package_path:
                from hairgap_binaries import __version__ as version

                build_docker_image(
                    package_path,
                    args.in_docker_image,
                    tags=[
                        "interdiode/interdiode:%s" % version,
                        "interdiode/interdiode:latest",
                    ],
                )
            else:
                logger.warning("no new package")
    else:
        install_dependencies()
        with tempfile.TemporaryDirectory() as temp_directory:
            temp_directory = Path(temp_directory)

            copy_files(src_directory, temp_directory)
            compile_module(src_directory, temp_directory)
            create_package(src_directory, temp_directory)


if __name__ == "__main__":
    main()
