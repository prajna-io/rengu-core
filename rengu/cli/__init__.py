# -*- coding: utf-8 -*-

from pkg_resources import iter_entry_points

import click
from click.core import Context
from click_plugins import with_plugins

from rengu.cli.common import ChoiceWithParam


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
@click.option(
    "-B",
    "--base",
    "baseuri",
    help="URI to Rengu data Base",
    envvar="RENGU_BASE",
    type=ChoiceWithParam([x.name for x in iter_entry_points("rengu_store")]),
)
def cli(ctx, verbose: int, baseuri: str):
    """A command line tool for Rengu home management"""

    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["baseuri"] = baseuri


@cli.command()
@click.pass_context
def info(ctx: Context):
    """Show basic information about Rengu environment"""

    print(type(ctx))
    print(f"Verbose: {ctx.obj['verbose']}")
    print(f"BaseURI: {ctx.obj['baseuri']}")
