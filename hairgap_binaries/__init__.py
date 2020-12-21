__version__ = "1.0.0"
__author__ = "Matthieu Gallet"
__all__ = ["get_hairgapr", "get_hairgaps"]

from typing import Optional

import pkg_resources

known_platforms = {
    "linux-x86_64": "manylinux2014_x86_64",
}


def get_hairgapr() -> Optional[str]:
    """return the path of the hairgapr binary"""
    prefix = known_platforms.get(pkg_resources.get_platform())
    return prefix and pkg_resources.resource_filename(
        "hairgap_binaries", "%s-hairgapr" % prefix
    )


def get_hairgaps() -> Optional[str]:
    """return the path of the hairgaps binary"""
    prefix = known_platforms.get(pkg_resources.get_platform())
    return prefix and pkg_resources.resource_filename(
        "hairgap_binaries", "%s-hairgaps" % prefix
    )
