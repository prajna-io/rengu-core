from setuptools import setup, find_packages

from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))

with open(path.join(PROJECT_ROOT, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

requires_extra = {
    "dev": ["GitPython", "pylint", "black"],
}
requires_extra["all"] = [m for v in requires_extra.values() for m in v]

setup(
    name="rengu-core",
    version="1.0",
    description="Library and tools for managing content fragments with metadata",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://prajna.io",
    author="Thornton K. Prime",
    author_email="thornton.prime@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        "Click",
        "click-shell",
        "dpath",
        "splitstream",
        "toolz",
        "titlecase",
        "ruamel.yaml",
    ],
    extras_require=requires_extra,
    entry_points={
        "console_scripts": [
            "rengux=rengu.cli:cli",
        ],
        "rengu_cli": [],
        "rengu_store": [],
        "rengu_map": [],
        "rengu_input": [],
        "rengu_output": [],
    },
)
