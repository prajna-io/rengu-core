class RenguOutputError(Exception):
    pass


class RenguOutput:
    def __init__(self, name: str, extra: str):
        print(name, extra)
        raise RenguOutputError(f"Unimplemented output handler {__class__}")
