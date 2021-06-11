from sys import stdout
from io import TextIOBase
from uuid import UUID

from rengu.io import RenguOutput


class RenguOutputList(RenguOutput):
    def __init__(self, args: str, fd: TextIOBase = stdout):

        self.args = args
        self.fd = fd

    def __call__(self, obj: [UUID, dict]):

        if isinstance(obj, UUID):
            print(obj, file=self.fd)
        elif isinstance(obj, dict):
            print(obj.get("ID", ""))
        else:
            print(obj, file=self.fd)
