from sys import stdout
from io import TextIOBase
from uuid import UUID

from rengu.io import RenguOutput


class RenguOutputList(RenguOutput):
    def __init__(self, arg: str, fd: TextIOBase = stdout):
        super().__init__(arg=arg, fd=fd)

    def __call__(self, obj: [UUID, dict]):

        if isinstance(obj, UUID):
            print(obj, file=self.fd, flush=True)
        elif isinstance(obj, dict):
            print(obj.get("ID", ""), file=self.fd, flush=True)
        else:
            print(obj, file=self.fd, flush=True)
