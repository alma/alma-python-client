import pathlib
from setuptools import setup

version = {}
with open("./alma/version.py") as fp:
    exec(fp.read(), version)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


# This call to setup() does all the work
setup(
    name="alma-python-client",
    version=version["__version__"],
    description="Python API client for the Alma Installments API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alma/alma-python-client",
    author="Alma",
    author_email="contact@getalma.eu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["alma"],
    include_package_data=True,
    install_requires=["requests"],
)
