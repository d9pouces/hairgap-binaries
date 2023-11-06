# ############################################################################
#  This file is part of Hairgap                                              #
#                                                                            #
#  Copyright (C) 2020 Matthieu Gallet <github@19pouces.net>                  #
#  All Rights Reserved                                                       #
#                                                                            #
#  You may use, distribute and modify this code under the                    #
#  terms of the (BSD-like) CeCILL-B license.                                 #
#                                                                            #
#  You should have received a copy of the CeCILL-B license with              #
#  this file. If not, please visit:                                          #
#  https://cecill.info/licences/Licence_CeCILL-B_V1-en.txt (English)         #
#  or https://cecill.info/licences/Licence_CeCILL-B_V1-fr.txt (French)       #
#                                                                            #
# ############################################################################
import os
from unittest import TestCase, mock

from hairgap_binaries import get_hairgapr, get_hairgaps


class TestOnLinux(TestCase):
    # noinspection PyUnusedLocal
    @mock.patch("sysconfig.get_platform", side_effect=lambda: "linux-x86_64")
    def test_on_linux_hairgapr(self, mock_):
        target = get_hairgapr()
        self.assertTrue(os.path.isfile(target))

    # noinspection PyUnusedLocal
    @mock.patch("sysconfig.get_platform", side_effect=lambda: "linux-x86_64")
    def test_on_linux_hairgaps(self, mock_):
        target = get_hairgaps()
        self.assertTrue(os.path.isfile(target))


macos = "macosx-10.14.6-x86_64"


class TestOnMacosX(TestCase):
    # noinspection PyUnusedLocal

    @mock.patch("sysconfig.get_platform", side_effect=lambda: macos)
    def test_on_macos_hairgapr(self, mock_):
        self.assertIsNone(get_hairgapr())

    # noinspection PyUnusedLocal
    @mock.patch("sysconfig.get_platform", side_effect=lambda: macos)
    def test_on_macos_hairgaps(self, mock_):
        self.assertIsNone(get_hairgaps())
