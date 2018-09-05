#!/usr/bin/env python3
"""Determine backlog count and bugs reviewed for report.

Copyright 2018 Canonical Ltd.
Joshua Powers <josh.powers@canonical.com>
"""
from datetime import datetime
import json
import sys
from urllib.request import urlopen

from launchpadlib.launchpad import Launchpad


def bug_backlog_size():
    """Print out the current backlog size."""
    launchpad = Launchpad.login_anonymously(
        'ubuntu-bug-triage', 'production', version='devel'
    )
    ubuntu = launchpad.distributions['Ubuntu']
    team = launchpad.people['ubuntu-server']
    backlog = len(ubuntu.searchTasks(bug_subscriber=team))

    print("- %s bugs in the [backlog]('https://bugs.launchpad.net/"
          "~ubuntu-server/+subscribedbugs)" % backlog)


def main():
    """Get report and print."""
    print('')
    print('## Bug Work and Triage\n')
    bug_backlog_size()
    print('- [Notes on daily bug triage](https://wiki.ubuntu.com/'
          'ServerTeam/KnowledgeBase#Bug_Triage)\n')


if __name__ == '__main__':
    main()
