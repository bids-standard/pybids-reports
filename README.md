# pybids-reports

pybids-reports is a subpackage of pyBIDS, implementing automatic report
generation from BIDS datasets.

See the [BIDS paper](http://www.nature.com/articles/sdata201644) and
http://bids.neuroimaging.io website for more information.

NOTE: The reports module is experimental and currently under active development,
and as such should be used with caution. Please remember to verify any generated
report before putting it to use.

Additionally, only MRI datatypes (func, anat, fmap, and dwi) are currently
supported.

### Quickstart

A simple example of standard usage follows. We assume that we have a root folder
containing a BIDS-compliant project in `/bidsproject`.

<!-- TODO

update example below

 -->

```python
from bids.layout import BIDSLayout
from bids.reports import BIDSReport

# Load the BIDS dataset
layout = BIDSLayout('/bidsproject')

# Initialize a report for the dataset
report = BIDSReport(layout)

# Method generate returns a Counter of unique descriptions across subjects
descriptions = report.generate()

# For datasets containing a single study design, all but the most common
# description most likely reflect random missing data.
pub_description = descriptions.most_common()[0][0]
```

## License

`pybids-reports` is licensed under the terms of the MIT license. See the file
"LICENSE" for information on the history of this software, terms & conditions
for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.

Copyright (c) 2016--, PyBIDS developers, Planet Earth
