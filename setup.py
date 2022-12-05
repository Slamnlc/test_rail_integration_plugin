import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pytest-testrail-api-client',
    version='1.0',
    use_scm_version=False,
    description='TestRail Api Python Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Biriukov Maksym',
    author_email='maksym.biriukov@eleks.com',
    url="https://gitlab2.eleks-software.local/python/test_rail_integration_plugin",
    download_url='https://gitlab2.eleks-software.local/python/test_rail_integration_plugin/-/archive/v1.0.1/test_rail_integration_plugin-v1.0.1.tar.gz',
    packages=setuptools.find_packages(exclude=("tests", "dev_tools")),
    install_requires=[
        'requests',
        'pytest',
    ],
    entry_points={
        "pytest11": [
            "pytest-testrail-api-client = test_rail.plugin",
        ],
        "testrail_api": [
            "test_rail_client = test_rail.rail_client"
        ]
    },
)
