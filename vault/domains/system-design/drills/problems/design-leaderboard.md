---
nodes: [problems.realtime.leaderboard, caching.strategies]
tags: [problem]
---
# Drill: Design a real-time leaderboard

Design the backend for a game's real-time leaderboard: millions of players' scores update
continuously, anyone can view the global top ranks, and any player can look up their own
current rank. Cover the write path, whether/when to shard, rank queries, tie-breaking,
time-windowed boards, friends-only boards, durability and cheating.

**Constraints to state and honor**
- 30M DAU, 5 matches/player/day average, ~10,417 peak write QPS and ~31,250 peak read QPS
  (read:write ≈ 3:1) at a 6x evening-peak factor.
- The full 150M-account leaderboard costs only ~17GB as a Redis sorted set — memory is not
  what forces sharding here.
- Redis executes commands on a single thread; a conservative, derated sustainable ceiling
  per primary (~50,000 op/s) still leaves the peak write path ~4.8x headroom at this scale
  — a single primary with read replicas is the correct baseline, not a sharded cluster.
- Scores are written only by a trusted backend match-settlement service, never submitted
  directly by the game client.

**Grading points**
- Explains why neither the leaderboard's memory footprint nor its throughput forces
  sharding at the stated scale, and computes the single-primary headroom instead of
  defaulting to a sharded design ([[problems-leaderboard-memory-vs-single-thread-ceiling]]).
- Once write throughput would outgrow a single primary, chooses score-range sharding over
  player-id sharding, and explains how a per-shard member count turns "what's my global
  rank" back into a cheap operation ([[problems-leaderboard-score-range-sharding-rank-sum]]).
- Justifies giving the top of the leaderboard reads from the primary (strong freshness)
  while the rest read from replicas, and — once sharded — shifts the long tail to an
  approximate, periodically-recomputed rank tied to who actually needs precision
  ([[problems-leaderboard-exact-top-approx-long-tail]]).
- Designs a tie-break that encodes a secondary ordering signal into the sorted-set score
  itself, and can justify the numeric precision headroom for doing so
  ([[problems-leaderboard-composite-score-tiebreak]]).
- Designs a friends-only leaderboard by batch-scoring a bounded friend list at read time,
  rejects a dedicated sorted set per user, and names the analogous fan-out trade-off from
  social feed design ([[problems-leaderboard-friends-board-read-time-vs-dedicated-set]]).
- Uses one independently-keyed sorted set per time window (day/week) rather than clearing
  a single set in place, and explains what a reset actually means under this design
  ([[problems-leaderboard-time-windowed-keys-not-in-place-reset]]).
- Treats the sorted sets as a rebuildable cache over an authoritative append-only event
  log, and can state what recovery capability is lost without that separation
  ([[problems-leaderboard-sorted-set-rebuildable-cache]]).
- States the structural anti-cheat design (server-authoritative score submission) and
  distinguishes it from after-the-fact anomaly detection
  ([[problems-leaderboard-server-authoritative-score-submission]]).

**Solution**: [[solution-leaderboard]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
