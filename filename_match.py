#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: filename_match.py
# ---------------------------
# Check whether filename matches with the file name in the head comment

import os, sys, re

INTERESTED_FILENAME_SUFFIXES = [
    ".cc", ".cpp", ".c", ".h",
    ".py", ".sh", ".js",
    ".json", ".yaml", ".yml", ".sch"
]
FILENAME_LINE = re.compile(r'\A(#|\s?\*)\s?(F|f)ile:\s+(.+)')

"""
@args: filepath: str - the path to the file to be examined
       checking_dir: bool - if this function is used by check_cwd()
@return: bool - whether the file is ok
         The following are present only if the file is not ok:
         int - the line number of the comment line
         str - the comment filename
         str - the real filename
"""
def check_file(filepath, checking_dir=False):
    # skip if under test-inputs as they are not important here
    if "test-inputs/" in filepath:
        return (True,)
    with open(filepath, 'r') as f:
        first_lines = [ f.readline() for _ in range(8)]
        for i, line in enumerate(first_lines):
            matchObj = FILENAME_LINE.match(line)
            if matchObj:
                comment_filename = matchObj.group(3)
                filename = os.path.basename(filepath)
                if comment_filename != filename:
                    res = (False, i + 1, comment_filename, filename)
                    if not checking_dir:
                        print("[Error] %s line %d:" % (res[0], res[1]))
                        print("     filename in intro is \x1b[38;5;196m%s\x1b[0;m" % res[2])
                        print("     but should be \x1b[38;5;155m%s\x1b[0;m" % res[3])
                    return res
    return (True,)

"""
@return: bool - whether the repo at current working directory is ok
         int - number errors
"""
def check_dir(target):
    error_count = 0
    for dirpath, _, filenames in os.walk(target):
        for filename in filenames:
            is_interested = False
            for suffix in INTERESTED_FILENAME_SUFFIXES:
                if filename.endswith(suffix):
                    is_interested = True
                    break
            if not is_interested:
                continue
            filepath = os.path.join(dirpath, filename)
            res = check_file(filepath=filepath, checking_dir=True)
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Check if the filename in the head comment matches real filename",
        epilog="if 'target' is a directory, then recursively visit each file")
    parser.add_argument("target", nargs='+', help="path to directory or one file")
    args = parser.parse_args()

    if len(args.target) != 1:
        print("[Error] one path expected, %d given" % len(args.target))
        sys.exit(1)

    target = args.target[0]
    if os.path.isfile(target):
        passed = check_file(target)[0]
    elif os.path.isdir(target):
        passed = check_dir(target)
    else:
        print("[Error] not found: %s" % target)
        sys.exit(1)

    sys.exit(0 if passed else 1)