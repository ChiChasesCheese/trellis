---
nodes: [problems.media.video-conferencing, networking.realtime]
tags: [problem]
---
# Drill: Design a video conferencing service (Zoom)

Design the backend for a Zoom-class video conferencing service: participants join a
meeting from arbitrary networks, see and hear each other with low latency, the system
degrades gracefully on bad networks, and it scales from 1:1 calls to large webinars.

**Constraints to state and honor**
- 300M DAU, 1.2 meetings/user/day, 32-minute average meeting, ~8M average concurrent
  participants (via Little's Law) and ~32M peak concurrent participants at a 4x factor.
- Each participant's stream costs ~1.54 Mbps (1.5 Mbps video + 40 kbps audio); a full
  mesh topology already breaks a typical home uplink by N=6 participants.
- An assumed 15% of participant connections cannot establish a direct path and require
  TURN relay — a mandatory, separately-provisioned tier, not a rare fallback.
- The signalling plane (WebSocket control) and media plane (UDP/SRTP) are decoupled
  systems with very different scaling profiles.

**Grading points**
- Computes mesh bandwidth for a given N and explains why it scales with N² in aggregate
  and breaks a typical uplink well before N reaches double digits
  ([[problems-video-conferencing-mesh-bandwidth-n-squared]]).
- Splits signalling and media into decoupled systems and explains the failure-mode
  benefit: a signalling outage doesn't interrupt already-flowing media
  ([[problems-video-conferencing-signalling-media-plane-split]]).
- Compares SFU and MCU on where they push cost (server CPU for MCU via decode+encode vs.
  near-zero-compute packet forwarding for SFU) and computes an approximate core cost for
  a stated meeting size ([[problems-video-conferencing-sfu-vs-mcu-compute-cost]]).
- Explains why TURN relay must be provisioned as a mandatory tier (not an edge case) and
  why a relay server's effective capacity is lower than a plain forwarding node's
  ([[problems-video-conferencing-turn-relay-mandatory-fallback]]).
- Uses simulcast/SVC plus a bounded visible-tile count to keep SFU downlink bandwidth
  independent of meeting size, and can compute the resulting downlink figure
  ([[problems-video-conferencing-simulcast-tile-cap-bounds-downlink]]).
- States the bad-network degradation order (resolution → frame rate → video off → audio
  last) and justifies it by the cost/value asymmetry between audio and video
  ([[problems-video-conferencing-degradation-order-audio-last]]).
- Explains that a single SFU node crash only affects the participants assigned to it
  (ICE restart, reassignment), not the whole meeting, and why splitting media forwarding
  across many nodes produces that isolated blast radius
  ([[problems-video-conferencing-sfu-node-failure-isolated-blast-radius]]).
- Designs cascaded regional SFUs for a large meeting and explains why inter-region
  backbone traffic scales with (presenters × regions) rather than audience size
  ([[problems-video-conferencing-cascaded-sfu-decouples-backbone-from-audience]]).

**Solution**: [[solution-video-conferencing]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
