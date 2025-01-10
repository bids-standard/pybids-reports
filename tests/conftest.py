"""Fixtures for tests."""

from __future__ import annotations

import json
from pathlib import Path

import nibabel as nib
import pytest
from bids.layout import BIDSLayout


@pytest.fixture
def data_path():
    return Path(__file__).parent / "data"


@pytest.fixture
def testdataset(data_path):
    """Path to a BIDS dataset for testing."""
    data_dir = data_path / "synthetic"
    return data_dir


@pytest.fixture(scope="session")
def testlayout(testdataset):
    """A BIDSLayout for testing."""
    return BIDSLayout(testdataset)


@pytest.fixture
def testimg(testlayout):
    """A Nifti1Image for testing."""
    func_files = testlayout.get(
        subject="01",
        session="01",
        task="nback",
        run="01",
        extension=[".nii.gz"],
    )
    return nib.load(func_files[0].path)


@pytest.fixture
def testdiffimg(testlayout):
    """A Nifti1Image for testing."""
    dwi_files = testlayout.get(
        subject="01",
        session="01",
        datatype="dwi",
        extension=[".nii.gz"],
    )
    return nib.load(dwi_files[0].path)


@pytest.fixture
def testconfig():
    """The standard config file for testing."""
    config_file = Path(__file__).parent / "config" / "converters.json"
    with open(config_file) as fobj:
        config = json.load(fobj)
    return config


@pytest.fixture(scope="module")
def testmeta():
    """A small metadata dictionary for testing."""
    return {
        "RepetitionTime": 2.0,
        "MultibandAccelerationFactor": 2,
        "ParallelReductionFactorInPlane": 2,
        "FlipAngle": 90,
        "PhaseEncodingDirection": "i",
        "SliceTiming": [0, 1, 2, 3],
    }


@pytest.fixture(scope="module")
def testmeta_light():
    """An even smaller metadata dictionary for testing."""
    return {"RepetitionTime": 2.0}
