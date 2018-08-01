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


if [ -z  `which log2dch` ]; then
  echo "Warning: missing log2dch script from https://github.com/CanonicalLtd/uss-tableflip for cloud-init and curtin dev-summary. This will result in missing bug references on published commit messages."
fi

cp template.md "$SUMMARY_FILEPATH"
./report_git_backlog.py "$LAST_SUMMARY_DATE" "$SUMMARY_FILEPATH"
./report_backlog.py "$LAST_SUMMARY_DATE" >> "$SUMMARY_FILEPATH"
./report_uploads.py "$LAST_SUMMARY_DATE" >> "$SUMMARY_FILEPATH"
