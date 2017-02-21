# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    #package_data = {'project': ['strains.xml']},
    #include_package_data = True,
    entry_points = {'scrapy': ['settings = test1.settings']},
)
