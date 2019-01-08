#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: Haihong Li
#
# File: dirname_discipline.py
# ---------------------------
# Check directory name discipline

import os, sys

"""
@return: bool - whether the repo (current working directory) passed
"""
def check_cwd():
    include_exist = os.path.isdir("include")
    src_exist = os.path.isdir("src")
    unit_tests_exist = os.path.isdir("unit-tests")
    tests_exist = os.path.isdir("tests") # can be missing

    if not include_exist:
        return True # this is not a C/C++ repo, then assume it passed

    # now, include_exist == True
    dir_missing = False
    if not src_exist:
        print("[Error] not found: ./src")
        dir_missing = True
    if not unit_tests_exist:
        print("[Error] not found: ./unit-tests")
        dir_missing = True
    if dir_missing:
        return False

    has_error = False

    include_readme_exist = os.path.isfile("include/README.md")
    src_readme_exist = os.path.isfile("src/README.md")
    unit_readme_tests_exist = os.path.isfile("unit-tests/README.md")
    tests_readme_exist = os.path.isfile("tests/README.md")

    if not include_readme_exist:
        print("[Error] not found: ./include/README.md")
        has_error = True
    if not src_readme_exist:
        print("[Error] not found: ./src/README.md")
        has_error = True
    if not unit_readme_tests_exist:
        print("[Error] not found: ./unit-tests/README.md")
        has_error = True
    if tests_exist and not tests_readme_exist: # can be missing
        print("[Error] not found: ./tests/README.md")
        has_error = True

    modules = {} # key: name, value: number of files
    for item in os.listdir("include"):
        path = os.path.join("include", item)
        if not os.path.isdir(path):
            continue
        path_ls = os.listdir(path)
        for subitem in path_ls:
            subpath = os.path.join(path, subitem)
            if os.path.isdir(os.path.join(path, subitem)):
                print("[Error] %s contains a directory %s" % (path, subitem))
                has_error = True
        modules[item] = len([subitem for subitem in path_ls if not subitem.startswith(".")])

    # xeno
    if os.path.isdir("xeno"):
        xeno_ls = os.listdir("xeno")
        for item in xeno_ls:
            path = os.path.join("xeno", item)
            if not (os.path.isdir(path) and os.path.isfile(os.path.join(path, "LICENSE.txt"))):
                continue
            xeno_component_ls = os.listdir(path)
            if "include" in xeno_component_ls:
                has_unit_tests = "unit-tests" in xeno_component_ls
                if not has_unit_tests:
                    print("[Error] unit-tests expected to exist in %s" % path)
                    has_error = True
                for item2 in os.listdir(os.path.join(path, "include")):
                    if os.path.isdir(os.path.join(path, "include", item2)):
                        if item2 in modules:
                            print("[Error] conflicting module name: %s" % item2)
                        else:
                            modules[item2] = None

    for item in os.listdir("src"):
        path = os.path.join("src", item)
        if not os.path.isdir(path):
            continue
        has_error = False
        path_ls = os.listdir(path)
        for subitem in path_ls:
            subpath = os.path.join(path, subitem)
            if os.path.isdir(os.path.join(path, subitem)):
                print("[Error] %s contains a directory %s" % (path, subitem))
                has_error = True
        if item not in modules:
            print("[Error] src/%s has no match in include/" % path)
            has_error = True

    for item in os.listdir("unit-tests"):
        path = os.path.join("unit-tests", item)
        if not os.path.isdir(path) or item == "build":
            continue
        has_error = False
        if item not in modules:
            print("[Error] unit-tests/%s has no match in include/" % path)
            has_error = True

    if tests_exist: # can be missing
        for item in os.listdir("tests"):
            path = os.path.join("unit-tests", item)
            if not os.path.isdir(path) or item == "build":
                continue
            has_error = False
            if item not in modules:
                print("[Error] unit-tests/%s has no match in include/" % path)
                has_error = True

    return True if not has_error else False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check directory name discipline", epilog="if the target is a repo, then it should be your current working directory")
    parser.add_argument("target", nargs='+', help="path to repo directory or one file")
    args = parser.parse_args()

    if len(sys.argv[1:]) != 1:
        print("[Error] need path to repo as argument")
        sys.exit(1)

    REPO_DIR = os.path.abspath(sys.argv[1])
    if not os.path.samefile(REPO_DIR, "."):
        print("[Error] you are not at project root")
        sys.exit(1)

    check_cwd()