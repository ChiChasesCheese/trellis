%% trellis:begin %%
# Unique ID Generator
*Design Problems / Building Blocks & Warm-ups*

Roughly time-ordered 64-bit ids with no coordinator on the hot path; clock skew and sequence exhaustion.

**Requires:** [[domains/system-design/map/distributed.time.clocks|Clocks & Timestamps]]

## Readings
- [[solution-unique-id-generator|设计题解：唯一 ID 生成器（Unique ID Generator）]]
- [[src-instagram-unique-id-generator|Sharding & IDs at Instagram]]
- [[src-rfc9562-unique-id-generator|RFC 9562 — Universally Unique IDentifiers (UUIDs)]]
- [[src-twitter-unique-id-generator|Announcing Snowflake]]

## Drills
- [[design-unique-id-generator|Drill: Design a unique ID generator]]

## Cards (8)
1. [[problems-unique-id-generator-sequence-bits-not-bottleneck]]
2. [[problems-unique-id-generator-worker-id-bits-from-deployment-count]]
3. [[problems-unique-id-generator-embedded-vs-service-placement]]
4. [[problems-unique-id-generator-clock-rollback-refuse]]
5. [[problems-unique-id-generator-two-exhaustion-scales]]
6. [[problems-unique-id-generator-uuidv7-collision-math]]
7. [[problems-unique-id-generator-lease-coordinator-outage]]
8. [[problems-unique-id-generator-sign-bit-boundary]]
%% trellis:end %%

## Notes
