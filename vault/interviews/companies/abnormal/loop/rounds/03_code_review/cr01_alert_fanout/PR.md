# Add notification fan-out worker for high-severity alerts

**Author:** Dana Whitfield (@dwhitfield) · **Reviewers:** you · **Size:** +388 / -2 (18 files, tests included)

## Why

Insider Risk alerts with severity >= 3 currently only show up in the console. Customers (Acme and
Globex first) asked to get them in Slack, by email and on their own webhook endpoints so their SOC
sees them without logging in. This PR adds the worker that does that fan-out.

## What changed

- `fanout/worker.py`: pulls alerts from the alerts queue, drops anything below `min_severity` or older
  than 15 minutes, looks up the tenant's channels, and sends to each one. Sends run on a
  `ThreadPoolExecutor` (`FANOUT_CONCURRENCY`, default 8) so one slow endpoint does not stall a batch.
- `fanout/config_store.py`: per-tenant channel config (sqlite for now, Postgres later).
- `fanout/dedup.py`: in-memory TTL cache so the same alert is not notified twice (the producer
  sometimes emits an alert twice).
- `fanout/senders/`: webhook (real HTTP POST), email and Slack (stubbed behind a `transport` callable).
- `fanout/cli.py`: `python -m fanout` entry point.
- Settings for the above in `fanout/settings.py`.

## Design notes

- We ack (delete) the message as soon as we receive it so that a second worker does not pick it up
  while we are still sending. Sends are retried until they succeed because customers hate missing alerts.
- Dead-lettering is not wired up yet; ops is creating the DLQ this week (see TODO).
- Only one worker process is deployed at the moment, so I kept the dedup cache in memory.

## Tested locally

- `python -m pytest` is green (13 tests).
- Ran the worker against a local queue with 3 alerts and a `python -m http.server` as the webhook;
  all three arrived.
- Not tested against real Slack/SMTP (stubs).

## Rollout

Deploy behind the existing `alerts-fanout` flag, Acme first.
