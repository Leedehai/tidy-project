#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: all.py
# ---------------------------
# Run all tidiness scripts. Could be used by pre-commit.

import os, sys, subprocess
# tidy script modules
import dirname_discipline
import filename_match
import whitespace
import clang_format

def print_stage(silent, content):
    if not silent:
        print(content)

def check_each_status(dirname_passed, whitespace_passed, filename_passed, clang_format_done):
    if not dirname_passed:
        print("tidy: error at tidy.dirname_discipline")
    if not filename_passed:
        print("tidy: error at tidy.filename_match")
    if not whitespace_passed:
        print("tidy: error at tidy.whitespace")
    if not clang_format_done:
        print("tidy: error at tidy.clang_format")
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
def run_file(filename, silent_if_ok=False):
    print_stage(silent_if_ok, "tidy.dirname_discipline: skipped") # as this is a file
    dirname_passed = True
    print_stage(silent_if_ok, "tidy.filename_match: running...")
    filename_passed = filename_match.check_file(filename)
    print_stage(silent_if_ok, "tidy.whitespace: running...")
    whitespace_passed = whitespace.check_file(filename=filename, silent_if_ok=silent_if_ok)[0]
    if check_clang_format_prereq(silent_if_ok) == True:
        print_stage(silent_if_ok, "tidy.clang_format: running...")
        clang_format_done = clang_format.format_file(filename=filename, silent_if_ok=silent_if_ok)
    else:
        clang_format_done = True # assume success, as it's not essential

    return check_each_status(dirname_passed, whitespace_passed, filename_passed, clang_format_done)

# export as library interface
def run_repo(silent_if_ok=False):
    print_stage(silent_if_ok, "tidy.dirname_discipline: running...")
    dirname_passed = dirname_discipline.check_cwd()
    print_stage(silent_if_ok, "tidy.filename_match: running...")
    filename_passed = filename_match.check_dir(".")[0]
    print_stage(silent_if_ok, "tidy.whitespace: running...")
    whitespace_passed = whitespace.check(target=".", silent_if_ok=silent_if_ok)[0]
    if check_clang_format_prereq(silent_if_ok) == True:
        print_stage(silent_if_ok, "tidy.clang_format: running...")
        clang_format_done = clang_format.format_cwd_staged(silent_if_ok=silent_if_ok)
    else:
        clang_format_done = True # assume success, as it's not essential

    if not dirname_passed:
        print("tidy: error at tidy.dirname_discipline")
    if not filename_passed:
        print("tidy: error at tidy.filename_match")
    if not whitespace_passed:
        print("tidy: error at tidy.whitespace")
    if not clang_format_done:
        print("tidy: error at tidy.clang_format")
    return check_each_status(dirname_passed, whitespace_passed, filename_passed, clang_format_done)

if __name__ == "__main__":
    # could be used by Git's pre-commit
    import argparse
    parser = argparse.ArgumentParser(
        description="Run all scripts in %s on a file or this directory" % os.path.dirname(__file__),
        epilog="you need to be at the project's root")
    parser.add_argument("target", nargs='?', help="file path, if absent, run on current directory")
    parser.add_argument("-s", "--silent", action="store_true", help="no printout if no error detected")
    args = parser.parse_args()

    if args.target and os.path.isfile(args.target):
        passed = run_file(args.target, args.silent)
    elif not args.target:
        if not os.path.isfile("LICENSE.txt"):
            print("[Error] you are not at this project's root")
            sys.exit(1)
        passed = run_repo(args.silent)
    else:
        if os.path.isdir(args.target):
            print("[Error] 'target' argument should be a file, use --help")
        else:
            print("[Error] file not found: %s" % args.target)
        sys.exit(1)

    sys.exit(0 if passed else 1)
