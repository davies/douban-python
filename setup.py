from setuptools import setup, find_packages

setup(
        name = 'douban-python',
        version = '0.1',
        description = "Python client library for Douban APIs",
        license = "Apache 2.0",
        url = "http://www.douban.com/service/api/",
        install_requires = ['setuptools', 'gdata'],
        tests_requires = ['nose'],
        packages = find_packages(),
        test_suite = 'nose.collector',
)
