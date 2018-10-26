# Python Utilities

This repository provides various utilities for python 3.

## Documentation

The most complete documentation is given by the output of `doxygen`; to view this
documentation, navigate to the `doc/doxygen` directory and run `doxygen`:

```
doxygen Doxyfile
```

The root HTML output file is `doc/doxygen/html/index.html`.

## Code Formatting

This code is formatted using `yapf` (Yet Another Python Formatter). The style
file used is `.style.yapf`. To format a single file:

```
yapf -i /path/to/file.py
```

The `-i` argument specifies the formatting to be applied to the file instead of
just printing out the result to the screen. To apply formatting to the entire
code base, just run the provided formatting script:

```
./format.sh
```
