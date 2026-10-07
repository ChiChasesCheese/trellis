# insiderwatch

Insider-risk detection over audit logs. Customers connect their SaaS audit logs (Microsoft 365,
Okta, Slack); we normalize them to events, learn what is normal for each person, and raise alerts
when someone's behaviour departs from their own baseline or from what HR says about their status.

## How it works

```
fixtures/raw/<source>/page-NNNN.json
        |  connectors/   fetch pages, normalize() each record
        v
     Event  (user, ts UTC, Action, bytes, target, source, attrs)
        |  legacy/dlp_rules.py   every event is scanned by the v1 rule engine; hits become alerts
        v
   signals/   @signal registry; one finding per user per day per signal
        |       reads baselines/ (SQLite rolling daily stats) and hr/ (roster)
        v
   scoring.py   weight * strength, weights in config.py
        v
   alerts/   AlertStore (SQLite)   ->   notify/   Notifier (console, Slack outbox)
```

* `python -m insiderwatch replay fixtures/raw --until 2026-09-30` processes raw logs day by day.
* `python -m insiderwatch alerts [--user EMAIL] [--json]` lists alerts.
* `python -m insiderwatch outbox` shows queued Slack messages.

State lives in one SQLite file (`--db`, default `insiderwatch.db`). Tests: `python -m pytest`.
See `CONTRIBUTING.md` before adding code.
* `python -m insiderwatch risk` ranks users by decayed risk; `export --format csv|jsonl` dumps alerts;
  `check fixtures/raw` dry-runs the connectors and warns about directories nobody claims.
* `python -m insiderwatch cases [--user U] [--json]` lists alert cases (alerts grouped per user and time
  window); `cases close <id>` closes one. Notifications are sent when a case opens or escalates.
