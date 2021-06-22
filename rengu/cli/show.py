import click
from click.core import Context

from rengu.cli.common import *


@click.command()
@click.pass_context
@output_option
@input_option
@query_string_arguments
def show(ctx: Context, output: str, input: str, query: list[str]):
    """Show matching rengu objects"""

    out = output_handler(output)
    store = storage_handler(ctx.obj["baseuri"])

    q = store.query(query, with_data=True)
    for x in q:
        out(x)

    if ctx.obj["verbose"]:
        print(q)
