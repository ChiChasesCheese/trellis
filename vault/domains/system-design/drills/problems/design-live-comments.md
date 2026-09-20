---
nodes: [problems.social.live-comments, networking.realtime]
tags: [problem]
---
# Drill: Design a live-comments broadcast system

Design the system behind comments on a live video: viewers watching the same stream post
comments, and every other viewer currently connected — anywhere from a few hundred to ten
million on the biggest streams — should see new comments in near real time.

**Constraints to state and honor**
- Peak: 10M concurrent viewers on one video, ~167 comments/sec produced for that video.
- Naive full broadcast implies ~1.67B delivery events/sec platform-wide for that one
  video — not achievable on any real fleet.
- Broadcast delivery target: P99 < 2s to other online viewers. A late-joining viewer needs
  context, not a full replay of everything posted before they joined.
- Viewer-to-server traffic (posting) is rare per viewer; server-to-viewer (broadcast) is
  the dominant direction.

**Grading points**
- Picks SSE over WebSockets for the broadcast direction and justifies it from the traffic
  asymmetry rather than by default, citing SSE's reconnect/resume mechanics
  ([[problems-live-comments-sse-vs-websocket]], [[networking-sse-mechanics]], [[networking-realtime-transport-choice]]).
- Computes the fan-out amplification (comments/sec × concurrent viewers) and uses that
  number, not intuition, to justify why the naive design is impossible at this scale
  ([[problems-live-comments-fanout-amplification]]).
- Uses a dispatcher + subscription registry so a comment is forwarded only to the gateways
  that actually hold viewers of that video, not broadcast to the whole fleet
  ([[problems-live-comments-dispatcher-subscription-registry]]).
- For the mega-stream case, samples/rate-limits the broadcast itself (not per-connection
  throttling) and can compute the required sampling ratio from a target per-gateway push
  rate ([[problems-live-comments-sampling-ratio]]).
- Scopes ordering to a per-video monotonic sequence number backed by partition-level
  ordering, not global linearizability across viewers
  ([[problems-live-comments-per-video-ordering]]).
- Gives late joiners a fixed-size recent window (not a full backlog replay) and reuses the
  same mechanism for reconnection after a drop ([[problems-live-comments-catchup-recent-n]]).
- Explains why a viral video's hot spot can't be mitigated by spreading load across more
  shard keys the way a hot key elsewhere can, and names the two levers that remain
  (sampling and co-location) ([[problems-live-comments-single-video-hotspot]]).
- States what changes at 10x peak viewers (sampling ratio tightens by another order of
  magnitude, not just "add more gateways") and its product consequence
  ([[problems-live-comments-10x-sampling-tightens]]).

**Solution**: [[solution-live-comments]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
