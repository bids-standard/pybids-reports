"""Generate publication-quality data acquisition methods section from BIDS dataset.

Utilities to generate the MRI data acquisition portion of a
methods section from a BIDS dataset.
"""
from __future__ import annotations

from typing import Any

from .logger import pybids_reports_logger
from bids.layout import BIDSFile
from bids.layout import BIDSLayout

LOGGER = pybids_reports_logger()


def collect_associated_files(
    layout: BIDSLayout, files: list[BIDSFile], extra_entities: list[str] = []
) -> list[BIDSFile]:
    """Collect and group BIDSFiles with multiple files per acquisition.

    Parameters
    ----------
    layout

    files : list of BIDSFile

    extra_entities

    Returns
    -------
    collected_files : list of list of BIDSFile
    """
    MULTICONTRAST_ENTITIES = ["echo", "part", "ch", "direction"]
    MULTICONTRAST_SUFFIXES = [
        ("bold", "phase"),
        ("phase1", "phase2", "phasediff", "magnitude1", "magnitude2"),
    ]
    if len(extra_entities):
        MULTICONTRAST_ENTITIES += extra_entities

    collected_files: list[BIDSFile] = []
    for f in files:
        if len(collected_files) and any(f in filegroup for filegroup in collected_files):
            continue
        ents = f.get_entities()
        ents = {k: v for k, v in ents.items() if k not in MULTICONTRAST_ENTITIES}

        # Group files with differing multi-contrast entity values, but same
        # everything else.
        all_suffixes = ents["suffix"]
        for mcs in MULTICONTRAST_SUFFIXES:
            if ents["suffix"] in mcs:
                all_suffixes = mcs
                break
        ents.pop("suffix")
        associated_files = layout.get(suffix=all_suffixes, **ents)
        collected_files.append(associated_files)
    return collected_files


def reminder() -> str:
    """Remind users about things they need to do after generating the report."""
    return "Remember to double-check everything and to replace <deg> with a degree symbol."


def remove_duplicates(seq: list[Any]) -> list[Any]:
    """Return unique elements from list while preserving order.

    From https://stackoverflow.com/a/480227/2589328
    """
    seen: set[Any] = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def num_to_str(num: int | float | str) -> str:
    """Converts to a nice string.

    E.g.,
        21 -> '21'
        2.500 -> '2.5'
        3. -> '3'
    """
    return f"{num:0.02f}".rstrip("0").rstrip(".")


def list_to_str(lst: list[str]) -> str:
    """Turn a list into a comma- and/or and-separated string.

    Parameters
    ----------
    lst : :obj:`list`
        A list of strings to join into a single string.

    Returns
    -------
    str_ : :obj:`str`
        A string with commas and/or ands separating the elements from ``lst``.

    """
    if len(lst) == 1:
        str_ = lst[0]
    elif len(lst) == 2:
        str_ = " and ".join(lst)
    elif len(lst) > 2:
        str_ = ", ".join(lst[:-1])
        str_ += f", and {lst[-1]}"
    else:
        raise ValueError("List of length 0 provided.")
    return str_
