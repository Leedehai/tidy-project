This repo might be out-of-sync with the tools I actually use.

# tidy

Scripts that are used to keep the project "tidy".

### Scripts
These commandline utilities are responsible for different aspects. For details, use `--help`.
- `clang_format.py`: format a file or this repo with program `clang-format` (you need to install it) according to this repo's `.clang-format` file.
- `whitespace.py`: check whitespace discipline of one file or this repo, e.g. no tabs is C++ files.
- `filename_match.py`: check whether filename matches with the file name in the head comment of a file.
- `dirname_discipline`: check directory name discipline, e.g. `unit-test/` exists if `include/` exists, and no conflicting module names.

### Run them all
Each scripts above can be used as a Python library as well. Executing `all.py` will run them altogether.

`all.py --help` gives the help message.

### Package
This directory is also a Python package, so you may use it like this:
```python
import tidy.whitespace
# do some work...
```

> `all.py` is recommended to be added to Git's `pre-commit` script.

###### EOF

