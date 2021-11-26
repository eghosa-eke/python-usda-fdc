from setuptools import setup, find_packages


def read_requirements(filename):
    return [req.strip() for req in open(filename)]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyUsda',
    version=open('VERSION').read().strip(),
    author='Eghosa Eke',
    author_email='eghosaeke@gmail.com',
    packages=find_packages(
        exclude=["tests"]),
    package_data={
        '': ['*.md', 'LICENSE', 'README'],
    },
    install_requires=read_requirements('requirements.txt'),
    license='GNU General Public License 3',
    description="Interface for accessing USDA's FDC API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="api usda fdc nutrition food",
    url="https://github.com/eghosa-eke/python-usda-fdc",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    project_urls={
        "Source Code": "https://github.com/eghosa-eke/python-usda-fdc",
    }
)