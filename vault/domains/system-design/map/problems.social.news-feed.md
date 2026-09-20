%% trellis:begin %%
# News Feed & Timeline (Twitter/Facebook)
*Design Problems / Social, Feeds & Messaging*

Fan-out on write vs on read, the celebrity problem, ranking, and keeping a timeline fresh and cheap.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/caching.strategies|Write & Read Strategies]], [[domains/system-design/map/async.queues|Message Queues]]

## Readings
- [[solution-news-feed|设计题解：信息流与时间线（News Feed & Timeline，Twitter/Facebook）]]
- [[src-donnemartin-news-feed|System Design Primer — Twitter timeline & search]]
- [[src-hellointerview-news-feed|Design Facebook's News Feed]]
- [[src-highscalability-news-feed|The Architecture Twitter Uses to Deal with 150M Active Users]]
- [[src-meta-engineering-news-feed|News Feed ranking, powered by machine learning]]

## Drills
- [[design-news-feed|Drill: Design a news feed / timeline like Twitter or Facebook]]

## Cards (8)
1. [[problems-news-feed-read-write-ratio-drives-precompute]]
2. [[problems-news-feed-hybrid-fanout-threshold]]
3. [[problems-news-feed-redundant-cache-hot-key]]
4. [[problems-news-feed-multipass-ranking-funnel]]
5. [[problems-news-feed-capped-inbox-vs-unbounded]]
6. [[problems-news-feed-composite-pagination-cursor]]
7. [[problems-news-feed-inbox-cache-outage-degradation]]
8. [[problems-news-feed-10x-physical-shard-inbox]]
%% trellis:end %%

## Notes
