# -*- coding: utf-8 -*-


from sys import stdout, stderr
from io import TextIOBase
from uuid import UUID
from unicodedata import normalize

from rengu.io import RenguOutput, RenguInput


ESC = str.maketrans(
    {
        "\\": r"\\",
        '"': r"\"",
        "\n": r"\n",
        "\r": r"\r",
        "\t": r"\t",
    }
)


class RenguOutputKv(RenguOutput):
    def __init__(self, arg: str, fd: TextIOBase = stdout):

        super().__init__(arg=arg, fd=fd)

        self.count = 0

    def __call__(self, obj: [UUID, dict]):

        # special case of UUID only
        if isinstance(obj, UUID):
            print(f"ID={obj}\n", file=self.fd, flush=True)
            return

        # Deep Recurse
        def _deep(prefix, obj):

            if isinstance(obj, dict):
                print(f"{prefix} = {{}};", file=self.fd, flush=True)
                for k in obj:
                    _deep(prefix + "." + k, obj[k])

            elif isinstance(obj, list):
                print(f"{prefix} = [];", file=self.fd, flush=True)
                for i, v in enumerate(obj):
                    _deep(prefix + "[" + str(i) + "]", v)

            elif isinstance(obj, (str, int, float)):
                # s = normalize("NFKD", str(obj).translate(ESC))
                s = str(obj).translate(ESC)
                print(f'{prefix} = "{s}";', file=self.fd, flush=True)

            else:
                print(f"UNKNOWN {prefix} with { type(obj) };", file=stderr)

        start_prefix = f"[{self.count}]"

        _deep(start_prefix, obj)

        self.count += 1


class RenguInputKv(RenguInput):
    pass
