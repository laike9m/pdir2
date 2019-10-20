import codecs

from setuptools import setup

readme = codecs.open('README.md', encoding='utf-8').read()
history = codecs.open('HISTORY.md', encoding='utf-8').read()

setup(
    name='pdir2',
    version='0.3.2',
    description='Pretty dir printing with joy',
    long_description=u'\n\n'.join([readme, history]),
    long_description_content_type='text/markdown',
    author='laike9m',
    author_email='laike9m@gmail.com',
    url='http://github.com/laike9m/pdir2',
    packages=['pdir'],
    setup_requires=[
        # minimum version to use environment markers
        'setuptools>=20.6.8'
    ],
    install_requires=[
        'colorama;platform_system=="Windows"',
        'enum34;python_version<"3.4"',
    ],
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
    ],
)
