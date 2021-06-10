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


output_option = click.option(
    "-o",
    "--output",
    default="list",
    help="Output format",
    type=ChoiceWithParam([x.name for x in iter_entry_points("rengu_output")]),
)
input_option = click.option(
    "-i",
    "--input",
    default="json",
    help="Input format",
    type=ChoiceWithParam([x.name for x in iter_entry_points("rengu_input")]),
)
