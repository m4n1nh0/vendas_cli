from setuptools import setup, find_packages

setup(
    name='vendas_cli',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'vendas_cli=vendas_cli.main:main',
        ],
    },
)
