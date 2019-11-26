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

1. Ubuntu Server Image
    - [Go create it](https://docs.google.com/presentation/d/10Jj-Qyu1OMhwtijCgZrKqiF4z6Z4NOeT5opowyq6Mew/edit?usp=sharing)
1. Template & Uploads
    - Run the `generate.sh` script to create a new markdown file for today and
      base it off of deltas between the most recent previous report's date
1. cloud-init and curtin
    - Review the Trello board done column
    - Summarize any done cards and add any missing items to the auto-generated
      items
1. Ubuntu Server
    - Review the Trello board done column
    - Summarize any done cards and add any missing items to the auto-generated
      items
1. Review
    - Send out a link to the draft for review to the team
    - Check spelling and grammar during this time as well
1. Run `publish.sh` to generate html and email formats
1. Insights
      1. Create a new blog post at
         https://admin.insights.ubuntu.com/wp-admin/post-new.php
      2. Title: "Ubuntu Server development summary - DD Month YYYY"
      3. Tags: Ubuntu Server, Server, weekly
      4. Topic: Cloud, Server
      5. Group: Cloud and server
      6. Text Tab: Paste html from chrome app
      7. Bottom Right: Featured Image -> Set Featured Image
      8. Publish!
1. Discourse
      1. Login to server hub at https://discourse.ubuntu.com/c/server
      2. Click new topic button 
      3. Title: "Ubuntu Server development summary - DD Month YYYY"
      4. Click the 'Upload' button above the text area for the new topic and upload the same png image you created for the insights post
      5. Paste the markdown output used in insights step above.
1. Send email to ubuntu-server
    - Use the $date.email file as the body of the email
    - Subject: Ubuntu Server development summary - DD Month YYYY
    - to: ubuntu-server@lists.ubuntu.com
    - bcc: lwn@lwn.net
1. Announce
    - Announce the post in #marketing about the post
