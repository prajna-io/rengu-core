from sys import stdout
from io import TextIOBase
from uuid import UUID
from json import dump

from rengu.io import RenguOutput, RenguInput


class RenguInputJson:
    pass


class RenguOutputJson(RenguOutput):
    def __init__(self, arg: str, fd: TextIOBase = stdout):

        super().__init__(arg=arg, fd=fd)

    def __call__(self, obj: [UUID, dict]):

        dump(obj, self.fd)
        print("", file=self.fd, flush=True)
