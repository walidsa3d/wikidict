from setuptools import find_packages
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print "warning: pypandoc module not found, could not convert Markdown to RST"
    read_md = lambda f: open(f, 'r').read()

setup(
    name="wikidict",
    version="1.0.0",
    description="Wikipedia at your fingertips",
    long_description=read_md('README.md'),
    author="Walid Saad",
    author_email="walid.sa3d@gmail.com",
    url="https://github.com/walidsa3d/wikidict",
    packages=find_packages(),
    include_package_data=True,
    test_suite="nose.collector",
    license="mit",
    zip_safe=False,
    entry_points={"console_scripts": ["wikidict=wikidict.wikidict:main"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities'
    ]
)
