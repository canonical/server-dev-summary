#!/bin/bash
set -u

TODAY=$(date +'%Y-%m-%d')
LAST_SUMMARY=$(date -d "now -7 days" +'%Y-%m-%d')

if [ ! -e doc/"$TODAY".md ]; then
    cp template.md doc/"$TODAY".md
fi

./upload_report.py "$LAST_SUMMARY"
