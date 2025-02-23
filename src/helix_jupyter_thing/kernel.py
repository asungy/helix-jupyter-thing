from helix_jupyter_thing.state import get_default_kernel
from pathlib import Path
import argparse
import datetime
import json
import jupyter_client
import os
import select
import sys
import time


def send_from_stdin(id_pattern=""):
    connection_file = None
    if id_pattern:
        try:
            connection_file = jupyter_client.find_connection_file(
                f"kernel-{id_pattern}*.json"
            )
        except:
            sys.stderr.write(f"Could not find connection file with pattern {id_pattern}")
            sys.exit(1)
    else:
        default_kernel = get_default_kernel()
        if not default_kernel:
            sys.stderr.write("No ID pattern or default kernel specified.")
            sys.exit(1)
        try:
            connection_file = jupyter_client.find_connection_file(Path(default_kernel).name)
        except:
            sys.stderr.write(f"Could not find connection file from default kernel [{Path(default_kernel).name}]")
            sys.exit(1)
    assert(type(connection_file) == str)

    ready, _, _ = select.select([sys.stdin], [], [], 0.1)
    input = None
    if ready:
        input = sys.stdin.read().strip()
    else:
        sys.stderr.write("No input provided.")
        sys.exit(1)

    connection_info = None
    with open(connection_file, "r") as f:
        connection_info = json.load(f)
    assert connection_info != None

    client = jupyter_client.BlockingKernelClient()
    client.load_connection_info(connection_info)
    client.start_channels()

    msg_id = client.execute(input)
    msg = client.get_iopub_msg()
    timeout_secs = 5
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout_secs:
            sys.stderr.write("Timeout reached. No response from kernel.")
            sys.exit(1)

        msg = client.get_iopub_msg(timeout=1)
        if msg:
            if msg["header"]["msg_type"] == "stream":  # Output from kernel
                print(msg["content"]["text"])
            elif (
                msg["header"]["msg_type"] == "status"
                and msg["content"]["execution_state"] == "idle"
            ):
                break  # Execution is complete
            # def serializer(obj):
            #     if isinstance(obj, datetime.datetime):
            #         return obj.isoformat()
            #     else:
            #         return obj
            # print(json.dumps(msg, default=serializer))
        else:
            continue

        
    client.stop_channels()
   
