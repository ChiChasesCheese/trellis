# Rulelang

Rulelang is the detection engine of a multi-tenant email-security product. Customers send us email,
login and mailbox-rule events; Rulelang runs a set of detectors over each event, stores the signals they
raise, keeps a graph of who emails whom, and serves the results to analysts over a small HTTP API.

You have just joined the team that owns it. The repo is in `starter/` (Python 3.11+, standard library
plus pytest). `README.md` and `CONTRIBUTING.md` are the team's own docs. You have a browser VS Code with
Claude Code. Pick up the ticket you are given; you have about 35 minutes of implementation time.
