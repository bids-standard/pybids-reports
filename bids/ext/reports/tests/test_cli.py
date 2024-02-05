"""Tests for the command-line interface."""

from __future__ import annotations

import os

from bids.ext.reports import cli


def test_cli(testdataset, tmp_path_factory):
    """Run cli.cli()."""
    tempdir = tmp_path_factory.mktemp("test_cli")
    args = [
        testdataset,
        str(tempdir),
        "--verbosity",
        "0",
    ]

    cli.cli(args)
    assert os.path.isfile(os.path.join(tempdir, "report.txt")), os.listdir(tempdir)
