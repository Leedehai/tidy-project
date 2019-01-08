This repo might be out-of-sync with the tools I actually use.

# tidy

Scripts that are used to keep a project "tidy".

### Scripts
These commandline utilities are responsible for different aspects. For details, use `--help`.
- `clang_format.py`: format a file or your repo with program [clang-format](https://clang.llvm.org/docs/ClangFormat.html) according to your repo's `.clang-format` file.
- `whitespace.py`: check whitespace discipline of one file or the repo, e.g. no tabs is C++ files.
- `filename_match.py`: check whether filename matches with the file name in the head comment of a file.
- `dirname_discipline`: check directory name discipline, e.g. `unit-test/` exists if `include/` exists, and no conflicting module names.

Each script above can be used as a Python library as well.

### Run them all

Executing `all.py` at the repo root will run all tidiness checkers altogether.

If [clang-format](https://clang.llvm.org/docs/ClangFormat.html) is not installed, or `.clang-format` is missing, then `clang_format.py` is skipped.

`--help` gives the help message.

### Package
This directory is also a Python package, so you may use it like this:
```python
import tidy.whitespace
# do some work...
```

> `all.py` is recommended to be added to Git's `pre-commit` script.

###### EOF

