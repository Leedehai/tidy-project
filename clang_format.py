#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: clang_format.py
# ---------------------------
# Formats staged modified files, according to project's .clang-format, and restage.
# Basically does git-clang-format's work, but I'd like to keep dependency small.

import os, sys, subprocess
import tidy_utils.git_utils as git_utils
import tidy_utils.should_visit as should_visit

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
def format_cwd(silent_if_ok=False):
    files = git_utils.load_staged_created_or_modified_files()
    if files == None:
        files = git_utils.get_staged_created_or_modified_files()

    if len(files) == 0:
        print_out(silent_if_ok, "[Info] no staged created/modified file, no work to do")
        return True # assume success

    for path in files:
        if format_file(path, silent_if_ok) == False: # problem encountered
            return False # immediately return, do not progress to the next file

    # restage the visited files (some might be formatted; some are kept intact) and exit, but don't commit
    if 0 == subprocess.call(" ".join(["git add"] + files), shell=True):
        return True
    else:
        print("[Error] error at re-running 'git add' after formatting")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Formats staged created/modified files, according\n" +
                    "project's .clang-format, and restage.\n" +
                    "You need to be at the repository's root.",
        epilog="you need to install clang-format program:\n" +
               "   https://clang.llvm.org/docs/ClangFormat.html\n" +
               "and have '.clang-format' config file in project root.\n" +
               "To format a single file, just use clang-format.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", "--silent", action="store_true", help="no printing")
    args = parser.parse_args()

    if not os.path.isdir(".git"):
        print("[Error] directory .git is missing.")
        print("        Either you are not at this project's root,")
        print("        or this is not a Git repository.")
        return 1
    successful = format_cwd()
    return 0 if successful else 1

if __name__ == "__main__":
    sys.exit(main())