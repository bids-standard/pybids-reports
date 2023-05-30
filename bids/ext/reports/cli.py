"""General parser for the cohort_creator package."""
from __future__ import annotations

import argparse
import sys
from typing import IO, Sequence
from pathlib import Path

import rich

from ._version import __version__


from bids.layout import BIDSLayout

# from bids.reports import BIDSReport

from reports import BIDSReport


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
    return parser


def cli(argv: Sequence[str] = sys.argv) -> None:
    """Entry point."""
    parser = base_parser()

    args, unknowns = parser.parse_known_args(argv[1:])

    bids_dir = Path(args.bids_dir[0]).resolve()
    # output_dir = Path(args.output_dir)
    # participant_label = Path(args.participant_label)

    layout = BIDSLayout(bids_dir)

    report = BIDSReport(layout)
    # descriptions =
    report.generate()
