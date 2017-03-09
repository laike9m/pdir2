# pdir2: Pretty dir() printing with joy🍺

Have you ever dreamed of a better output of `dir()`? I do. So I created this.

![](https://github.com/laike9m/pdir2/raw/master/images/presentation.gif)

## Features
* Attributes are grouped by types/functionalities, with beautiful colors.

* Support all platforms including Windows(Thanks to [colorama](https://github.com/tartley/colorama)).

* The return value of `pdir()` can still be used as a list of names.

* You can search for certain names with `.s()` or `.search()`:  

  ![](https://github.com/laike9m/pdir2/raw/master/images/search.gif)

## Install
```
pip install pdir2
```
About the name. I wanted to call it `pdir`, but there's already one with this
name on pypi. Mine is better, of course.

## Testing
Simply run `pytest`, or use `tox` if you like.

## Roadmap
- [ ] config color
- [ ] colorful docstring

[![Build Status](https://travis-ci.org/laike9m/pdir2.svg)](https://travis-ci.org/laike9m/pdir2)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pdir2.svg)](https://pypi.python.org/pypi/pdir2/)
