# Building BrickEdit Wheels
Warning: This file is a work in progress.

To build BrickEdit wheels on Linux...
```sh
python3 -m pip install build
python3 -m build --wheel
```
Building them on Windows is effectively the same process, besides the fact you can use the alias `py`.

----

The resulting wheels can be found in `./dist/`.