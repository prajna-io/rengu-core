# -*- coding: utf-8 -*-

from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins

class Environment(object):
    def __init__(self):
        self.verbose = False

    def log(self, msg: str, *args: str):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=click.get_text_stream("stderr"))

    def vlog(self, msg: str, *args: str):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


class ChoiceWithParam(click.Choice):
    """A choice type that allows a parameter to be passed after the choice name after a colon(:)"""

    def convert(self, value: str, param: str, env: click.Context):
        # Match through normalization and case sensitivity
        # first do token_normalize_func, then lowercase
        # preserve original `value` to produce an accurate message in
        # `self.fail`
        normed_value = value.split(":", 1)[0]
        normed_choices = {choice: choice for choice in self.choices}

        if env is not None and env.token_normalize_func is not None:
            normed_value = env.token_normalize_func(value)
            normed_choices = {
                env.token_normalize_func(normed_choice): original
                for normed_choice, original in normed_choices.items()
            }

        if not self.case_sensitive:
            lower = str.casefold

            normed_value = lower(normed_value)
            normed_choices = {
                lower(normed_choice): original
                for normed_choice, original in normed_choices.items()
            }

        if normed_value in normed_choices:
            return value

        self.fail(
            "invalid choice: %s. (choose from %s)" % (value, ", ".join(self.choices)),
            param,
            env,
        )


pass_environment = click.make_pass_decorator(Environment, ensure=True)

@with_plugins(iter_entry_points('rengu_cli'))
@click.group()
@click.help_option("-h", "--help")
@click.option(
    "--verbose",
    "-v",
    default=0,
    count=True,
    help="Verbosity level [0=no messages, 3=all messages]",
    envvar="VERBOSE",
)
@click.option(
    "-B", "--base", "baseuri", help="URI to Rengu data Base", envvar="RENGU_BASE"
)
@pass_environment
def cli(
    env: Environment, verbose: int, baseuri: str, engineid: str, nlpid: str, bindir: str
):
    """A command line tool for Rengu home management"""

    env.verbose = verbose
    env.base = baseuri

@cli.command()
def info(env: Environment):

    print(f"Verbose: {env.verbose}")
    print(f"BaseURI: {env.base}")

