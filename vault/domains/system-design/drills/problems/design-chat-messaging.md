---
nodes: [problems.social.chat-messaging, networking.realtime, async.queues]
tags: [problem]
---
# Drill: Design a chat and messaging system (WhatsApp-style)

Design a persistent-connection messaging platform for one-on-one and group chat
(groups up to 500 members), with delivery receipts, in-conversation ordering,
offline message sync, and presence. Target roughly 300 million DAU.

**Constraints to state and honor**
- 300 million DAU, ~50 messages/user/day (~15 billion messages/day, ~174k/s
  average, ~520k/s peak).
- ~45 million peak concurrent persistent connections.
- End-to-end delivery P99 < 200ms same-region for online users; at-least-once
  delivery with client-side dedup, never a false "sent" acknowledgment.
- Group fan-out must not multiply message-body storage by group size.

**Grading points**
- Sizes the stateful gateway fleet from concurrent connections (not message
  throughput), and states a connections-per-box assumption ([[problems-chat-messaging-gateway-connection-capacity]]).
- Chooses one message copy plus a narrow per-recipient delivery-status row
  over per-recipient message duplication, and can justify it with a number ([[problems-chat-messaging-group-fanout-storage-model]]).
- Explains how a sender's gateway finds which gateway holds an online
  recipient's socket, and why a session directory beats a per-user queue/topic
  for that job ([[problems-chat-messaging-session-directory-routing]]).
- Gets message ordering right: per-conversation monotonic sequence, not a
  global order and not client timestamps ([[problems-chat-messaging-per-conversation-ordering]]).
- Has an idempotency mechanism so client retries cannot double-persist or
  double-deliver a message ([[problems-chat-messaging-idempotent-send]]).
- States a concrete threshold for when group fan-out must move from
  synchronous push to an async queue, and ties it to a latency budget ([[problems-chat-messaging-sync-vs-async-fanout-threshold]]).
- Names at least one real failure mode (hot partition from a large/active
  conversation) and its mitigation ([[problems-chat-messaging-hot-partition-time-bucketing]]).
- Describes what changes at 10x scale, including why presence must tighten
  further, not just "add more servers" ([[problems-chat-messaging-ten-x-evolution]]).

**Solution**: [[solution-chat-messaging]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
