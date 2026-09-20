%% trellis:begin %%
# Ride Hailing (Uber)
*Design Problems / Location & Mobility*

Driver location ingestion, matching under contention, trip state machines and surge.

**Requires:** [[domains/system-design/map/distributed.consistency|Consistency Models]], [[domains/system-design/map/networking.realtime|Realtime Delivery]]

## Readings
- [[solution-ride-hailing|设计题解：网约车（Ride Hailing，Uber）]]
- [[src-google-s2|S2 Geometry Library]]
- [[src-hellointerview-uber|Uber]]
- [[src-highscalability-uber-dispatch|How Uber Scales Their Real-time Market Platform]]
- [[src-karanpratapsingh-uber|Uber]]
- [[src-uber-blog-dynamic-pricing|Behind the surge: how Uber's dynamic pricing works]]
- [[src-uber-blog-h3|H3: Uber's Hexagonal Hierarchical Spatial Index]]
- [[src-uber-investor-q4-2025|Uber Announces Results for Fourth Quarter and Full Year 2025]]

## Drills
- [[design-ride-hailing|Drill: Design a ride-hailing backend like Uber]]

## Cards (7)
1. [[problems-ride-hailing-ingestion-vs-matching-order-of-magnitude]]
2. [[problems-ride-hailing-exclusive-lock-not-optimistic]]
3. [[problems-ride-hailing-websocket-bidirectional]]
4. [[problems-ride-hailing-surge-streaming-precompute]]
5. [[problems-ride-hailing-hexagon-supply-demand-gradient]]
6. [[problems-ride-hailing-lock-outage-no-safe-fallback]]
7. [[problems-ride-hailing-10x-shared-shard-key]]
%% trellis:end %%

## Notes
