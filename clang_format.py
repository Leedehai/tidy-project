#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: clang_format.py
# ---------------------------
# Formats staged modified files, according to project's .clang-format, and restage.
# Basically does git-clang-format's work, but I'd like to keep dependency small.

import os, sys, subprocess
import git_utils, should_visit # my own

THIS_DIR = os.path.dirname(__file__)
FORMAT_UTIL = "clang-format"


def print_out(silent, content):
    if not silent:
        print(content)

"""
@args filename: str - the path to the file
      silent_if_ok: bool - if True, do not print
@return bool - if the utility returned successfully
"""
def format_file(filename, silent_if_ok=False):
    if not should_visit.should_visit(filename):
        print_out(silent_if_ok, "\tskip  %s" % filename)
        return True # assume success
    print_out(silent_if_ok, "\tvisit %s" % filename)
    # -i: modify in-place
    if 0 != subprocess.call(" ".join([FORMAT_UTIL, "-i", filename]), shell=True):
        print_out(True, "[Error] error: %s -i %s" % (FORMAT_UTIL, filename))
        print_out(True, "        did you installed clang-format?")
        print_out(True, "        do you have .clang-format at project root?")
        return False
    return True

"""
@args silent_if_ok: bool - if True, do not print
@return bool - if the utility returned successfully
"""
def format_cwd_staged(silent_if_ok=False):
    files = git_utils.get_staged_modified_in_tracked() # modified files (staged only)
    if len(files) == 0:
        print_out(silent_if_ok, "[Info] no staged modified file, no work to be done")
        return True # assume success
    files_visited = []
    for path in files:
        if not os.path.isfile(path):
            continue # file is deleted rather than created/modified
        files_visited.append(path)
        if format_file(path, silent_if_ok) == False:
            return False # immediately return, do not progress to the next file

    # restage the visited files (some might be formatted; some are kept intact) and exit, but don't commit
    if 0 == subprocess.call(" ".join(["git add"] + files_visited), shell=True):
        return True
    else:
        print("[Error] error at re-running 'git add' after formatting")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Formats staged modified files, according to project's .clang-format, and restage.",
        epilog="you need to install clang-format program and have '.clang-format' config file")
    parser.add_argument("-s", "--silent", action="store_true", help="no printing")
    args = parser.parse_args()

    if not os.path.isdir(".git"):
        print("[Error] you are not at this project's root")
        sys.exit(1)
    successful = format_cwd_staged()
    sys.exit(0 if successful else 1)