"""Tests for bids.reports.report."""
import json
from collections import Counter
from os.path import abspath, join

from bids.tests import get_test_data_path

from ext.reports import BIDSReport


def test_report_init(testlayout):
    """Report initialization should return a BIDSReport object."""
    report = BIDSReport(testlayout)
    assert isinstance(report, BIDSReport)


def test_report_gen(testlayout):
    """Report generation should return a counter of unique descriptions in the dataset."""
    report = BIDSReport(testlayout)
    descriptions = report.generate()
    assert isinstance(descriptions, Counter)


def test_report_gen_from_files(testlayout):
    """Test that a report from a file list returns a Counter of unique descs in the dataset."""
    report = BIDSReport(testlayout)
    files = testlayout.get(extension=[".nii.gz", ".nii"])
    descriptions = report.generate_from_files(files)
    assert isinstance(descriptions, Counter)


def test_report_subject(testlayout):
    """Test that a report for one subject return one subject's description.

    This should be one pattern with a counter of one in the Counter.
    """
    report = BIDSReport(testlayout)
    descriptions = report.generate(subject="01")
    assert sum(descriptions.values()) == 1


def test_report_session(testlayout):
    """Test that a report for one session doesn't show other sessions in any descriptions."""
    report = BIDSReport(testlayout)
    descriptions = report.generate(session="01")
    assert "session 02" not in " ".join(descriptions.keys())


def test_report_file_config(testlayout):
    """Report initialization should take in a config file and use that if provided."""
    config_file = abspath(join(get_test_data_path(), "../../reports/config/converters.json"))
    report = BIDSReport(testlayout, config=config_file)
    descriptions = report.generate()
    assert isinstance(descriptions, Counter)


def test_report_dict_config(testlayout):
    """Report initialization should take in a config dict and use that if provided."""
    config_file = abspath(join(get_test_data_path(), "../../reports/config/converters.json"))
    with open(config_file, "r") as fobj:
        config = json.load(fobj)
    report = BIDSReport(testlayout, config=config)
    descriptions = report.generate()
    assert isinstance(descriptions, Counter)
