from sys import stdout
from io import TextIOBase
from uuid import UUID
from json import dumps

from rengu.io import RenguOutput


class RenguInputJson:
    pass


class RenguOutputJson(RenguOutput):
    def __init__(self, name: str, extra: str, fd: TextIOBase = stdout):

        self.name = name
        self.extra = extra
        self.fd = fd

    def __call__(self, obj: [UUID, dict]):

        print(dumps(obj), file=self.fd)
