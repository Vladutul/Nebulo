from setuptools import setup, find_packages

setup(
    name="Nebulo",
    version="0.1.0",
    author="Ciurdea Vladut",
    author_email="ciurdeavladut@gmail.com",
    description="A fuzzy logic framework for modeling uncertainty and imprecision.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vladutul/Nebulo",
    packages=find_packages(where="nebulo"),
    package_dir={"": "nebulo"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)