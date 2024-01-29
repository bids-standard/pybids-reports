"""General parser for the cohort_creator package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import IO
from typing import Sequence

import rich

from ._version import __version__
from .logger import pybids_reports_logger
from bids.ext.reports import BIDSReport
from bids.layout import BIDSLayout

# from bids.reports import BIDSReport
LOGGER = pybids_reports_logger()


class MuhParser(argparse.ArgumentParser):
    def _print_message(self, message: str, file: IO[str] | None = None) -> None:
        rich.print(message, file=file)


def base_parser() -> MuhParser:
    parser = MuhParser(
        prog="pybids_reports",
        description="Report generator for BIDS datasets.",
        epilog="""
        For a more readable version of this help section,
        see the online doc https://cohort-creator.readthedocs.io/en/latest/
        """,
    )
    parser.add_argument(
        "bids_dir",
        help="""
        Path to BIDS dataset.
        """,
        nargs=1,
    )
    parser.add_argument(
        "output_dir",
        help="""
        Output path.
        """,
        nargs=1,
    )
    parser.add_argument(
        "--participant_label",
        help="""
        The label(s) of the participant(s) that should be used for the report.
        The label corresponds to sub-<participant_label> from the BIDS spec
        (so it does not include "sub-").

        If this parameter is not provided, The first subject will be used.
        Multiple participants can be specified with a space separated list.
        """,
        nargs="+",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__version__}",
    )
    parser.add_argument(
        "--verbosity",
        help="""
        Verbosity level.
        """,
        required=False,
        choices=[0, 1, 2, 3],
        default=2,
        type=int,
        nargs=1,
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


def cli(argv: Sequence[str] = sys.argv) -> None:
    """Entry point."""
    parser = base_parser()

    args, unknowns = parser.parse_known_args(argv[1:])

    bids_dir = Path(args.bids_dir[0]).resolve()
    # output_dir = Path(args.output_dir[0])
    participant_label = args.participant_label or None

    set_verbosity(args.verbosity)

    LOGGER.debug(f"{bids_dir}")

    layout = BIDSLayout(bids_dir)

    report = BIDSReport(layout)
    if participant_label:
        report.generate(subject=participant_label)
    else:
        report.generate()
