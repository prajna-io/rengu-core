from pkg_resources import iter_entry_points

import click


class ChoiceWithParam(click.Choice):
    """A click Choice that allows passing aditional information after the
        parameter name with a colon.

    Args:
        click ([type]): [Click]
    """

    def convert(self, value: str, param: str, ctx: click.Context) -> str:
        """[summary]

        Args:
            value (str): The value passed
            param (str): The parameter passed
            ctx (click.Context): The click context

        Returns:
            str: The matched value
        """
        normed_value = value.split(":", 1)[0]
        normed_choices = {choice: choice for choice in self.choices}

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
            ctx,
        )


# Rengu data storage option
storage_option = click.option(
    "-B",
    "--base",
    "baseuri",
    help="URI to Rengu data Base",
    envvar="RENGU_BASE",
    type=ChoiceWithParam([x.name for x in iter_entry_points("rengu_store")]),
)

# output handler option
output_option = click.option(
    "-o",
    "--output",
    default="list",
    help="Output format",
    type=ChoiceWithParam([x.name for x in iter_entry_points("rengu_output")]),
)

# Input handler option
input_option = click.option(
    "-i",
    "--input",
    default="json",
    help="Input format",
    type=ChoiceWithParam([x.name for x in iter_entry_points("rengu_input")]),
)

# Query string arguments
# this is used for all CLI functions that run queries
query_string_arguments = click.argument("query", nargs=-1, required=True, type=str)


def storage_handler(name: str):
    """[summary]

    Args:
        name (str): The name of the handler

    Raises:
        ModuleNotFoundError: If no matching module can be found in entry points

    Returns:
        RenguStorage: A rengu storage object
    """
    proto = name.split(":", 1)[0]

    for entry in iter_entry_points("rengu_store"):
        if entry.name == proto:
            return entry.load()(name, entry.extras)

    raise ModuleNotFoundError(f"No loadable module for {name}")


def output_handler(name: str):
    """Get a rengu output handler

    Args:
        name (str): name of the handler

    Raises:
        ModuleNotFoundError: If no matching module can be found in entry points

    Returns:
        RenguOutput: an output handler
    """

    hand = name.split(":", 1)[0]

    for entry in iter_entry_points("rengu_output"):
        if entry.name == hand:
            return entry.load()(arg=name)

    raise ModuleNotFoundError(f"No loadable module for {name}")
