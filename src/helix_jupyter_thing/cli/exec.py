import click
from helix_jupyter_thing import kernel


@click.command()
@click.option(
    "-i",
    "--id-pattern",
    "id_pattern",
    type=click.STRING,
    help="The first few characters of the kernel ID to connect to."
)
def exec(id_pattern):
    """Send code to kernel."""
    kernel.send_from_stdin(id_pattern)
