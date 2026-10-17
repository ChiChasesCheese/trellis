# Task: amazon.amz-emergency-pubsub

- **Leaf id**: `amazon.amz-emergency-pubsub`   **slug**: `amz-emergency-pubsub`   **kind**: problem
- **题目**: 应急事件发布订阅（Emergency Pub/Sub）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- Hello Interview `publish-subscribe-system` report 2026-10-01 mid-level: 'There is a need for an emergency response system where some components will subscribe/listen to emergency events and others will publish/notify those events. Implement a class/component that would handle the publish and subscribe logic.' https://www.hellointerview.com/community/questions?company=Amazon (question slug `publish-subscribe-system`) [medium–high]
- 1p3a question bank `pub-sub-system-ood` (onsite-coding, 2 sources, 2026-05-13..05-22; oop-design, pubsub, messaging, concurrency) [medium]
- kit forums LC6841317 (SDE II): 'event forwarding framework … batch, slow events, failures must not block others' [high, older]

## (reconstructed) — not in any visible report

- event types and severities, topic filtering, priority delivery, retry/dead letter, async delivery stage

## Reuse / link (our own repo first)

- bank [[solution-pub-sub]] (the generic in-process queue — link, do not re-teach; this leaf is the emergency-domain version with failure isolation and severity)
- concept leaf patterns.observer

## Card ladder notes

- ladder; step 7 = a subscriber that raises must not stop the others (concrete event, three subscribers, one raises); step 8 = slow subscriber → per-subscriber queue/worker
