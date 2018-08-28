#!/bin/bash
# Will generate email and html versions of latest report.
#
# Copyright 2018 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -u

LATEST_SUMMARY=$(ls doc/*/*-*.md | sort | tail -1)
BASE_DIR=$(dirname "$LATEST_SUMMARY")
FILE_NAME=$(basename "$LATEST_SUMMARY" .md)

# Create HTML document for wordpress publication
# apt install pandoc
pandoc --from markdown "$LATEST_SUMMARY" --to html \
    --output "$BASE_DIR/$FILE_NAME".html

# Create email and format correctly
# pip3 install markdown-link-style
mdl-style footnote "$LATEST_SUMMARY" "$BASE_DIR/$FILE_NAME".email
./clean_email.py "$BASE_DIR/$FILE_NAME".email
