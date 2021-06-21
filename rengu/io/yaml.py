# -*- coding: utf-8 -*-

from sys import stdout
from io import TextIOBase
from uuid import UUID

import ruamel.yaml


from rengu.io import RenguOutput, RenguInput

# https://gist.github.com/joshbode/569627ced3076931b02f

###############################################################################
# encoders and decoders

BAD_START = r" .!&*-:?{}[],#|>@`'\\" + '"'


def yaml_encode(text):

    if not text:
        return ""

    # text = text.replace(":", "：")

    if text[0] in BAD_START:
        text = "\\" + text

    return text


def yaml_decode(text):

    if not text:
        return ""

    if text[0] == "\\":
        text = text[1:]

    text = text.replace("：", ":")

    return text


class RenguOutputYaml(RenguOutput):
    def __init__(self, arg: str, fd: TextIOBase = stdout):

        super().__init__(arg=arg, fd=fd)

        self._yaml = ruamel.yaml.YAML()

        self._yaml.explicit_start = True
        self._yaml.explicit_end = False
        # self._yaml.default_style = "|"
        self._yaml.default_flow_style = False
        self._yaml.allow_unicode = True
        # self._yaml.line_break = "\n"
        self._yaml.width = 80
        self._yaml.indent(mapping=2, sequence=4, offset=2)

    def __call__(self, obj: [UUID, dict]):

        # special case of UUID only
        if isinstance(obj, UUID):
            self.fd.write(f"---\nID: {obj}\n")
            return

        # Check if Body is raw text
        if body := obj.get("Body"):
            self._yaml.dump({k: obj[k] for k in obj if k != "Body"}, self.fd)
            self.fd.write("---\n")
            self.fd.write(yaml_encode(body.strip()))
            self.fd.write("\n")

        else:
            self._yaml.dump(obj, self.fd)


class RenguInputYaml(RenguInput):
    pass
