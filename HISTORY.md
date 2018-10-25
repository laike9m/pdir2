Release History
===============

0.3.1(2018-10-25)
-----------------
* Add support for `__slots__` (#44, #45)
* Seperate `@staticmethod` with other descriptors(#38, #42)
* Add `__post_init__` support

Special thanks to @liwt31 for his great contribution.

0.3.0(2018-02-10)
-----------------
* Add support for various filters (#37)

0.2.0(2017-04-04)
-----------------
* Add support for color customization. (#14)

0.1.0(2017-03-16)
------------------
* Add support for ipython, ptpython and bpython (#4)

0.0.2(2017-03-11)
---------

### API Changes (Backward-Compatible)

* Added a `case_sensitive` parameter into the `search` function (#5)

### Bugfixes
* Error calling pdir(pandas.DataFrame) (#1)
* Methods are now considered functions (#6)
