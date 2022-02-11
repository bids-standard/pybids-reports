"""Fixtures for tests."""
import json
from os.path import abspath, join

import nibabel as nib
import pytest
from bids.tests import get_test_data_path

from bids import BIDSLayout


@pytest.fixture
def testlayout():
    """A BIDSLayout for testing."""
    data_dir = join(get_test_data_path(), "synthetic")
    return BIDSLayout(data_dir)


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
    config_file = abspath(
        join(get_test_data_path(), "../../reports/config/converters.json")
    )
    with open(config_file, "r") as fobj:
        config = json.load(fobj)
    return config


@pytest.fixture
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


@pytest.fixture
def testmeta_light():
    """An even smaller metadata dictionary for testing."""
    return {"RepetitionTime": 2.0}
