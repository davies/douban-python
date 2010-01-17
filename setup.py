from setuptools import setup, find_packages

setup(
        name = 'douban-python',
        version = '0.4.1',
        description = "Python client library for Douban APIs",
        license = "Apache 2.0",
        author = "Qiangning Hong",
        author_email = "hongqn@gmail.com",
        url = "http://code.google.com/p/douban-python/",
        install_requires = ['setuptools', 'gdata>=1.1.1'],
        tests_require = ['nose'],
        packages = find_packages(),
        #test_suite = 'nose.collector',
)
