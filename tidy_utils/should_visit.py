#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: should_visit.py
# ---------------------------
# Check if a file should be inspected based on the file type.

import os

should_not_visit_dirs = ["xeno/", "test-inputs/", "test-expected/", "zen/", "docs/"]

def should_visit(path):
    filename = os.path.abspath(path)
    for dirname in should_not_visit_dirs:
        if dirname in filename:
            return False

    if filename.endswith(".h"):
        return True
    elif filename.endswith(".c") or filename.endswith(".cc") or filename.endswith(".cpp"):
        return True
    elif filename.endswith(".js"):
        return True

    # all else..
    return False