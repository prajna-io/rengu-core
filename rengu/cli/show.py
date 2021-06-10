
from rengu import cli

@cli.command()
def show(env: Environment):

    print("SHOW")
    print(f"Verbose: {env.verbose}")
    print(f"BaseURI: {env.base}")