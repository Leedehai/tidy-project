#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: all.py
# ---------------------------
# Run all tidiness scripts. Could be used by pre-commit.

import os, sys, subprocess
import tidy_utils.git_utils as git_utils
# tidy script modules
import dirname_discipline
import filename_match
import whitespace
import clang_format

UNIT_1024 = ['','K','M','G','T','P','E','Z']
def sizeof_fmt(num, suffix='B'):
    for unit in UNIT_1024:
        if abs(num) < 1024.0:
            return "%.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def print_decription(filenames):
    print(" - tidy.dirname_discipline")
    print(" - tidy.filename_match")
    print(" - tidy.clang_format")
    print(" - tidy.whitespace")
    if len(filenames) > 0:
        print("\n".join([
            "\t%s (%s)" % (item, sizeof_fmt(os.stat(item).st_size)) for item in filenames
        ]))
    else:
        print("\t(no staged created/modified files)")

def print_stage(silent, content):
    if not silent:
        print(content)

def check_each_status(dirname_passed, whitespace_passed, filename_passed, clang_format_done):
    if not dirname_passed:
        print("[x] tidy: error at tidy.dirname_discipline")
    if not filename_passed:
        print("[x] tidy: error at tidy.filename_match")
    if not clang_format_done:
        print("[x] tidy: error at tidy.clang_format")
    if not whitespace_passed:
        print("[x] tidy: error at tidy.whitespace")
    return all([dirname_passed, whitespace_passed, filename_passed, clang_format_done])

def check_clang_format_prereq(silent_if_ok):
    if subprocess.call("which clang-format > /dev/null", shell=True) != 0:
        print_stage(silent_if_ok, "tidy.clang_format: skipped - program 'clang-format' not installed")
        return False
    elif not os.path.isfile(".clang-format"):
        print_stage(silent_if_ok, "tidy.clang_format: skipped - config '.clang-format' not found at repo root")
        return False
    return True

# export as library interface
def run_file(filename, silent_if_ok=False, with_description=False):
    if with_description:
        print_decription([filename])

    print_stage(silent_if_ok, "tidy.dirname_discipline: skipped") # as this is a file
    dirname_passed = True
    print_stage(silent_if_ok, "tidy.filename_match: running...")
    filename_passed = filename_match.check_file(filename)
    if check_clang_format_prereq(silent_if_ok) == True:
        print_stage(silent_if_ok, "tidy.clang_format: running...")
        clang_format_done = clang_format.format_file(filename=filename, silent_if_ok=silent_if_ok)
    else:
        clang_format_done = True # assume success, as it's not essential
    print_stage(silent_if_ok, "tidy.whitespace: running...")
    whitespace_passed = whitespace.check_file(filename=filename, silent_if_ok=silent_if_ok)[0]

    return check_each_status(dirname_passed, whitespace_passed, filename_passed, clang_format_done)

# export as library interface
def run_repo(silent_if_ok=False, with_description=False):
    # write staged changed files to current working directory
    git_utils.dump_staged_changed_files()

    if with_description:
        print_decription(git_utils.load_staged_created_or_modified_files())

    print_stage(silent_if_ok, "tidy.dirname_discipline: on all files")
    dirname_passed = dirname_discipline.check_cwd()
    print_stage(silent_if_ok, "tidy.filename_match:     on staged files")
    filename_passed = filename_match.check_dir(".")[0]
    if check_clang_format_prereq(silent_if_ok) == True:
        print_stage(silent_if_ok, "tidy.clang_format:       on staged files")
        clang_format_done = clang_format.format_cwd(silent_if_ok=silent_if_ok)
    else:
        clang_format_done = True # assume success, as it's not essential
    print_stage(silent_if_ok, "tidy.whitespace:         on staged files")
    whitespace_passed = whitespace.check(target=".", silent_if_ok=silent_if_ok)[0]

    # remove dumped
    git_utils.remove_dumped()

    return check_each_status(dirname_passed, whitespace_passed, filename_passed, clang_format_done)

def main():
    # could be used by Git's pre-commit
    import argparse
    parser = argparse.ArgumentParser(
        description="Run all scripts in %s on a file or this Git repository" % os.path.dirname(__file__),
        epilog="Your current working directory should be the Git repository's root")
    parser.add_argument("target", nargs='?', help="file path, if absent, run on current directory")
    parser.add_argument("-s", "--silent", action="store_true", help="no printout, unless errors are dectected")
    parser.add_argument("-w", "--with-description", action="store_true",
                        help="print a short description, overriding -s/--silent")
    args = parser.parse_args()

    if args.target and os.path.isfile(args.target):
        passed = run_file(args.target, args.silent, args.with_description)
    elif not args.target:
        if not os.path.isdir(".git"):
            print("[Error] directory .git is missing.")
            print("        Either you are not at this project's root,")
            print("        or this is not a Git repository.")
            return 1
        passed = run_repo(args.silent, args.with_description)
    else:
        if os.path.isdir(args.target):
            print("[Error] 'target' argument should be a file,")
            print("        but '%s' is a directory." % args.target)
            print("        use --help for help message")
        else:
            print("[Error] file not found: %s" % args.target)
        return 1

    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
