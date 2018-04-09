#!/usr/bin/env python3
"""Determine backlog count and bugs reviewed for report.

Copyright 2018 Canonical Ltd.
Joshua Powers <josh.powesrs@canonical.com>
"""
from datetime import datetime
import json
import sys
from urllib.request import urlopen

BASE_URL = 'http://10.25.2.224:9090/api/v1/query?query='


def _get_json_from_url(json_url):
    """Return JSON from a URL."""
    with urlopen(json_url) as url:
        data = json.loads(url.read().decode())

    return data


def bug_backlog_size():
    """Print out the current backlog size."""
    query = 'sum(server_triage_backlog_total{exported_job="server-triage"})'
    data = _get_json_from_url('%s%s' % (BASE_URL, query))
    backlog = data['data']['result'][0]['value'][1]
    print("- %s in the [backlog]('https://bugs.launchpad.net/"
          "~ubuntu-server/+subscribedbugs)" % backlog)


def bug_reviewed_size(start_date):
    """Print number of bugs reviewed since last summary."""
    date_fmt = '%Y-%m-%d'
    time_difference = datetime.now() - datetime.strptime(start_date, date_fmt)
    query = ('sum(increase(server_triage_daily_triage_total{exported_job='
             '"server-triage"}[%sd]))' % time_difference.days)
    data = _get_json_from_url('%s%s' % (BASE_URL, query))
    reviewed = int(float(data['data']['result'][0]['value'][1]))
    print("- %s bugs reviewed since the last report" % reviewed)


def main():
    """Get report and print."""
    print('')
    print('## Bug Work and Triage\n')
    bug_backlog_size()
    bug_reviewed_size(sys.argv[1])
    print('- [Notes on daily bug triage](https://wiki.ubuntu.com/'
          'ServerTeam/KnowledgeBase#Bug_Triage)\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please enter a date in the format YYYY-MM-DD')
        sys.exit(1)

    main()
