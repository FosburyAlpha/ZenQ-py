from setuptools import setup, find_packages
setup(
    name='zenqapi',
    version='0.11',
    author="Fosbury Alpha Team",
author_email="fosbury.alpha@gmail.com",
description="ZenQ exchange python client.",
    packages=find_packages(),
    install_requires=['requests'],
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
python_requires=">=3.6",
)
