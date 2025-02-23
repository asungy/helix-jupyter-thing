from pathlib import Path
import json
import jupyter_client
import os
import sys

# The default kernel connection file to connect to.
DEFAULT_KERNEL_KEY = "default-kernel"


def state_file():
    return (
        Path.home()
        .joinpath(".local")
        .joinpath("state")
        .joinpath("hjt")
        .joinpath("state.json")
    )


def init():
    config_path = state_file()
    dir = config_path.parent
    if not dir.exists():
        os.makedirs(dir)

    if not config_path.exists():
        with open(config_path, "w") as f:
            f.write("{}")


def get_default_kernel():
    with open(state_file(), "r") as f:
        default_kernel = None
        try:
            default_kernel = json.load(f)[DEFAULT_KERNEL_KEY]
        except:
            return None
        return default_kernel


def print_default_kernel():
    with open(state_file(), "r") as f:
        default_kernel = None
        try:
            default_kernel = json.load(f)[DEFAULT_KERNEL_KEY]
        except:
            sys.stderr.write("Default kernel is not defined.")
            sys.exit(1)

        assert default_kernel != None

        if Path(default_kernel).exists():
            sys.stdout.write(f"Default kernel: {default_kernel}")
        else:
            sys.stderr.write(f"Kernel [{Path(default_kernel).name}] does not exist.")
            sys.exit(1)


def set_default_kernel(id_pattern):
    connection_file = None
    try:
        connection_file = jupyter_client.find_connection_file(
            f"kernel-{id_pattern}*.json"
        )
    except:
        sys.stderr.write(f"Could not find kernel with ID pattern {id_pattern}")
        sys.exit(1)

    assert connection_file != None

    with open(state_file(), "r+") as f:
        state = json.load(f)
        state[DEFAULT_KERNEL_KEY] = str(connection_file)

        # Clear file contents
        f.seek(0)
        f.truncate(0)

        json.dump(state, f)
        sys.stdout.write(f"Set default kernel to {connection_file}")
