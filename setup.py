from setuptools import find_packages
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print "warning: pypandoc module not found, could not convert Markdown to RST"
    read_md = lambda f: open(f, 'r').read()
requires = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="wikidict",
    version="0.0.0",
    description="",
    long_description=read_md('README.md'),
    author="Walid Saad",
    author_email="walid.sa3d@gmail.com",
    url="https://github.com/walidsa3d/wikidict",
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=requires,
    test_suite="tests",
    license="mit",
    zip_safe=False,
    classifiers=(
    )
)
