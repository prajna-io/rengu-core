import click
from click.core import Context

from rengu.cli.common import *


@click.command()
@click.pass_context
@output_option
@input_option
def load(ctx: Context, output: str, input: str):
    """Show matching rengu objects"""

    print("SHOW")
    print(f"Verbose: {ctx.obj['verbose']}")
    print(f"BaseURI: {ctx.obj['baseuri']}")
