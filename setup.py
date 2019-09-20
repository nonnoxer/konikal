from setuptools import setup, find_packages

setup(
    name="konikal",
    version="0.1.0",
    packages=find_packages(exclude=["app*"]),
    license="MIT",
    description="A content management system using Flask",
    long_description=open("README.md").read(),
    install_requires=["flask", "sqlalchemy"],
    url="https://github.com/nonnoxer/konikal",
    author="Natanael Tan",
    author_email="nonnoxer@gmail.com",
)
