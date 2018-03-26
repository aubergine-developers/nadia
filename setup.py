"""Nadia: automatic generation of Marshmallow Schemas for OpenAPI 3 schemas."""

from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development']

LONG_DESCRIPTION = """Nadia is an automatic generator of marshmallow Schemas for your OpenAPI 3 schemas.

Currently Nadia supports schemas with the following types:

- integer, number
- string
- array
- object (including nested ones)

The required and nullable settings are also supported."""

setup(
    name='nadia',
    description=__doc__,
    use_scm_version=True,
    long_description=LONG_DESCRIPTION,
    platforms=["Linux", "Unix"],
    setup_requires=['setuptools_scm'],
    install_requires=['marshmallow', 'pyaml'],
    tests_require=['marshmallow', 'pyaml', 'ddt'],
    author='Konrad Jałowiecki <dexter2206@gmail.com>, Magdalena Nowak',
    author_email='dexter2206@gmail.com',
    packages=find_packages(exclude=["tests", "tests.*"]),
    keywords='openapi schema validation'
)
