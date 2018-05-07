from distutils.core import setup, Extension

setup(ext_modules=[Extension("expand", ["expand.c"])])

