#!/usr/bin/env python
# Author: Haihong Li
#
# File: git_utils.py
# ---------------------------
# My Git utilities.

import subprocess

# get tracked modified files (unstaged + staged)
"""
@return list of str
"""
def get_all_modified_in_tracked():
    COMMAND_STR = "{ git diff --name-only ; git diff --name-only --staged ; } | sort | uniq"
    out = subprocess.check_output(COMMAND_STR, shell=True).decode('utf-8')
    file_list = out.strip().split('\n') if len(out) != 0 else []
    return file_list

# get tracked modified files (staged only)
"""
@return list of str
"""
def get_staged_modified_in_tracked():
    COMMAND_STR = "{ git diff --name-only --staged ; } | sort | uniq"
    out = subprocess.check_output(COMMAND_STR, shell=True).decode('utf-8')
    file_list = out.strip().split('\n') if len(out) != 0 else []
    return file_list