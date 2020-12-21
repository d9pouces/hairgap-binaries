import os
from unittest import TestCase, mock

import pkg_resources

from hairgap_binaries import get_hairgapr, get_hairgaps


class TestOnLinux(TestCase):
    # noinspection PyUnusedLocal
    @mock.patch("pkg_resources.get_platform", side_effect=lambda: "linux-x86_64")
    def test_on_linux_hairgapr(self, mock_):
        target = pkg_resources.resource_filename(
            "hairgap_binaries", "manylinux2014_x86_64-hairgapr"
        )
        self.assertEqual(
            target, get_hairgapr(),
        )
        self.assertTrue(os.path.isfile(target))

    # noinspection PyUnusedLocal
    @mock.patch("pkg_resources.get_platform", side_effect=lambda: "linux-x86_64")
    def test_on_linux_hairgaps(self, mock_):
        target = pkg_resources.resource_filename(
            "hairgap_binaries", "manylinux2014_x86_64-hairgaps"
        )
        self.assertEqual(
            target, get_hairgaps(),
        )
        self.assertTrue(os.path.isfile(target))


class TestOnMacosX(TestCase):
    # noinspection PyUnusedLocal
    @mock.patch(
        "pkg_resources.get_platform", side_effect=lambda: "macosx-10.14.6-x86_64"
    )
    def test_on_macos_hairgapr(self, mock_):
        self.assertIsNone(get_hairgapr())

    # noinspection PyUnusedLocal
    @mock.patch(
        "pkg_resources.get_platform", side_effect=lambda: "macosx-10.14.6-x86_64"
    )
    def test_on_macos_hairgaps(self, mock_):
        self.assertIsNone(get_hairgaps())
