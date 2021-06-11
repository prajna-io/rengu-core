from sys import stdout
from io import TextIOBase
from uuid import UUID
from json import dumps

from rengu.io import RenguOutput, RenguInput


class RenguInputJson:
    pass


class RenguOutputJson(RenguOutput):
    def __init__(self, args: str, fd: TextIOBase = stdout):

        self.args = args
        self.fd = fd

    def __call__(self, obj: [UUID, dict]):

        print(dumps(obj))
