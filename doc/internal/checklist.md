# Checking before updating / pushing changes to brickedit

Warning: this file is work in progress.

## Pushing changes
- Double-check conventions listed in [conventions.py](/doc/internal/conventions.md).

### If it is the first push after a release:
- Update version in [var.py](/src/brickedit/var.py): update values and set `BRICKEDIT_IS_DEV_VERSION` to `True`.

## Release
- Update version in [var.py](/src/brickedit/var.py) ensure values are updated and set `BRICKEDIT_IS_DEV_VERSION` to `False`.