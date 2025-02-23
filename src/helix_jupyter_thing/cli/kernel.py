import click
from helix_jupyter_thing.state import set_default_kernel
from helix_jupyter_thing.state import print_default_kernel


@click.command()
def get():
    """Get the default kernel id."""
    print_default_kernel()


@click.command("set")
@click.argument(
    "id_pattern",
    type=click.STRING,
    required=True,
)
def set_cmd(id_pattern):
    """Set the default kernel."""
    set_default_kernel(id_pattern)


@click.group("kernel")
def kernel():
    pass


kernel.add_command(get)
kernel.add_command(set_cmd)
