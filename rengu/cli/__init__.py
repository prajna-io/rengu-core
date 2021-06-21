# -*- coding: utf-8 -*-

from pkg_resources import iter_entry_points

import click
from click.core import Context
from click_plugins import with_plugins

from rengu.cli.common import ChoiceWithParam, storage_option


@with_plugins(iter_entry_points("rengu_cli"))
@click.group()
@click.help_option("-h", "--help")
@click.pass_context
@click.option(
    "--verbose",
    "-v",
    default=0,
    count=True,
    help="Verbosity level [0=no messages, 3=all messages]",
    envvar="VERBOSE",
)
@storage_option
def cli(ctx, verbose: int, baseuri: str):
    """A command line tool for Rengu home management"""

    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["baseuri"] = baseuri


@cli.command()
@click.pass_context
def info(ctx: Context):
    """Show basic information about Rengu environment"""

    if ctx.obj["verbose"]:
        print(f"VERBOSE={ctx.obj['verbose']}")

    print(f"RENGU_BASE={ctx.obj['baseuri']}")
