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

1. Template
  - Copy the template.md file to doc string
  - `cp template.md doc/$(date +'%Y-%m-%d').md`
2. Uploads
  - Download and run the [upload report](https://git.launchpad.net/server-team-ci/plain/scripts/upload_report.py)
  - Use the preivous Friday as the input date
3. Triage Queue
  - Look at the bug triage spreadsheet and look at the rows for the past week
  - If someone has not done bug triage that is fine
  - Sum up the number of bugs reviewed (Column J)
  - Sum up the number of bugs accepted (Column K)
  - View the final count of bugs in the backlog (Column I)
4. IRC Meeting
  - Get the link to the latest meeting from [Meetingology](https://ubottu.com/meetingology/logs/ubuntu-meeting/)
5. cloud-init and curtin
  - Review the Trello board done column
  - Summarize any done cards
6. Ubuntu Server
  - Review the Trello board done column
  - Summarize any done cards
7. Review
  - Send out a link to the draft for review to the team
