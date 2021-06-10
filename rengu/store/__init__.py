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

    def query(
        self,
        queryterms: list[str],
        default_operator: str = "&",
        result: "RenguStore.ResultSet" = None,
    ):
        """[summary]

        Args:
            queryterms (str[]): An array of query terms
            default_operator (str, optional): The default operator for the query. Defaults to "&".

        Raises:
            RenguStorageError: Cannot parse the query

        Returns:
            ResultSet: The resulting set of matching values
        """

        # last term is None
        queryterms.append(None)

        def _parse(depth: int = 0):

            current_operator = None
            result = None

            while q := queryterms.pop(0):

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
                    r = ResultSet(self, q)

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

    class ResultSet(Set):
        def __init__(self, rengu_store, term: str, result: list[str] = None):
            pass

        def __iter__(self):
            raise RenguStorageError(f"__iter__ is not implemented in {__class__}")

        def __next__(self):
            raise RenguStorageError(f"__next__ is not implemented in {__class__}")
