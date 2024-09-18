from setuptools import find_packages
from setuptools import setup


version = "0.0.1"

setup(
    name='passerelle-imio-focus',
    version=version,
    author="iMio",
    author_email="support-ts@imio.be",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/IMIO/passerelle-imio-focus",
    install_requires=[
        'django>=3.2, <3.3',
    ],
    zip_safe=False,
)
