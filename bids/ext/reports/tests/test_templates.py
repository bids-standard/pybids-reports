"""Tests for bids.reports.parsing."""

from __future__ import annotations

import json
from pathlib import Path

from bids.ext.reports import templates


def test_pet():
    with open(Path(__file__).parent / "data" / "sub-01_ses-01_pet.json") as f:
        metadata = json.load(f)

    templates.pet_info(metadata)
