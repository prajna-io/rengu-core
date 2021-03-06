from setuptools import setup, find_packages

from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))

with open(path.join(PROJECT_ROOT, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

requires_extra = {
    "dev": ["GitPython", "pylint", "black"],
    "core": [
        "dpath",
    ],
    "input": [
        "splitstream",
        "ruamel.yaml",
        "titlecase",
    ],
}
requires_extra["all"] = [m for v in requires_extra.values() for m in v]

setup(
    name="rengu",
    version="6.0",
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
    install_requires=["Click", "click_plugins"],
    extras_require=requires_extra,
    entry_points={
        "console_scripts": [
            "rengu=rengu.cli:cli",
        ],
        "rengu_cli": [
            "show = rengu.cli.show:show",
            "load = rengu.cli.load:load",
            "delete = rengu.cli.load:delete",
        ],
        "rengu_store": [],
        "rengu_map": [
            "pass = rengu.map.pass:RenguMapPass",
            "edit = rengu.map.edit:RenguMapEdit",
        ],
        "rengu_input": [
            "json = rengu.io.json:RenguInputJson",
            "yaml = rengu.io.yaml:RenguInputYaml",
            "kv = rengu.io.kv:RenguInputKv",
        ],
        "rengu_output": [
            "list = rengu.io.list:RenguOutputList",
            "json = rengu.io.json:RenguOutputJson",
            "yaml = rengu.io.yaml:RenguOutputYaml",
            "kv = rengu.io.kv:RenguOutputKv",
        ],
    },
)
