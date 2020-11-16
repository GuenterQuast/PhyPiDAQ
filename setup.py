"""
Setup script for the phypidaq module.

This setup includes the test runner for the module and the setup class for
package information
"""
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
import phypidaq  # from this directory


class PyTest(TestCommand):
    """
    Test runner for the phypidaq module

    For more info visit: https://pytest.org/latest/goodpractices.html
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.pytest_args)
        sys.exit(errcode)

setup(
    name='phypidaq',
    version=phypidaq.__version__,
    author='Guenter Quast',
    author_email='Guenter.Quast@online.de',
    packages=['phypidaq'],
    package_data={'phypidaq': ['PhyPiDemoData.csv']},
    scripts=[],
    classifiers=[
    'Development Status :: 5 - stable',
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    ],
    url='http://www.ekp.kit.edu/~quast/',
    license='MIT BSD 2-Clause',
    description='Data AcQuisition and analysis for Physics education with Raspberry Pi',
    long_description=open('README.md').read(),
    setup_requires=[\
        "NumPy >= 1.13.3",
        "SciPy >= 0.18.1",
        "matplotlib >= 2.0.0",]
)
