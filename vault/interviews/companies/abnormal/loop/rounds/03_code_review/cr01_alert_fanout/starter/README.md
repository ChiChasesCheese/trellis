# fanout

Delivers high-severity alerts to each tenant's configured channels (webhook, email, Slack).

    python -m fanout          # run the worker (FANOUT_DB, FANOUT_QUEUE, FANOUT_CONCURRENCY)
    python -m pytest          # unit tests

Layout: `queue.py` (sqlite queue with SQS semantics), `models.py`, `config_store.py` (tenant channels),
`dedup.py`, `senders/`, `worker.py`.
