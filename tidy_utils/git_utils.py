#!/usr/bin/env python
# Author: Haihong Li
#
# File: git_utils.py
# ---------------------------
# My Git utilities. Only works in repo root, not other directories.

import subprocess, os

def _decorate_files(file_list):
    return [ (f if os.path.exists(f) else "- %s" % f) for f in file_list ]

def _get_created_or_modified_from_decorated(decorated_files):
    return [ item for item in decorated_files if not item.startswith("- ") ]

def _get_deleted_from_decorated(list):
    return [ item for item in changed if item.startswith("- ") ]

# get changed files (unstaged + staged)
# NOTE untracked files (i.e. ignored by .gitignore) are not reported
"""
@return list of str - paths, related to repo root (if is deleted files, prefix with "- ")
"""
def get_all_changed():
    COMMAND_STR = "{ git diff --name-only ; git diff --name-only --staged ; } | sort | uniq"
    out = subprocess.check_output(COMMAND_STR, shell=True).decode('utf-8')
    file_list = out.strip().split('\n') if len(out) != 0 else [] # paths are related to repo root
    return _decorate_files(file_list)

# get changed files (staged only)
# NOTE untracked files (i.e. ignored by .gitignore) are not reported
"""
@return list of str - paths, related to repo root (if is deleted files, prefix with "- ")
"""
def get_staged_changed():
    COMMAND_STR = "{ git diff --name-only --staged ; } | sort | uniq"
    out = subprocess.check_output(COMMAND_STR, shell=True).decode('utf-8')
    file_list = out.strip().split('\n') if len(out) != 0 else [] # paths are related to repo root
    return _decorate_files(file_list)

"""
@return list of str - paths, related to repo root (if is deleted files, prefix with "- ")
"""
def get_staged_created_or_modified_files():
    decorated_files = get_staged_changed()
    return _get_created_or_modified_from_decorated(decorated_files)

"""
@return list of str - paths, related to repo root (if is deleted files, prefix with "- ")
"""
def get_staged_deleted_files():
    decorated_files = get_staged_changed()
    return _get_deleted_from_decorated(decorated_files)

FILE_LIST_DUMP = "git-status.log"
def dump_staged_changed_files():
    # collect staged files that are created/modified, but not deleted, reported by 'git status'
    decorated_files = get_staged_changed()
    with open(FILE_LIST_DUMP, 'w') as dump: # overwrite if exists
        dump.write("# staged files only\n")
        dump.write("\n".join(decorated_files))

def _load_from_log(filename):
    with open(filename, 'r') as dump:
        lines = dump.read().split('\n')
    return [ item for item in lines if (len(item) > 0 and not item.startswith("# "))]

"""
return None (if FILE_LIST_DUMP not found)
       list of str - paths, related to repo root (if FILE_LIST_DUMP is present)
"""
def load_staged_created_or_modified_files():
    if not os.path.isfile(FILE_LIST_DUMP):
        return None
    decorated_files = _load_from_log(FILE_LIST_DUMP)
    return _get_created_or_modified_from_decorated(decorated_files)

"""
return None (if FILE_LIST_DUMP not found)
       list of str - paths, related to repo root (if FILE_LIST_DUMP is present)
"""
def load_staged_deleted_files():
    if not os.path.isfile(FILE_LIST_DUMP):
        return None
    decorated_files = _load_from_log(FILE_LIST_DUMP)
    return _get_deleted_from_decorated(decorated_files)

def remove_dumped():
    if os.path.isfile(FILE_LIST_DUMP):
        os.remove(FILE_LIST_DUMP)
