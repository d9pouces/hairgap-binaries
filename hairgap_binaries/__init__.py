# ###########################################################################
#  This file is part of Hairgap                                             #
#                                                                           #
#  Copyright (C) 2020 Matthieu Gallet <github@19pouces.net>                 #
#  All Rights Reserved                                                      #
#                                                                           #
#  You may use, distribute and modify this code under the                   #
#  terms of the (BSD-like) CeCILL-B license.                                #
#                                                                           #
#  You should have received a copy of the CeCILL-B license with             #
#  this file. If not, please visit:                                         #
#  https://cecill.info/licences/Licence_CeCILL-B_V1-en.txt (English)        #
#  or https://cecill.info/licences/Licence_CeCILL-B_V1-fr.txt (French)      #
#                                                                           #
# ###########################################################################
"""Return the path of the hairgap{r,s} binaries, if available."""
__all__ = ["get_hairgapr", "get_hairgaps"]
__author__ = "Matthieu Gallet"

import atexit
import importlib.resources
import sysconfig
from contextlib import ExitStack
from typing import Optional

known_platforms = {"linux-x86_64"}


def get_hairgapr(suffix="hairgapr") -> Optional[str]:
    """Return the path of the hairgapr binary."""
    n = sysconfig.get_platform()
    if n not in known_platforms:
        return None
    file_manager = ExitStack()
    atexit.register(file_manager.close)
    module = "hairgap_binaries"
    ref = importlib.resources.files(module).joinpath(f"{n}-{suffix}")
    return str(file_manager.enter_context(importlib.resources.as_file(ref)))


def get_hairgaps() -> Optional[str]:
    """Return the path of the hairgaps binary."""
    return get_hairgapr(suffix="hairgaps")
