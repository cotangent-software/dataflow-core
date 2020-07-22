import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataflow-core-ctrekker",
    version="0.0.1",
    author="Connor Burns",
    author_email="ctrekker4@gmail.com",
    description="A modular graph-based approach to backend implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ctrekker/dataflow-core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
