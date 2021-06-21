from io import TextIOBase
from uuid import UUID


class RenguOutputError(Exception):
    pass


class RenguOutput:
    """Base class for output"""

    def __init__(self, arg: str, fd: TextIOBase):
        """Create a output object

        Args:
            arg (str): [description]
            fd (TextIOBase): [description]
        """

        # common arguments
        self.arg = arg
        self.fd = fd

        # extended extra arguments
        self.extra = []
        more_args = arg.split(":", 1)
        if len(more_args) == 2:
            self.extra = more_args[1].split(",")

        for x in self.extra:
            if x.startswith("file="):
                fname = x.split("=")[1]
                self.fd = open(fname, "w")
                break

    def __call__(self, obj: [UUID, dict]):
        raise RenguOutputError(
            f"Unimplemented output handler {__class__} for {self.arg}"
        )


class RenguInput:
    """Base class for input"""

    def __init__(self, arg: str, fd: TextIOBase):

        self.arg = arg
        self.fd = fd

    def __call__(self, obj: [UUID, dict]):
        raise RenguOutputError(
            f"Unimplemented input handler {__class__} for {self.arg}"
        )
