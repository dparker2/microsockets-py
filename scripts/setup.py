import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="microsockets",
    version="1.0.0",
    author="David Parker",
    description="ASGI Websocket server made with simplicity in mind.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ParkerD559/microsockets-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
