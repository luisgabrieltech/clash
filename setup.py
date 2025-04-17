from setuptools import setup, find_packages

setup(
    name="clash-analytics",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pymongo",
        "python-dotenv",
        "requests",
        "flask"
    ]
) 