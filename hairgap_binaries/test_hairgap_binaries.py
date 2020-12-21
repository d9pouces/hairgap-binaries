from unittest import TestCase, mock

import pkg_resources

from hairgap_binaries import get_hairgapr


class TestOnLinux(TestCase):
    # noinspection PyUnusedLocal
    @mock.patch("pkg_resources.get_platform", side_effect=lambda: "linux-x86_64")
    def test_on_linux(self, mock_):
        self.assertEqual(
            pkg_resources.resource_filename(
                "hairgap_binaries", "manylinux2014_x86_64-hairgapr"
            ),
            get_hairgapr(),
        )


class TestOnMacosX(TestCase):
    # noinspection PyUnusedLocal
    @mock.patch(
        "pkg_resources.get_platform", side_effect=lambda: "macosx-10.14.6-x86_64"
    )
    def test_on_linux(self, mock_):
        self.assertIsNone(get_hairgapr())
