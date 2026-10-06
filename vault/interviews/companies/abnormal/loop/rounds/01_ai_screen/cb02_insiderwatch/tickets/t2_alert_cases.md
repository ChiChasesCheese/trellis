# INSIDER-331: Alert fatigue

Analysts are drowning: one bad actor can generate 40 alerts in a night. Group them so an analyst
sees one thing per incident, and stop paging the on-call Slack channel 40 times for the same person.

New command: `python -m insiderwatch cases [--user U] [--json]`. With `--json` it prints a list of
cases, each with at least `id`, `user`, `status` (`open` / `closed`), `severity` (`low` / `medium` /
`high`) and `alerts` (the ids of its member alerts). `python -m insiderwatch cases close <id>` closes
a case once the analyst has dealt with it.
