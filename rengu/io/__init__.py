from io import TextIOBase


class RenguOutputError(Exception):
    pass


class RenguOutput:
    def __init__(self, args: str, fd: TextIOBase):

        self.args = args

        raise RenguOutputError(f"Unimplemented output handler {__class__} for {args}")


class RenguInput:
    pass
