from sys import stdout
from io import TextIOBase
from uuid import UUID

from rengu.io import RenguOutput


class RenguOutputList(RenguOutput):
    def __init__(self, name: str, extra: str, fd: TextIOBase = stdout):

        self.name = name
        self.extra = extra
        self.fd = fd

    def __call__(self, obj: [UUID, dict]):

        if isinstance(obj, UUID):
            print(obj, file=self.fd)
        elif isinstance(obj, dict):
            print(obj.get("ID", ""), file=self.fd)
        else:
            print(obj, file=self.fd)
