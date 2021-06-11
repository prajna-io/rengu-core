import sys

import re
from fnmatch import fnmatchcase
from uuid import UUID
from collections.abc import Set
from json import loads

import lmdb

from rengu.store import RenguStore


# Regex matches
RE_GLOB = re.compile(r"[\*\?\[]")


class RenguStoreLmdbRo(RenguStore):
    def __init__(self, name: str, extra: list[str]):

        path = name.split(":", 1)[1]

        self.db = lmdb.open(path, max_dbs=4, map_size=2 ** 40 - 1)

        self.index_db = self.db.open_db("index".encode(), dupsort=True)
        self.data_db = self.db.open_db("data".encode())

    class ResultSet(Set):
        def __init__(
            self,
            term: str,
            parent: "RenguStoreLmdbro",
            txn: lmdb.Transaction,
            result: "ResultSet" = None,
        ):

            self.parent = parent
            self.term = term
            self.seen = set()
            self.seen_all = False
            self.seen_pos = 0
            self.txn = txn

            if result:
                self.seen_all = True
                self.seen = set(result)
                self.cursor = None
                return

            # Set the defaul start for the cursor
            self.start = self.term

            # If there is a glob, start at the glob beginning
            self.glob = False
            if m := RE_GLOB.search(self.term):
                self.glob = True
                self.start = self.start[: m.start()]

            # Get the cursor and set the range
            self.cursor = txn.cursor(self.parent.index_db)

            # If the range isn't in the DB, then we've seen all
            # and it is an empty set
            if not self.cursor.set_range(self.start.encode()):
                print("Not in DB")
                self.seen_all = True
                self.cursor.close()

        def __iter__(self):

            if self.seen_all:
                self.seen_pos = 0
            else:
                if not self.cursor.set_range(self.start.encode()):
                    print("Not in DB")
                    self.seen_all = True
                    self.cursor.close()

            return self

        def __next__(self):

            if self.seen_all:

                if self.seen_pos >= len(self.seen):
                    raise StopIteration

                self.seen_pos += 1
                return list(self.seen)[self.seen_pos - 1]

            else:

                while key := self.cursor.key().decode():

                    if self.glob:

                        # Stop iteration of the start doesn't match
                        if not key[: len(self.start)] == self.start:
                            self.seen_all = True
                            raise StopIteration

                        # Skip if this doesn't match the glob
                        if not fnmatchcase(key, self.term):
                            self.cursor.next()
                            continue

                    # break if not a glob and prefix doesn't match
                    elif not key == self.start:
                        self.seen_all = True
                        raise StopIteration

                    # All other cases, get the UUID
                    try:
                        u = UUID(bytes=self.cursor.value())
                    except ValueError:
                        self.cursor.next()
                        continue

                    # Skip seen values
                    if u in self.seen:
                        print(f"Seen {u} for {key}")
                        self.cursor.next()
                        continue

                    # add to seen and yield
                    else:
                        self.seen.add(u)
                        self.cursor.next()
                        return u

            self.seen_all = True
            raise StopIteration

        def __contains__(self, i):

            # Shortcut for seen all
            if self.seen_all:
                return i in self.seen

            # iterate through the list
            for j in self:
                if i in j:
                    return True

            return False

        def __len__(self):

            # Shortcut for seen all
            if self.seen_all:
                return len(self.seen)

            return len(set(self))

        def __repr__(self):

            return f"{self.term}[n={len(self)}]"

        def __and__(self, other):
            _ = len(self) > len(other)
            return RenguStoreLmdbRo.ResultSet(
                f"( {self} & {other} )",
                self.parent,
                self.txn,
                result=self.seen & other.seen,
            )

        def __sub__(self, other):
            _ = len(self) > len(other)
            return RenguStoreLmdbRo.ResultSet(
                f"( {self} - {other} )",
                self.parent,
                self.txn,
                result=self.seen - other.seen,
            )

        def __or__(self, other):
            _ = len(self) > len(other)
            return RenguStoreLmdbRo.ResultSet(
                f"( {self} | {other} )",
                self.parent,
                self.txn,
                result=self.seen | other.seen,
            )

        def __xor__(self, other):
            _ = len(self) > len(other)
            return RenguStoreLmdbRo.ResultSet(
                f"( {self} ^ {other} )",
                self.parent,
                self.txn,
                result=self.seen ^ other.seen,
            )

    def get(self, id: UUID):
        """Get detail for the specified id"""

        txn = self.db.begin()
        cursor = txn.cursor(self.data_db)

        return loads(cursor.get(id.bytes).decode())

    def query(
        self, args: list[str], default_operator: str = "&", with_data: bool = False
    ):

        txn = self.db.begin()

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
                        raise Error("Invalid subquery - unmatched )")
                    return result

                # standard resultset
                else:
                    r = self.ResultSet(q, self, txn)

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
                    raise Error("No operator specified")

                current_operator = default_operator

            return result

        if with_data:
            yield from [self.get(i) for i in _parse()]
        else:
            yield from _parse()


class RenguStoreLmdbRw(RenguStoreLmdbRo):
    pass
