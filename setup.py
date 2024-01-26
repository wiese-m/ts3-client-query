import pathlib

from setuptools import setup, find_packages

from ts3_client_query import get_version

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="ts3_client_query",
    version=get_version(),
    description="Python client for TS3 Client Query API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wiese-m/ts3-client-query",
    author="Marek Wiese",
    author_email="wiese.marek@gmail.com",
    packages=find_packages(),
    python_requires=">=3.10, <4",
    install_requires=[
        "telnetlib3"
    ],
)
