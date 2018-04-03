# Ubuntu Sever Development Summary
This repository is used by the Canonical Server team to develop the weekly
development summary that is sent out to the community as a whole. This summary
is used to communicate accomplishments and progress made by the server team
over the previous week.

## Template
The template is a starter to generating the weekly summary. This is used to
allow whoever is working on the summary to focus on content and not style.

## Instructions
Below is a list of steps to generate the complete summary:

1. Template & Uploads
  - Run the `generate.sh` script to create a new markdown file for today.
  - The `upload_report.py` will automatically run with last week's date
  - Paste the output into the generated markdown document
2. Triage Queue
  - Login to the team KPI
  - Copy the three values under Bug Triage into the markdown document
3. IRC Meeting
  - Get the link to the latest meeting from [Meetingology](https://ubottu.com/meetingology/logs/ubuntu-meeting/)
  - Put that link into the markdown document
4. cloud-init and curtin
  - Review the Trello board done column
  - Summarize any done cards
5. Ubuntu Server
  - Review the Trello board done column
  - Summarize any done cards
6. Review
  - Send out a link to the draft for review to the team
  - Check spelling and grammer during this time as well
  - Add http://pad.lv/ links for Launchpad bugs.
7. Publish
  - Get Ubuntu Server image for the week
  - Convert markdown to HTML
    - Chrome app: "Minimalist Markdown", works well.
      - Paste MD into left pane, copy out HTML from right pane
    - Or use [online app](http://dillinger.io/)
  - Create blog post on insights.ubuntu.com
    1. Create new blog post: articles -> add an article
    2. Title: "Ubuntu Server development summary - DD Month YYYY"
    3. Tags: Ubuntu Server, Server, weekly
    4. Topic: Cloud, Server
    5. Group: Cloud and server
    6. Text Tab: Paste html from chrome app
    7. Bottom Right: Featured Image -> Set Featured Image
    8. Publish!
8. Send email
  - `sudo pip3 install markdown-link-style`
  - `mdl-style footnote 2017-07-07.md /tmp/email.txt`
  - Verify no line is longer than 72 charachters
  - Subject: Ubuntu Server development summary - DD Month YYYY
  - mailto:ubuntu-server@lists.ubuntu.com
  - Bcc: lwn@lwn.net
  - Add link to insights post to top of email
