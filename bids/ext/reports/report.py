"""Generate publication-quality data acquisition methods section from BIDS dataset."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from bids.layout import BIDSFile, BIDSLayout
from rich import print

from . import parsing, utils
from .logger import pybids_reports_logger

LOGGER = pybids_reports_logger()


class BIDSReport:
    """Generate publication-quality data acquisition section from BIDS dataset.

    Parameters
    ----------
    layout : :obj:`bids.layout.BIDSLayout`
        Layout object for a BIDS dataset.

    config : :obj:`str` or :obj:`dict`, optional
        Configuration info for methods generation. Can be a path to a file
        (str), a dictionary, or None. If None, loads and uses default
        configuration information.
        Keys in the dictionary include:

            'dir':      a dictionary for converting encoding direction strings
                        (e.g., j-) to descriptions (e.g., anterior to
                        posterior)
            'seq':      a dictionary of sequence abbreviations (e.g., EP) and
                        corresponding names (e.g., echo planar)
            'seqvar':   a dictionary of sequence variant abbreviations
                        (e.g., SP) and corresponding names (e.g., spoiled)

    Warning
    -------
    pybids' automatic report generation is experimental and currently under
    active development, and as such should be used with caution.
    Please remember to verify any generated report before putting it to use.

    Additionally, only MRI datatypes (func, anat, fmap, and dwi) are currently
    supported.
    """

    def __init__(
        self, layout: BIDSLayout, config: None | str | Path | dict[str, dict[str, str]] = None
    ):
        self.layout = layout
        if config is None:
            config = Path(__file__).absolute().parent / "templates" / "config" / "converters.json"

        if isinstance(config, str):
            config = Path(config)
        if isinstance(config, Path):
            with config.open() as fobj:
                config = json.load(fobj)

        if not isinstance(config, dict):
            raise ValueError(
                "Input config must be None, dict, or path to json file containing dict."
            )

        self.config = config

    def generate_from_files(self, files: list[BIDSFile]) -> Counter[str]:
        r"""Generate a methods section from a list of files.

        Parameters
        ----------
        files : list of :obj:`~bids.layout.BIDSImageFile` objects
            List of files from which to generate methods description.

        Returns
        -------
        counter : :obj:`collections.Counter`
            A dictionary of unique descriptions across subjects in the file list,
            along with the number of times each pattern occurred. In cases
            where all subjects underwent the same protocol, the most common
            pattern is most likely the most complete. In cases where the
            file list contains multiple protocols, each pattern will need to be
            inspected manually.
        """
        descriptions = []

        subjects = sorted(list({f.get_entities().get("subject") for f in files}))
        sessions = sorted(list({f.get_entities().get("session") for f in files}))
        for sub in subjects:
            subject_files = [f for f in files if f.get_entities().get("subject") == sub]
            description_list = []
            for ses in sessions:
                data_files = [f for f in subject_files if f.get_entities().get("session") == ses]

                if data_files:
                    ses_description = parsing.parse_files(
                        self.layout,
                        data_files,
                        self.config,
                    )
                    ses_description[0] = f"In session {ses}, " + ses_description[0]
                    description_list += ses_description
                    metadata = self.layout.get_metadata(data_files[0].path)
                else:
                    raise Exception(f"No imaging files for subject {sub}")

            # Assume all data were converted the same way and use the last nifti
            # file's json for conversion information.
            if "metadata" not in vars():
                raise Exception("No valid jsons found. Cannot generate final paragraph.")

            description = "\n\t".join(description_list)
            description += f"\n\n{parsing.final_paragraph(metadata)}"
            descriptions.append(description)
        counter = Counter(descriptions)
        print(f"Number of patterns detected: {len(counter.keys())}")
        print(utils.reminder())
        return counter

    def generate(self, **kwargs: Any) -> Counter[str]:
        r"""Generate the methods section.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments passed to BIDSLayout to select subsets of the
            dataset.

        Returns
        -------
        counter : :obj:`collections.Counter`
            A dictionary of unique descriptions across subjects in the dataset,
            along with the number of times each pattern occurred. In cases
            where all subjects underwent the same protocol, the most common
            pattern is most likely the most complete. In cases where the
            dataset contains multiple protocols, each pattern will need to be
            inspected manually.
        """
        descriptions = []

        subjects = self.layout.get_subjects(**kwargs)
        kwargs = {k: v for k, v in kwargs.items() if k != "subject"}
        for sub in subjects:
            descriptions.append(self._report_subject(subject=sub, **kwargs))

        counter = Counter(descriptions)
        LOGGER.info(f"Number of patterns detected: {len(counter.keys())}")

        LOGGER.info(utils.reminder())

        return counter

    def _report_subject(self, subject: str, **kwargs: Any) -> str:
        """Write a report for a single subject.

        Parameters
        ----------
        subject : :obj:`str`
            Subject ID.

        Attributes
        ----------
        layout : :obj:`bids.layout.BIDSLayout`
            Layout object for a BIDS dataset.

        config : :obj:`dict`
            Configuration info for methods generation.

        Returns
        -------
        description : :obj:`str`
            A publication-ready report of the dataset's data acquisition
            information. Each scan type is given its own paragraph.
        """
        description_list = []
        # Remove session from kwargs if provided, else set session as all available
        sessions = kwargs.pop("session", self.layout.get_sessions(subject=subject, **kwargs))
        if not sessions:
            sessions = [None]
        elif not isinstance(sessions, list):
            sessions = [sessions]

        for ses in sessions:
            data_files = self.layout.get(
                subject=subject,
                extension=[".nii", ".nii.gz", ".set", ".fif", ".edf", ".bdf", ".snirf"],
                **kwargs,
            )

            if data_files:
                ses_description = parsing.parse_files(
                    self.layout,
                    data_files,
                    self.config,
                )
                ses_description[0] = f"In session {ses}, " + ses_description[0]
                description_list += ses_description
                metadata = self.layout.get_metadata(data_files[0].path)
            else:
                LOGGER.warning(f"No imaging files for subject {subject}")
                metadata = None

        # Assume all data were converted the same way and use the first nifti
        # file's json for conversion information.
        description = "\n".join(description_list)
        if metadata:
            description += f"\n\n{parsing.final_paragraph(metadata)}"
        return description
