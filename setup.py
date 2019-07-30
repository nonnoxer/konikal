from setuptools import setup, find_packages

setup(
    name='konikal',
    version='0.0.1',
    packages=find_packages(exclude=["files*"]),
    license='MIT',
    description='A website generator using Flask',
    long_description=open('README.md').read(),
    install_requires=['flask'],
    url='https://github.com/nonnoxer/konikal',
    author='Natanael Tan',
    author_email='nonnoxer@gmail.com'
)
