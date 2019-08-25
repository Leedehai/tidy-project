#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: filename_match.py
# ---------------------------
# Check whether filename matches with the file name in the head comment.
# NOTE it only runs on git-staged files, and it does NOT modify files.

import os, sys, re
import tidy_utils.git_utils as git_utils

INTERESTED_FILENAME_SUFFIXES = [
    ".cc", ".cpp", ".c", ".h",
    ".py", ".sh", ".js",
    ".json", ".yaml", ".yml", ".sch"
]
def is_interested(filename):
    for suffix in INTERESTED_FILENAME_SUFFIXES:
        if filename.endswith(suffix):
            return True
    return False

FILENAME_LINE = re.compile(r'\A(#|\s?\*)\s?(F|f)ile:\s+(.+)')

"""
@args: filepath: str - the path to the file to be examined
       print_error: bool - if print error
@return: bool - whether the file is ok
         int or None - the line number of the comment line
         str or None - the comment filename
         str or None - the real filename
"""
def check_file(filepath, print_error=True):
    with open(filepath, 'r') as f:
        first_lines = [ f.readline() for _ in range(8)]
        for i, line in enumerate(first_lines):
            matchObj = FILENAME_LINE.match(line)
            if matchObj:
                comment_filename = matchObj.group(3)
                filename = os.path.basename(filepath)
                if comment_filename != filename:
                    res = (False, i + 1, comment_filename, filename)
                    if print_error:
                        print("[Error] %s line %d:" % (res[0], res[1]))
                        print("     filename in intro is \x1b[38;5;196m%s\x1b[0;m" % res[2])
                        print("     but should be \x1b[38;5;155m%s\x1b[0;m" % res[3])
                    return res
    return (True, None, None, None)

"""
@return: bool - whether the repo at current working directory is ok
         int - number errors
"""
def check_dir(target):
    filepaths = []
    if os.path.isdir(".git"): # .git is present
        all_filepaths = git_utils.load_staged_created_or_modified_files()
        if all_filepaths == None:
            all_filepaths = git_utils.get_staged_created_or_modified_files()
        filepaths = [ f for f in all_filepaths if is_interested(f) ]
    else: # .git is missing
        for dirpath, _, filenames in os.walk(target):
            for filename in filenames:
                if not is_interested(filename):
                    continue
                filepaths.append(os.path.join(dirpath, filename))

    error_count = 0
    for filepath in filepaths:
        res = check_file(filepath=filepath, print_error=False)
        if res[0] == False:
            error_count += 1
            print("[%02d] %s line %d:" % (error_count, filepath.replace("./", ""), res[1]))
            print("     filename in intro is \x1b[38;5;196m%s\x1b[0;m" % res[2])
            print("     but should be \x1b[38;5;155m%s\x1b[0;m" % res[3])
    if error_count != 0:
        print("%d errors found" % error_count)
        return False, error_count
    else:
        return True, 0

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Check if the filename in the head comment matches real filename",
        epilog="if 'target' is a directory:\n" +
               "   if .git is missing, recursively visit each file\n" +
               "   if .git is present, visit each staged created/modified file",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("target", nargs=1, help="path to directory or one file")
    args = parser.parse_args()

    target = args.target[0]
    if os.path.isfile(target):
        passed = check_file(target)[0]
    elif os.path.isdir(target):
        passed = check_dir(target)
    else:
        print("[Error] not found: %s" % target)
        return 1

    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())