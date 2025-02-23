import click
from .exec import exec
from .kernel import kernel


@click.group()
@click.version_option()
def root():
    """A thing to help the Helix text editor connect to a Jupyter kernel."""
    pass


root.add_command(exec)
root.add_command(kernel)


def run():
    root()
