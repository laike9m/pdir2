# pdir2: Pretty dir() printing with joy

![Build status](https://github.com/laike9m/pdir2/actions/workflows/ci.yml/badge.svg)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pdir2.svg)](https://pypi.python.org/pypi/pdir2/)
![PyPI Version](https://img.shields.io/pypi/v/pdir2.svg)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Have you ever dreamed of a better output of `dir()`? I do. So I created this.

![](https://github.com/laike9m/pdir2/raw/master/images/presentation_v2.gif)

## Features

-   Attributes are grouped by types/functionalities, with beautiful colors.

-   Support color customization, [here's how](https://github.com/laike9m/pdir2/wiki/User-Configuration).

-   Support all platforms including Windows(Thanks to [colorama](https://github.com/tartley/colorama)).

-   Support [ipython](https://github.com/ipython/ipython), [ptpython](https://github.com/jonathanslenders/ptpython), [bpython](https://www.bpython-interpreter.org/) and [Jupyter Notebook](http://jupyter.org/)! See [wiki](https://github.com/laike9m/pdir2/wiki/REPL-Support) for details.

-   The return value of `pdir()` can still be used as a list of names.

-   ✨ Attribute searching

    You can search for certain names with `.s()` or `.search()`:

    ![](https://github.com/laike9m/pdir2/raw/master/images/search.gif)

    Search is case-insensitive by default.
     `search(name, case_sensitive=True)` does case-sensitive searching.

-   :star2: Attribute filtering

    `properties`: Find properties/variables defined in the inspected object.

    `methods`: Find methods/functions defined in the inspected object.

    `public`: Find public attributes.

    `own`: Find attributes that are not inherited from parent classes.

    These filters **can be chained!** Order does **NOT** matter.

    For example, use `pdir(obj).public.own.methods` to find all public own methods.

    You can also call `search` on the returned results.

    See a [complete example](https://github.com/laike9m/pdir2/wiki/Attribute-Filtering).

## Install

### Generic

    pip install pdir2

About the name. I wanted to call it "pdir", but there's already one with this
name on pypi. Mine is better, of course.

### Fedora

    dnf install python3-pdir2
    --or--
    dnf install python2-pdir2

## Automatic Import

As a better alternative of `dir()`, it's more convenient to automatically import
pdir2 when launching REPL. Luckily, Python provides a way to do this. In you `.bashrc`(or `.zshrc`), add this line:

    export PYTHONSTARTUP=$HOME/.pythonstartup

Then, create `.pythonstartup` in your home folder. Add one line:

    import pdir

Next time you launch REPL, `pdir()` is already there, Hooray!

## Development

1. Set up development environment

   - **PDM**: pdir2 uses [PDM](https://pdm.fming.dev/latest/) to manage dependencies, so you want to make sure it's installed.
   - **pyenv**: Since you need to test pdir2 on multiple Python versions, [pyenv](https://github.com/pyenv/pyenv) is highly recommended.

2. Install dev dependencies

   Simply run `pdm install`.

   If you want to work on a specific Python version, run `pdm use [PYTHON_VERSION]` first to switch PDM to that version (e.g. `pdm use 3.9` if you want to debug a Python 3.9 specific issue).


3. Run tests

   Run `pdm run tox`

The guide may be incomplete. Please file bugs if you encounter any issues.
