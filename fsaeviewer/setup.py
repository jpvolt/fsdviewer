import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fsd-viewer-jpvolt",
    version="0.0.7",
    author="João Voltani",
    author_email="jpvoltdeveloper@gmail.com",
    description="Simple 2d viewer for formula student driverless projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpvolt/fsdviewer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
