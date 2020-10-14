import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='scappamento',
    version='0.1a1',  # TODO: decide first version identifier
    author='Lorenzo Bunino',
    author_email="bunino.lorenzo@gmail.com",
    description="B2B automation for music stores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lorenzobunino/scappamento",
    packages=setuptools.find_packages(),  # TODO: find_packages vs hand-compiled list
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",  # TODO: fix path handling and
                                                     #  change "Microsoft :: Windows" to "OS Independent"
    ],
    python_requires='>=3.6'
)
