#!/usr/bin/env python3
"""Clean email file for sending.

Copyright 2018 Canonical Ltd.
Joshua Powers <josh.powers@canonical.com>
"""
import re
import sys
import textwrap


def clean_email(filename):
    """TODO."""
    with open(filename, 'r') as file:
        text_array = file.readlines()

    new_text = ''
    for line in text_array:
        # Change header of '# Hello Ubuntu Server'
        if line == '# Hello Ubuntu Server\n':
            line = 'Hello Ubuntu Server,\n'

        # correct links [test][1] -- > test [1]
        line = re.sub(r'\[(.+?)\](\[\d+\])', r'\1 \2', line)

        # reduce line length to 72, unless a footnote link or upload line
        if (len(line) > 72 and not re.match(r'\[\d+\]:', line)
                and not re.match(r'- `(.+?)` (\[\d+\])\n', line)):
            line = '%s\n' % textwrap.fill(line, width=72)

        # remove backticks from package uploads
        line = re.sub(r'- `(.+?)` (\[\d+\])', r'- \1 \2', line)

        new_text += line

    with open(filename, 'w') as file:
        file.write(new_text)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please provide a filename as an argument to clean')
        sys.exit(1)

    clean_email(sys.argv[1])
