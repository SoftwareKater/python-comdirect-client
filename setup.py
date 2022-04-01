from setuptools import setup

setup(
    name='python-comdirect-client',
    version='0.1.0',
    py_modules=['src'],
    install_requires=[
        'appdirs',
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'pcc = src.cli:cli',
        ],
    },
)
