# Time Tracker

A stripped-back timesheet tracking tool, coded in Python: add clients, log hours against those clients, and then download summaries. The scope was intentionally kept as small as possible to make the app more functional.

Built using Eel for the web client and SQLite for persistent storage - this allows for easy data portability once you need more complex features.

> Please note that this code has not been hardened against any attacks - as such, it is wholly unsuitable for hosting on an untrusted network!
> If you do want to use this, I recommend using Tailscale (or a similar service) to provide controlled access from anywhere.
