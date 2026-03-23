#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def main():

    rc = 0
    prefixes = ["asl", "ds00", "eeg", "meg", "ieeg", "pet"]

    base_dir = Path("tools") / "bids-examples"
    output_dir = Path(__file__).parent

    for pre in prefixes:
        for path in base_dir.glob(f"{pre}*"):
            if not path.is_dir():
                continue

            if path.name == "bids-examples":
                continue

            print()
            print("running on dataset", path)

            (output_dir / path.name).mkdir(exist_ok=True)

            cmd = [
                "pybids_reports",
                str(path),
                str(output_dir / path.name),
                "--verbosity",
                "1",
            ]

            print(" ".join(cmd))

            result = subprocess.run(cmd)
            if result.returncode != 0:
                rc = result.returncode

    sys.exit(rc)


if __name__ == "__main__":
    main()
