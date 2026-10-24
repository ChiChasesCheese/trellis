# Task — backend fundamentals (八股) for TikTok / ByteDance, group K3

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only
`vault/interviews/core/fundamentals/tiktok/tiktok-fundamentals.md` (the index page) and one page per topic in the same
folder. Learning pages: `proposals/WRITING_RULES.md` strictly; Chinese, English terms; senior bar.

Topics (from `research/companies/tiktok/catalog/CATALOG.md` §3, most asked first): Redis (distributed lock with SET NX +
Lua, watchdog, RedLock and its critique, data structures, persistence), MySQL (B+ tree indexes, isolation / MVCC / gap
locks, slow queries, deep paging), cache problems (penetration / breakdown / avalanche, cache-aside consistency, hot
and big keys), message queues (Kafka partitions, rebalance, ordering, no-loss, backlog, dead letter), idempotency and
distributed transactions (TCC, SAGA, outbox), runtime and concurrency (Java ConcurrentHashMap / thread pools / GC, Go
GMP, Python GIL), networking and OS (TCP handshake / TIME_WAIT, TLS, DNS, what happens when you open a URL, virtual
memory), Linux troubleshooting (disk full, high CPU, network), service protection (rate limit, degrade, circuit breaker,
retry with backoff, a 10x QPS spike).

Each page: the 8–15 questions interviewers ask on the topic, each with a rehearsable answer (mechanism → why → the
number or trade-off → the follow-up and its answer). The index lists the topics with links and a 5-line "how this part
of the hour goes". Gate: `plain_style.py`, `phone_diagrams.py`, `check_wikilinks.py interviews/core/fundamentals/tiktok`.
Reply ≤ 6 lines.
