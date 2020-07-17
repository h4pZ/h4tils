import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h4tils-h4pZ",
    version="0.0.1",
    author="h4pZ",
    author_email="h4pz@pm.me",
    description="Personal utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/h4pZ/h4tils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
