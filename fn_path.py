# -*- coding: utf-8 -*-
"""This module contains functions for determining path to files for the other modules."""

import os
import mode


def concat_gui(file):
    """Convert a GUI image name into an expected path to that GUI image element

        Args:
            file (str): Image filename

        Returns:
            (str): A string which represents the concatenated path the indicated GUI image element
    """

    return os.path.join(mode.app_root, 'img', 'gui', file)