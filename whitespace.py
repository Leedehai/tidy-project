#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: whitespace.py
# ---------------------------
# Check whitespace discipline of one file or a repo.

import os, sys
import tidy_utils.git_utils as git_utils
import tidy_utils.should_visit as should_visit

"""
@args: filename: str - path to file
       silent_if_ok: bool - no printing if no error
       details: bool - whether details need to be printed
@return: bool - whether the file passes
         int  - number of errors
"""
def check_file(filename, silent_if_ok=False, details=False):
    if not should_visit.should_visit(filename):
        if not silent_if_ok:
            print("\tskip %s" % filename)
        return True, 0 # assume it is passed

    if os.path.isdir(filename):
        print("[Error] path %s is a directory" % filename)
        raise ValueError
    if not os.path.isfile(filename):
        # file not found, assume it is because the file is deleted rather than created/modified
        return True, 0

    num_error, num_line, errors = 0, 0, []
    with open(filename, 'r') as f: # read-only
        line = ""
        prev_line = ""
        while True:
            line = f.readline()
            if len(line) == 0: # end of file
                break
            num_line += 1
            tab_count = line.count('\t') # for '\t'
            if tab_count != 0:
                num_error += 1
                if details:
                    errors.append("- Tab: %d tab%s on line %d" % (tab_count, 's' if tab_count > 1 else '', num_line))
            if len(line.rstrip()) != len(line.rstrip('\n')): # for trailing whitespaces
                num_error += 1
                if details:
                    errors.append("- Whitespace: trailing whitespaces on line %d" % num_line)
            prev_line = line

        if prev_line != "" and prev_line != "\n":
            pass # deactivated to indulge clang-format's behavior of removing last newline
            # num_error += 1
            # if details:
            #     errors.append("- Newline missing: the last line is not \"\\n\"")

    if num_error > 0 and not details:
        errors.append("\t- %d whitespace error%s in file %s" % (num_error, 's' if num_error > 1 else '', filename))
        errors.append("\t  for details: %s %s -d" % ("utils/tidy/whitespace.py", filename))

    if silent_if_ok and num_error == 0:
        pass
    else:
        print("\tvisit %s" % filename)
        if len(errors):
            print("\n".join(errors))

    return True if num_error == 0 else False, num_error

"""
@args: target: str - path to target (repo or file)
       silent_if_ok: bool - no printing if no error
       details: bool - whether details need to be printed
@return: bool - whether the target passes
         int  - number of errors (file: whitespace errors; repo: number of bad files)
"""
def check(target, silent_if_ok=False, details=False):
    if os.path.isfile(target):
        return check_file(target, silent_if_ok, details)

    filepaths = []
    if os.path.isdir(".git"): # .git is present
        filepaths = git_utils.load_staged_created_or_modified_files()
        if filepaths == None:
            filepaths = git_utils.get_staged_created_or_modified_files()
    else: # .git is missing
        for dirpath, _, filenames in os.walk(target):
            for filename in filenames:
                filepaths.append(os.path.join(dirpath, filename))

    bad_file_count = 0
    for path in filepaths:
        if check_file(path, silent_if_ok, details)[0] == False:
            bad_file_count += 1
    return True if bad_file_count == 0 else False, bad_file_count

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Check whitespace discipline",
        epilog="if 'target' is a directory:\n" +
               "   if .git is missing, recursively visit each file\n" +
               "   if .git is present, visit each staged created/modified file",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("target", nargs=1, help="path to repo directory or one file")
    parser.add_argument("-d", "--details", action="store_true", help="print details of error")
    parser.add_argument("-s", "--silent", action="store_true", help="no printing if no error is encountered")
    args = parser.parse_args()

    passed = check(target=args.target[0], silent_if_ok=args.silent, details=args.details)[0]
    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())