# `brickedit`: Constants

This contains common variables used throughout brickedit, such as the current version of brickedit and the supported Brick Rigs version.

### BrickEdit versions:
- `BRICKEDIT_VERSION_MAJOR` (`int`): The major version of brickedit.
- `BRICKEDIT_VERSION_MINOR` (`int`): The minor version of brickedit.
- `BRICKEDIT_VERSION_PATCH` (`int`): The patch version of brickedit.
- `BRICKEDIT_IS_DEV_VERSION` (`bool`): Whether this is a development version of brickedit.
- `BRICKEDIT_VERSION_FULL` (`str`): The full version string of brickedit.

### BrickRigs file versions:
- `FILE_DEV_VERSION` (`int`): The current development version of Brick Rigs files. Note: this is only available for reference. BrickEdit will not support this version yet. Using a dev version will not reveal anything about the upcoming update.
- `FILE_EXP_VERSION` (`int`): The experimental branch version of Brick Rigs files.
- `FILE_MAIN_VERSION` (`int`): The main branch version of Brick Rigs files.
- `FILE_LEGACY_VERSION` (`int`): The legacy branch version of Brick Rigs files (6).

### BrickEdit supported versions:
- `FILE_MAX_SUPPORTED_VERSION` (`int`): The maximum supported Brick Rigs file version by brickedit.
- `FILE_MIN_SUPPORTED_VERSION` (`int`): The minimum supported Brick Rigs file version by brickedit.

### Named constant for Brick Rigs file updates:
- `GROUPS_UPDATE` (`int`): The version in which weld and editor groups were added.
- `FILE_UNIT_UPDATE` (`int`): The version in which units were refactored (past this version BrickRigs uses centimeters only, RGBA,...).

### Visibility constants for metadata serialization:
- `VISIBILITY_PUBLIC` (`int`): Public visibility constant.
- `VISIBILITY_FRIENDS` (`int`): Friends-only visibility constant.
- `VISIBILITY_PRIVATE` (`int`): Private visibility constant.
- `VISIBILITY_HIDDEN` (`int`): Hidden visibility constant.
