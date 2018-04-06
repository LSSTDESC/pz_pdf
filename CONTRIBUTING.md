# How to contribute to PZPipelines packages.

## Coding guidelines and suggested practices

Please read and adhere to the DESC coding guidlines: https://docs.google.com/document/d/1v54bVQI2NejK2UqACDnGXj1t6IGFgY3Uc1R7iV2uLpY/edit

### Supplemental LSST DM standards of interest

LSST Data Management has a page (https://developer.lsst.io) devoted to developer standards and practices that may be useful to duplicate within DESC, especially if/when DESC code needs to interface with that from DM (e.g pz_pdf). Not all of this will be applicable to development within DESC (e.g. you can safely ignore mentions of Jenkins or JIRA) much of it is transferable.

Git/Github setup: https://developer.lsst.io/git/setup.html
This link also includes links to helpful Git/Github tutorials for newcomers.

LSST DM python style: https://developer.lsst.io/python/style.html
Documenting python code: https://developer.lsst.io/python/numpydoc.html

## Creating Issues

To keep the issue page relatively clean, inquiries about functionality, possible improvements, additions, etc. should be made first in the #desc-pz Slack channel. If it is agreed that the new functionality/ improvement should be implemented or that more discussion is warranted, then an issue can be created. If code development is associated with this issue, please also create an associated branch in the repo.

To compare to LSST DM, we would like to, for now, have issues be treated similarly to how DM treats tickets, Request for Changes (RFCs, https://developer.lsst.io/communications/rfc.html) and Request for Discussions (RFDs, https://developer.lsst.io/communications/rfd.html).

## Branches

Users branches not related to a specific Github issue should use the following naming convention:
u/{{username}}/{{topic}}

Branches associated with a given issue should take the form:
issue/{{NUMBER}}/{{topic}}

## Workflow
[TODO]
