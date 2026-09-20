%% trellis:begin %%
# Real-Time Leaderboard
*Design Problems / Real-Time, Compute & AI Services*

Rank millions of players live: sorted sets, sharded rankings and approximate rank.

**Requires:** [[domains/system-design/map/caching.strategies|Write & Read Strategies]]

## Readings
- [[solution-leaderboard|设计题解：实时排行榜（Real-Time Leaderboard）]]
- [[src-redis-benchmark-leaderboard|Redis benchmark (redis-benchmark and Redis's single-threaded architecture)]]
- [[src-redis-docs-sorted-sets-leaderboard|Redis sorted sets]]
- [[src-redis-solutions-leaderboard|Real-time leaderboard & ranking solutions (Redis)]]
- [[src-systemdesignone-leaderboard|Leaderboard System Design (systemdesign.one)]]

## Drills
- [[design-leaderboard|Drill: Design a real-time leaderboard]]

## Cards (8)
1. [[problems-leaderboard-memory-vs-single-thread-ceiling]]
2. [[problems-leaderboard-score-range-sharding-rank-sum]]
3. [[problems-leaderboard-exact-top-approx-long-tail]]
4. [[problems-leaderboard-composite-score-tiebreak]]
5. [[problems-leaderboard-time-windowed-keys-not-in-place-reset]]
6. [[problems-leaderboard-friends-board-read-time-vs-dedicated-set]]
7. [[problems-leaderboard-sorted-set-rebuildable-cache]]
8. [[problems-leaderboard-server-authoritative-score-submission]]
%% trellis:end %%

## Notes
