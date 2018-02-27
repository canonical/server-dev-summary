#!/usr/bin/python3
"""Determine uploads into development release and SRUs.

Copyright 2017 Canonical Ltd.
Robbie Basak <robie.basak@canonical.com>
Joshua Powers <josh.powers@canonical.com>
"""
from functools import lru_cache
import sys

import launchpadlib.launchpad
from lazr.restfulclient.errors import ClientError

SRU = 'SRU'
DEV = 'DEV'


@lru_cache()
def series_name(launchpad, series_link):
    """Translate series link to a name."""
    return launchpad.load(series_link).name


@lru_cache()
def person_name(launchpad, person_link):
    """Translate name link to a name."""
    if person_link:
        try:
            return launchpad.load(person_link).name
        except ClientError as exc:
            if exc.response["status"] == "410":  # gone, user suspended
               return None
    return None


def generate_uploads(start_date):
    """Determine uploads from a particular date."""
    launchpad = launchpadlib.launchpad.Launchpad.login_with(
        'ubuntu-server upload report',
        'production',
        version='devel',
    )

    packages = [
        p.name
        for p in launchpad.people['ubuntu-server'].getBugSubscriberPackages()
    ]

    ubuntu = launchpad.distributions['ubuntu']
    devel = ubuntu.current_series_link.split('/')[-1]
    archive = ubuntu.main_archive

    for package in packages:
        spphs = archive.getPublishedSources(
            created_since_date=start_date,
            order_by_date=True,  # essential ordering for migration detection
            source_name=package,
            exact_match=True,
        )
        migrated_versions = set()
        for spph in spphs:
            report_entry = {
                'package': spph.source_package_name,
                'version': spph.source_package_version,
                'author': person_name(launchpad, spph.package_creator_link),
                'series': series_name(launchpad, spph.distro_series_link),
                'signer': person_name(launchpad, spph.package_signer_link),
                'sponsor': person_name(launchpad, spph.sponsor_link),
                'pocket': spph.pocket,
                'created': spph.date_created,
            }

            if report_entry['pocket'] == 'Security':
                    continue

            if report_entry['series'] == devel:
                if report_entry['pocket'] == 'Release':
                    migrated_versions.add(report_entry['version'])
                    continue  # ignore migration from an upload perspective
                elif report_entry['pocket'] == 'Proposed':
                    report_entry['migrated'] = (
                        report_entry['version'] in migrated_versions
                    )
                report_entry['category'] = DEV
            else:
                if report_entry['pocket'] == 'Updates':
                    migrated_versions.add(report_entry['version'])
                elif report_entry['pocket'] == 'Proposed':
                    report_entry['migrated'] = (
                        report_entry['version'] in migrated_versions
                    )
                report_entry['category'] = SRU

            if report_entry['sponsor'] == 'ubuntu-archive-robot':
                continue  # skip syncs

            yield report_entry


def print_proposed_sru(entries):
    """Print SRU Proposed entries."""
    print('')
    print('### Proposed Uploads to the Supported Releases\n')
    print('Please consider testing the following by [enabling proposed]'
          '(https://wiki.ubuntu.com/Testing/EnableProposed)'
          ', checking packages for update regressions, and making sure to '
          'mark affected bugs [verified as fixed]'
          '(https://wiki.ubuntu.com/StableReleaseUpdates#Verification).\n')
    print('Total: %s\n' % len(entries))

    if not entries:
        return

    for entry in entries:
        uploader = entry['author'] if entry['author'] else entry['signer']
        print('- [`%s, %s, %s, %s`](https://launchpad.net/ubuntu/+source/%s/%s)' %
              (entry['package'], entry['series'], entry['version'], uploader,
               entry['package'], entry['version']))


def print_sru(entries):
    """Print SRU entries."""
    print('')
    print('### Uploads Released to the Supported Releases\n')
    print('Total: %s\n' % len(entries))

    if not entries:
        return

    for entry in entries:
        uploader = entry['author'] if entry['author'] else entry['signer']
        print('- [`%s, %s, %s, %s`](https://launchpad.net/ubuntu/+source/%s/%s)' %
              (entry['package'], entry['series'], entry['version'], uploader,
               entry['package'], entry['version']))


def print_dev(entries):
    """Print Dev release entries."""
    print('')
    print('### Uploads to the Development Release\n')
    print('Total: %s\n' % len(entries))

    if not entries:
        return

    for entry in entries:
        uploader = entry['author'] if entry['author'] else entry['signer']
        print('- [`%s, %s, %s`](https://launchpad.net/ubuntu/+source/%s/%s)' %
              (entry['package'], entry['version'], uploader,
               entry['package'], entry['version']))

def main():
    """Get report and print."""
    report = sorted(
        generate_uploads(sys.argv[1]),
        key=lambda r: r['category']
    )

    print_proposed_sru([item for item in report if item['category'] == SRU
                       and item['pocket'] == 'Proposed'
                       and not item['migrated']])
    print_sru([item for item in report if item['category'] == SRU
              and item['pocket'] == 'Updates'])
    print_dev([item for item in report if item['category'] == DEV])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please enter a date in the format YYYY-MM-DD')
        sys.exit(1)

    main()
