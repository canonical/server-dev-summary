#!/bin/bash
# Generate initial weekly report
#
# Copyright 2017-2018 Canonical Ltd.
# David Britton <david.britton@canonical.com>
# Joshua Powers <josh.powers@canonical.com>
set -u

YEAR=$(date +'%Y')
SUMMARY_FILEPATH="doc/$YEAR/$(date +'%Y-%m-%d').md"
LAST_SUMMARY_DATE=$(basename $(ls doc/*/*-*.md | sort | tail -1 ) .md)

if [ ! -d "doc/$YEAR" ]; then
    mkdir -p "doc/$YEAR"
fi

if [ -e "$SUMMARY_FILEPATH" ]; then
    rm "$SUMMARY_FILEPATH"
fi

cp template.md "$SUMMARY_FILEPATH"
./report_backlog.py "$LAST_SUMMARY_DATE" >> "$SUMMARY_FILEPATH"
./report_uploads.py "$LAST_SUMMARY_DATE" >> "$SUMMARY_FILEPATH"
