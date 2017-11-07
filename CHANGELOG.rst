Changelog
=========

vx.x.x
------

*Unreleased*

Features
~~~~~~~~

- E-mails are now sent with a multipart/HTML version, featuring very plain text
  in a box, styled with the event's primary color. (#159)
- You can now choose to hide the public schedule (including talk pages and
  speaker pages, but excluding feedback pages and the schedule.xml export) (#126)
- Mail template placeholders are now validated so that invalid placeholders
  cannot be saved at all. (#215)
- You can now add questions that take a file upload as an answer. (#208)
- Speakers can now upload files which will be shown on their talk page. (#209)
- Questions can now be considered 'asking for personal data', and answers to
  those questions will be deleted on account deletion. Questions are considered
  to ask for personal data by default, to ease migration.

Bug fixes
~~~~~~~~~

- Don't crash when using incorrect invite tokens, show a 404 page instead (#204).
- Use actual hostname and not localhost when building absolute URLs.
- Fix an access rights issue that made it impossible to be both reviewer and orga.


v0.1.0
------

*Released on 2017-11-01.*

As this is the first release, there are neither new features, nor fixed bugs,
nor relevant release notes. All of those are to follow!

pretalx releases will be signed by PGP key F0DAD3990F9C816CFD30F8F329C085265D94C052.
Further details, including the PGP key, will be supplied at https://pretalx.org.
