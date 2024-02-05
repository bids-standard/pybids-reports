"""General parser for the cohort_creator package."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import IO, Sequence

import rich
from bids.layout import BIDSLayout

from bids.ext.reports import BIDSReport
from bids.ext.reports._version import __version__
from bids.ext.reports.logger import pybids_reports_logger

# from bids.reports import BIDSReport
LOGGER = pybids_reports_logger()


def _path_exists(path, parser):
    """Ensure a given path exists."""
    if path is None or not Path(path).exists():
        raise parser.error(f"Path does not exist: <{path}>.")

    return Path(path).absolute()


class MuhParser(argparse.ArgumentParser):
    def _print_message(self, message: str, file: IO[str] | None = None) -> None:
        rich.print(message, file=file)


def base_parser() -> MuhParser:
    from functools import partial

    parser = MuhParser(
        prog="pybids_reports",
        description="Report generator for BIDS datasets.",
        epilog="""
        For a more readable version of this help section,
        see the online doc https://cohort-creator.readthedocs.io/en/latest/
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    PathExists = partial(_path_exists, parser=parser)

    parser.add_argument(
        "bids_dir",
        action="store",
        type=PathExists,
        help="Path to BIDS dataset.",
    )
    parser.add_argument(
        "output_dir",
        action="store",
        type=Path,
        help="Output path.",
    )
    parser.add_argument(
        "--participant_label",
        help="""\
The label(s) of the participant(s) that should be used for the report.
The label corresponds to sub-<participant_label> from the BIDS spec
(so it does not include "sub-").

If this parameter is not provided, The first subject will be used.
Multiple participants can be specified with a space separated list.
        """,
        nargs="+",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__version__}",
    )
    parser.add_argument(
        "--verbosity",
        required=False,
        choices=[0, 1, 2, 3],
        default=2,
        type=int,
        nargs=1,
        help="Verbosity level.",
    )
    return parser


def set_verbosity(verbosity: int | list[int]) -> None:
    if isinstance(verbosity, list):
        verbosity = verbosity[0]

    if verbosity == 0:
        LOGGER.setLevel("ERROR")
    elif verbosity == 1:
        LOGGER.setLevel("WARNING")
    elif verbosity == 2:
        LOGGER.setLevel("INFO")
    elif verbosity == 3:
        LOGGER.setLevel("DEBUG")


def cli(args: Sequence[str] = None, namespace=None) -> None:
    """Entry point."""
    parser = base_parser()
    opts = parser.parse_args(args, namespace)

    bids_dir = opts.bids_dir.absolute()
    output_dir = opts.output_dir.absolute()
    participant_label = opts.participant_label or None

    set_verbosity(opts.verbosity)

    LOGGER.debug(bids_dir)

    layout = BIDSLayout(bids_dir)

    report = BIDSReport(layout)
    if participant_label:
        counter = report.generate(subject=participant_label)
    else:
        counter = report.generate()

    common_patterns = counter.most_common()
    if not common_patterns:
        LOGGER.warning("No common patterns found.")
    else:
        with open(output_dir / "report.txt", "w") as f:
            f.write(str(counter.most_common()[0][0]))
