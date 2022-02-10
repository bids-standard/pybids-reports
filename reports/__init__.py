"""pybids-reports: A tool for building methods sections for BIDS datasets."""
from . import _version
from .due import Doi, due
from .report import BIDSReport

__all__ = ["BIDSReport"]

due.cite(
    Doi("10.1038/sdata.2016.44"),
    description="Brain Imaging Data Structure",
    tags=["reference-implementation"],
    path="bids",
)

del due, Doi

__version__ = _version.get_versions()["version"]
