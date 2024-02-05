"""Tests for bids.reports.parsing."""

from __future__ import annotations

import json
from pathlib import Path

from bids.ext.reports import parsing, templates


def test_pet():
    with open(Path(__file__).parent / "data" / "sub-01_ses-01_pet.json") as f:
        metadata = json.load(f)

    desc_data = {**parsing.device_info(metadata), **metadata}
    templates.pet_info(desc_data)
