import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
CHANGELOG = (HERE / "CHANGELOG.md").read_text()

# This call to setup() does all the work
setup(
    name="alma-client",
    version="3.0.2",
    description="Python API client for the Alma Installments API",
    long_description=f"{README}\n\n{CHANGELOG}",
    long_description_content_type="text/markdown",
    url="https://github.com/alma/alma-python-client",
    author="Alma",
    author_email="contact@getalma.eu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["httpx"],
)
