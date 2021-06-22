# -*- coding: utf-8 -*-

from collections.abc import Set
from uuid import UUID


class RenguStorageError(Exception):
    pass


class RenguStore:
    """Base class defining Rengu storage objects."""

    def save(self, obj: dict) -> dict:
        raise RenguStorageError(f"Save is not implemented in {__class__}")

    def delete(self, id: UUID) -> UUID:
        raise RenguStorageError(f"Delete is not implemented in {__class__}")

    class ResultSet(Set):
        def __init__(self, rengu_store, term: str, result: list[str] = None):
            pass

        def __iter__(self):
            raise RenguStorageError(f"__iter__ is not implemented in {__class__}")

        def __next__(self):
            raise RenguStorageError(f"__next__ is not implemented in {__class__}")

    def query(
        self, args: list[str], default_operator: str = "&", with_data: bool = False
    ):

        # last term is None
        args = [*args]
        args.append(None)

        def _parse(depth=0):

            current_operator = None
            result = None

            while q := args.pop(0):

                r = None

                # Switch operator
                if q in "&-|^":
                    current_operator = q
                    continue

                # Nest query
                if q == "(":
                    r = _parse(depth=depth + 1)

                elif q == ")":
                    if depth < 1:
                        raise RenguStorageError("Invalid subquery - unmatched )")
                    return result

                # standard resultset
                else:
                    r = self.ResultSet(self, q)

                # Run the query operation
                if not current_operator:
                    result = r

                elif current_operator == "&":
                    result = result & r

                elif current_operator == "-":
                    result = result - r

                elif current_operator == "|":
                    result = result | r

                elif current_operator == "^":
                    result = result ^ r

                else:
                    raise RenguStorageError("No operator specified")

                current_operator = default_operator

            return result

        return _parse()
