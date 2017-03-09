import codecs
from setuptools import setup

readme = codecs.open('README.rst', encoding='utf-8').read()

setup(
    name='pdir2',
    version='0.0.1.post2',
    description='Pretty dir printing with joy',
    long_description=readme,
    author='laike9m',
    author_email='laike9m@gmail.com',
    url='http://github.com/laike9m/pdir2',
    packages=[
        'pdir',
    ],
    install_requires=[
        'colorama',
        'enum34;python_version<"3.4"',
    ],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ], )
