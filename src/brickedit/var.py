from typing import Final

BRICKEDIT_VERSION_MAJOR: Final[int] = 5
BRICKEDIT_VERSION_MINOR: Final[int] = 0
BRICKEDIT_VERSION_PATCH: Final[int] = 0
BRICKEDIT_IS_DEV_VERSION: Final[bool] = True
BRICKEDIT_VERSION_FULL: Final[str] = (
    str(BRICKEDIT_VERSION_MAJOR) + '.' +
    str(BRICKEDIT_VERSION_MINOR) + '.' +
    str(BRICKEDIT_VERSION_PATCH) +
    ("-dev" if BRICKEDIT_IS_DEV_VERSION else "")
)

FILE_EXP_VERSION: Final[int] = 16
FILE_MAIN_VERSION: Final[int] = 15
FILE_LEGACY_VERSION: Final[int] = 6
