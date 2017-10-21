# pdir2: Pretty dir() printing with joy
[![Build Status](https://travis-ci.org/laike9m/pdir2.svg)](https://travis-ci.org/laike9m/pdir2)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pdir2.svg)](https://pypi.python.org/pypi/pdir2/)
![PyPI Version](https://img.shields.io/pypi/v/pdir2.svg)

Have you ever dreamed of a better output of `dir()`? I do. So I created this.

![](https://github.com/laike9m/pdir2/raw/master/images/presentation_v2.gif)

## Features
* Attributes are grouped by types/functionalities, with beautiful colors.

* Support color customization, [here's how](https://github.com/laike9m/pdir2/wiki/User-Configuration).

* Support all platforms including Windows(Thanks to [colorama](https://github.com/tartley/colorama)).

* Support [ipython](https://github.com/ipython/ipython), [ptpython](https://github.com/jonathanslenders/ptpython), [bpython](https://www.bpython-interpreter.org/) and [Jupyter Notebook](http://jupyter.org/)! See [wiki](https://github.com/laike9m/pdir2/wiki/REPL-Support) for details.

* The return value of `pdir()` can still be used as a list of names.

* You can search for certain names with `.s()` or `.search()`:  

  ![](https://github.com/laike9m/pdir2/raw/master/images/search.gif)

  Search is case-insensitive by default.  
  You can use `.search(name, case_sensitive=True)` to do case sensitive searching.

## Install

### Generic
```
pip install pdir2
```
About the name. I wanted to call it "pdir", but there's already one with this
name on pypi. Mine is better, of course.

### Fedora
```
dnf install python3-pdir2
--or--
dnf install python2-pdir2
```

## Automatic Import
As a better alternative of `dir()`, it's more convenient to automatically import
pdir2 when launching REPL. Luckily, Python provides a way to do this. In you `.bashrc`(or `.zshrc`), add this line:
```
export PYTHONSTARTUP=$HOME/.pythonstartup
```
Then, create `.pythonstartup` in your home folder. Add one line:
```
import pdir
```
Next time you launch REPL, `pdir()` is already there, Hooray!

## Testing
Simply run `pytest`, or use `tox` if you like.
