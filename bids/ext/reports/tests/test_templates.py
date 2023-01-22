"""Tests for bids.reports.parsing."""
import json
from pathlib import Path

from ext.reports import parsing, templates


def test_pet():

    with (open(Path(__file__).parent.joinpath("data", "sub-01_ses-01_pet.json")) as f):
        metadata = json.load(f)

    desc_data = {**parsing.device_info(metadata), **metadata}
    templates.pet_info(desc_data)
