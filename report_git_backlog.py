#!/usr/bin/env python3
"""Determine unpublished backlog messages for a given repo (cloud-init|curtin)

Copyright 2018 Canonical Ltd.
"""
import argparse
from datetime import datetime
import subprocess as subp
import os
import shutil
import sys
from urllib.request import urlopen
CORE_DEVS = ['Scott Moser', 'Ryan Harper', 'Josh Powers', 'Chad Smith']


def get_unreported_commits(project_name, start_date):
    """Inspect previous status summary and report only unpublished commits.

    Commit messages already present in the previous dev-summary are excluded.

    @param project_name: A known launchpad-git project from which we
       report commit logs (curtin|cloud-init). Will be cloned via the command:
       git clone lp:project_name.
    @param start_date: The date string YYYY-MM-DD from which we will publish
       git logs. Any logs seen in previous
    @return: A list of debian changelog lines including author and bug numbers.
       Each changelog entry filters cloud-init core developers from the commit
       log.
    """
    year = start_date.split('-')[0]
    with open(os.path.join('doc', year, '%s.md' % start_date)) as stream:
        previous_status = stream.read()
    if not os.path.exists(project_name):
        with open(os.devnull, 'w') as FNULL:
            subp.check_call(
                ['git', 'clone', 'lp:%s' % project_name], stdout=FNULL)
    cwd = os.getcwd()
    os.chdir(project_name)
    with open(os.devnull, 'w') as FNULL:
        subp.check_call(['git', 'pull'], stdout=FNULL)
    git_log = subp.check_output(
        ['git', 'log', '--since', '%sT00:00:00-00:00' % start_date])
    with open('/tmp/recent_git_log', 'wb') as stream:
        stream.write(git_log)
    if shutil.which('log2dch'):
        dch_output = subp.check_output(
            ['log2dch', '/tmp/recent_git_log']).decode('utf-8')
    else:
        dch_output = subp.check_output(
            ['git', 'log', '--since', '%sT00:00:00-00:00' % start_date,
             "--format=  - %s [%aN]"]).decode('utf-8')
        for person in CORE_DEVS:
            dch_output = dch_output.replace(' [%s]' % person, '')

    unreported_lines = []
    for line in dch_output.splitlines():
       stripped_line = line.strip()
       if stripped_line.startswith('- '):
           prefix = '  '
           if stripped_line in previous_status:
               break
       else:  # Proper indent of multi-line entry
           prefix = '    '
       unreported_lines.append('%s%s' % (prefix, stripped_line))
    os.chdir(cwd)
    return unreported_lines


def main(start_date, doc_file):
    """Get report and print unpublished commits to project."""
    summary_lines = ['\n## cloud-init\n']
    summary_lines.extend(get_unreported_commits('cloud-init', start_date))
    summary_lines.append('\n## curtin\n')
    summary_lines.extend(get_unreported_commits('curtin', start_date))
    summary_content = '\n'.join(summary_lines)
    with open(doc_file, 'rb') as stream:
       template_content = stream.read().decode('utf-8')
    with open(doc_file, 'wb') as stream:
       stream.write(
           template_content.format(
               cloud_init_curtin_logs=summary_content).encode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "start_date", help=("The start-date for the format YYYY-MM-DD from"
                            " which to generate the dev-summary"))
    parser.add_argument(
        "outfile", help="The path to the markdown file we will update.")
    args = parser.parse_args()
    main(args.start_date, args.outfile)
