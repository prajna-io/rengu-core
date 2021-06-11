# -*- coding: utf-8 -*-


from sys import stdout
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
    }
)


class RenguOutputKv(RenguOutput):
    def __init__(self, args: str, fd: TextIOBase = stdout):

        self.args = args
        self.fd = fd

        self.count = 0
        self.extra = []

        more_args = args.split(":", 1)
        if len(more_args) == 2:
            self.extra = more_args[1].split(",")

    def __call__(self, obj: [UUID, dict]):

        # special case of UUID only
        if isinstance(obj, UUID):
            print(f"ID={obj}\n", file=self.fd)
            return

        # Deep Recurse
        def _deep(prefix, obj):

            if isinstance(obj, dict):
                print(f"{prefix} = {{}};")
                for k in obj:
                    _deep(prefix + "." + k, obj[k])

            elif isinstance(obj, list):
                print(f"{prefix} = [];")
                for i, v in enumerate(obj):
                    _deep(prefix + "[" + str(i) + "]", v)

            elif isinstance(obj, (str, int, float)):
                # s = normalize("NFKD", str(obj).translate(ESC))
                s = str(obj).translate(ESC)
                print(f'{prefix} = "{s}";')

            else:
                print(f"UNKNOWN {prefix}={obj};")

        start_prefix = f"[{self.count}]"

        _deep(start_prefix, obj)

        self.count += 1


class RenguInputKv(RenguInput):
    pass
