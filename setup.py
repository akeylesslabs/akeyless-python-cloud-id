from setuptools import find_packages, setup  # noqa: H301

NAME = "akeyless-cloud-id"
VERSION = "0.1.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="AKEYLESS Cloud Id retriever",
    author="Dmitry Gorochovsky",
    author_email="dgoro@akeyless.io",
    url="https://www.akeyless.io/",
    keywords=["AKEYLESS Cloud ID"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache 2.0",
    long_description="""\
    Akeyless cloud id retriever  # noqa: E501
    """
)
