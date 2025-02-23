from helix_jupyter_thing import cli
from helix_jupyter_thing import state


def main():
    state.init()
    cli.run()
