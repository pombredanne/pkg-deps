from setuptools import setup, find_packages
import sys


tests_require = ['virtualenv']

if sys.version_info < (3, 2):
    tests_require.append('subprocess32')

setup(
    name="pkg-deps",
    version="0.5",
    packages=find_packages(),
    install_requires=['pydot3k', 'networkx', 'click'],
    tests_require=tests_require,
    # entry_points based script is really slow (0.5 seconds)
    # might want to switch to normal script, since windows
    # version isn't a concern right now
    entry_points={
        'console_scripts': [
            'pkg_deps = pkg_deps.main:main',
        ],
    },
    test_suite='tests.tests',
    zip_safe=False,
)
