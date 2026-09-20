---
nodes: [problems.social.notification-system, async.queues, correctness.idempotency]
tags: [problem]
---
# Drill: Design a multi-channel notification system

Design a notification system that fans out push (APNs/FCM), SMS (Twilio-class) and email
(SendGrid-class) notifications to 500M DAU, triggered both by synchronous business-service
calls and by async event streams. It must respect per-type channel preferences and
per-user quiet hours, and must never let a marketing blast delay an OTP.

**Constraints to state and honor**
- 500M DAU, ~5 notifications/user/day → ~2.5B/day, average QPS ≈ 28,935, peak (×4) ≈ 115,741.
- Transactional notifications (OTP, security alerts): P99 < 5s end to end. Marketing
  notifications: no hard latency SLA, minutes to hours for a full campaign is acceptable.
- SMS is the scarcest channel: a long code is limited to 1 message/second, a short code to
  100/second (Twilio-documented).
- At-least-once delivery from every retry path (client, queue, provider); the same logical
  notification must never be double-sent because of a retry on our side.

**Grading points**
- Separates transactional and marketing traffic into physically independent queues and
  worker pools (not a priority field on one shared queue) and can quantify why a shared
  queue fails the OTP SLA ([[problems-notification-system-priority-lane-drain-time]]).
- Models preferences as a (notificationType, channel) matrix rather than a single
  per-user channel toggle ([[problems-notification-system-preference-matrix-model]]).
- Uses a business-meaningful `sourceEventId` as the idempotency key, generated once per
  triggering event and reused across retries, not minted fresh per HTTP call
  ([[problems-notification-system-sourceeventid-dedup]], [[correctness-idempotency-key-design]]).
- Sizes the dedup retention window from the longest documented downstream retry/queue
  window rather than picking an arbitrary duration
  ([[problems-notification-system-dedup-window-sizing]], [[correctness-dedup-window]]).
- Batches high-volume, mergeable notification types (likes, follows) into windowed digests
  and can compute the reduction factor, while keeping transactional types un-digested
  ([[problems-notification-system-digest-reduction]]).
- Normalizes each provider's error codes behind a unified channel-adapter interface with
  per-provider rate limiters and circuit breakers, and fails over to a backup provider
  without business logic knowing ([[problems-notification-system-provider-failover-circuit-breaker]]).
- States an asymmetric degradation plan when the preference/quiet-hours service is down:
  transactional sends proceed on defaults, marketing sends defer
  ([[problems-notification-system-preference-service-outage-degradation]]).
- Identifies that at 10x scale the SMS channel's provider-side rate limits become the
  bottleneck before compute or storage do, and proposes multi-provider, region-sharded
  pooling as the fix ([[problems-notification-system-sms-quota-bottleneck-10x]]).

**Solution**: [[solution-notification-system]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
