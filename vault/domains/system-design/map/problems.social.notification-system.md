%% trellis:begin %%
# Notification System
*Design Problems / Social, Feeds & Messaging*

Multi-channel push/SMS/email with preferences, rate caps, retries and deduplication at billions a day.

**Requires:** [[domains/system-design/map/async.queues|Message Queues]], [[domains/system-design/map/correctness.idempotency|Idempotency]]

## Readings
- [[solution-notification-system|设计题解：通知系统（Notification System）]]
- [[src-apple-notification-system|Communicating with APNs]]
- [[src-firebase-notification-system|Set the lifespan of a message]]
- [[src-linkedin-notification-system|Air Traffic Controller: Member-First Notifications at LinkedIn]]
- [[src-twilio-notification-system|Understanding Twilio Rate Limits and Message Queues]]

## Drills
- [[design-notification-system|Drill: Design a multi-channel notification system]]

## Cards (8)
1. [[problems-notification-system-priority-lane-drain-time]]
2. [[problems-notification-system-preference-matrix-model]]
3. [[problems-notification-system-sourceeventid-dedup]]
4. [[problems-notification-system-dedup-window-sizing]]
5. [[problems-notification-system-digest-reduction]]
6. [[problems-notification-system-provider-failover-circuit-breaker]]
7. [[problems-notification-system-preference-service-outage-degradation]]
8. [[problems-notification-system-sms-quota-bottleneck-10x]]
%% trellis:end %%

## Notes
