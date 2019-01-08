Taken from a larger project of mine; may be out-of-sync.

# tidy

Scripts that are used to keep a Git repository "tidy".

### Scripts
These commandline utilities are responsible for different aspects. For details, use `--help`.
- `clang_format.py`: format a file or the repo with program [clang-format](https://clang.llvm.org/docs/ClangFormat.html) (you need to install it) according to the repo's `.clang-format` file.
- `whitespace.py`: check whitespace discipline of one file or the repo, e.g. no tabs is C++ files.
- `filename_match.py`: check whether filename matches with the file name in the head comment of a file.
- `dirname_discipline`: check directory name discipline, e.g. `unit-test/` exists if `include/` exists, and no conflicting module names.

Each script above can be used as a Python library as well.

### Run them all

Executing `all.py` at the repo root will run all tidiness checkers altogether.

If [clang-format](https://clang.llvm.org/docs/ClangFormat.html) is not installed, or `.clang-format` is missing, then `clang_format.py` is skipped.

`all.py --help` gives the help message.

### Package
This directory is also a Python package, so you may use it like this:
```python
import tidy.whitespace
# do some work...
```

> `all.py` is recommended to be added to Git's `pre-commit` script.

### Does it scale with large repo?
Yes. It only checks staged files that are created/modified reported by command `git status`.

###### EOF
