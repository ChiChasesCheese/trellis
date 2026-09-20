---
nodes: [problems.media.email-service, storage.search]
tags: [problem]
---
# Drill: Design an email service (Gmail)

Design the backend for a Gmail-class email service: users send and receive mail with
external senders over SMTP, organize a per-user mailbox, search their own mail history,
and are protected from spam and phishing before it reaches the inbox.

**Constraints to state and honor**
- 1.5B DAU, 20 received / 3 sent messages per user per day on average, ~347K avg / ~1.39M
  peak receive QPS and ~52K avg / ~208K peak send QPS at a 4x peak factor.
- New attachment bytes accumulate at roughly 9x the rate of new metadata bytes per year —
  attachments, not message text, are the storage bottleneck, and must be content-addressed
  and deduplicated at the point of sending, not per received copy.
- Once accepted with SMTP's `250`, a message's delivery is this service's responsibility,
  not the sender's — outbound retry state must be partitioned per destination domain.
- Each mailbox's search corpus is isolated by product semantics, so it can be sharded by
  user id with no cross-shard fan-out.

**Grading points**
- Explains why attachments dominate storage growth (~9x metadata) and why deduplication
  must be modeled off send events, not received copies, to avoid overcounting unique bytes
  ([[problems-email-service-attachment-dominates-storage]]).
- Splits mailbox storage into an immutable Message table and a separate per-user mutable
  MailboxEntry table, and explains why this keeps marking a message read cheap
  ([[problems-email-service-immutable-message-mutable-mailboxentry]]).
- States what SPF, DKIM and DMARC each actually prove as distinct claims, and can explain
  why a phishing email can pass SPF and DKIM while still being caught by DMARC
  ([[problems-email-service-spf-dkim-dmarc-distinct-proofs]]).
- Partitions the outbound retry queue per destination domain rather than using one global
  FIFO queue, and can compute the steady-state in-flight retry volume from an arrival rate
  and average dwell time via Little's Law ([[problems-email-service-per-destination-retry-queue-depth]]).
- Explains that per-user search sharding doesn't eliminate the sharding problem a global
  search engine faces — it trades fan-out/tail-latency for a hot-shard (oversized mailbox)
  problem instead ([[problems-email-service-per-user-search-sharding-changes-problem]]).
- Chooses fail-open over fail-closed for the async spam/phishing classifier when it's
  unavailable, and justifies it by which failure is recoverable after the fact
  ([[problems-email-service-spam-classifier-fail-open]]).
- Explains what a storage quota (15GB-class) is actually protecting against given that a
  median account would take decades to fill it, and places the quota check as a pre-write
  gate rather than a passive storage-overflow condition
  ([[problems-email-service-quota-protects-tail-not-median]]).
- Treats the per-user search index as a rebuildable derived view over the Message store
  (not a source of truth), consistent with why a search cluster is never the system of
  record ([[storage-search-not-sot]]).

**Solution**: [[solution-email-service]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
