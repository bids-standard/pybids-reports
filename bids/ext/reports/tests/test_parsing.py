"""Tests for bids.reports.parsing."""
from __future__ import annotations

from pathlib import Path

from bids import BIDSLayout
from bids.ext.reports import parsing
from bids.tests import get_test_data_path


def test_anat_info_smoke(testlayout, testconfig):
    """Smoke test for parsing.anat_info.

    It should return a str description when provided valid inputs.
    """
    anat_files = testlayout.get(
        subject="01",
        session="01",
        suffix="T1w",
        extension=[".nii.gz"],
    )
    desc = parsing.anat_info(anat_files, testconfig, testlayout)
    assert isinstance(desc, str)


def test_dwi_info_smoke(testlayout, testconfig):
    """Smoke test for parsing.dwi_info.

    It should return a str description when provided valid inputs.
    """
    dwi_files = testlayout.get(
        subject="01",
        session="01",
        datatype="dwi",
        extension=[".nii.gz"],
    )
    desc = parsing.dwi_info(dwi_files, testconfig, testlayout)
    assert isinstance(desc, str)


def test_fmap_info_smoke(testlayout, testconfig):
    """Smoke test for parsing.fmap_info.

    It should return a str description when provided valid inputs.
    """
    fmap_files = testlayout.get(
        subject="01",
        session="01",
        datatype="fmap",
        suffix="phasediff",
        extension=[".nii.gz"],
    )
    desc = parsing.fmap_info(testlayout, fmap_files, testconfig)
    assert isinstance(desc, str)


def test_func_info_smoke(testlayout, testconfig):
    """Smoke test for parsing.func_info.

    It should return a str description when provided valid inputs.
    """
    func_files = testlayout.get(
        subject="01",
        session="01",
        task="nback",
        run="01",
        extension=[".nii.gz"],
    )
    desc = parsing.func_info(func_files, testconfig, testlayout)
    assert isinstance(desc, str)


def test_meg_info_smoke():
    """Smoke test for parsing.meg_info.

    It should return a str description when provided valid inputs.
    """
    data_dir = Path(get_test_data_path()).joinpath("ds000117")
    testlayout = BIDSLayout(data_dir)
    meg_files = testlayout.get(
        subject="01",
        session="meg",
        task="facerecognition",
        run="01",
    )
    desc = parsing.meg_info(meg_files)
    assert isinstance(desc, str)


def test_final_paragraph_smoke(testmeta):
    """Smoke test for parsing.final_paragraph.

    It should return a str description when provided valid inputs.
    """
    desc = parsing.final_paragraph(testmeta)
    assert isinstance(desc, str)


def test_parse_files_smoke(testlayout, testconfig):
    """Smoke test for parsing.parse_files.

    It should return a list of string descriptions when provided valid inputs,
    with each string containing the description for a single nifti file
    (except functional data, which is combined within task, across runs).
    """
    subject = "01"
    niftis = testlayout.get(subject=subject, extension=[".nii", ".nii.gz"])
    desc = parsing.parse_files(testlayout, niftis, testconfig)
    assert isinstance(desc, list)
    assert isinstance(desc[0], str)
