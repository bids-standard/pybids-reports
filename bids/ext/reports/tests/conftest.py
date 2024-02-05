"""Fixtures for tests."""

from __future__ import annotations

import json
from os.path import abspath, join

import nibabel as nib
import pytest
from bids.tests import get_test_data_path

from bids.layout import BIDSLayout
from bids.tests import get_test_data_path


@pytest.fixture(scope="module")
def testdataset():
    """Path to a BIDS dataset for testing."""
    data_dir = join(get_test_data_path(), "synthetic")
    return data_dir


@pytest.fixture(scope="module")
def testlayout(testdataset):
    """A BIDSLayout for testing."""
    return BIDSLayout(testdataset)


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def testdiffimg(testlayout):
    """A Nifti1Image for testing."""
    dwi_files = testlayout.get(
        subject="01",
        session="01",
        datatype="dwi",
        extension=[".nii.gz"],
    )
    return nib.load(dwi_files[0].path)


@pytest.fixture(scope="module")
def testconfig():
    """The standard config file for testing."""
    config_file = abspath(join(get_test_data_path(), "../../reports/config/converters.json"))
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
