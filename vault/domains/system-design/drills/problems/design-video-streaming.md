---
nodes: [problems.media.video-streaming]
tags: [problem]
---
# Drill: Design a video-on-demand streaming platform like YouTube

Design the upload, transcoding and playback distribution paths for a UGC video platform:
creators upload videos of arbitrary length, the system produces an adaptive bitrate
ladder, and viewers around the world stream with a low startup delay and few stalls.

**Constraints to state and honor**
- 500 hours of video uploaded per minute platform-wide; 150M DAU averaging 40 minutes of
  watch time per day.
- Peak concurrent viewers reach roughly 12.5M, at an average blended bitrate of 3 Mbps.
- Never lose a confirmed upload's master file, even though the playback path may serve
  stale or partially-ready renditions during processing.
- Live streaming, search, recommendations and DRM key management are out of scope.

**Grading points**
- Models a Video as owning multiple independent VideoAsset (rendition) records rather
  than fixed fields, so partially-ready renditions can be published incrementally ([[problems-video-streaming-video-asset-model]]).
- Splits the transcode pipeline into a DAG of independent per-rendition jobs so one
  rendition's failure doesn't block or invalidate the others ([[problems-video-streaming-dag-failure-isolation]]).
- Computes the bitrate-ladder storage amplification (~6.1x the master) and derives a
  tiered/long-tail transcoding policy from it rather than transcoding every upload into
  the full ladder ([[problems-video-streaming-ladder-storage-amplification]], [[problems-video-streaming-long-tail-lazy-transcode]]).
- Computes peak playback egress bandwidth and explains why it rules out serving playback
  directly from an origin data center, requiring CDN edge distribution ([[problems-video-streaming-peak-egress-cdn]]).
- Argues per-title vs. per-shot encoding as a real cost/benefit trade-off, not just "use
  a smarter codec" ([[problems-video-streaming-per-title-vs-per-shot]]).
- Justifies a hybrid CDN strategy (self-operated edge network for head-of-catalog traffic,
  third-party CDN for long tail) with the economics behind each choice ([[problems-video-streaming-cdn-build-vs-buy]]).
- Designs a client ABR policy that treats startup and steady-state playback as separate
  problems with different selection logic ([[problems-video-streaming-abr-two-phase]]).
- Calls out at least one failure mode (transcode worker/orchestrator failure, CDN edge
  node failure, origin object storage outage) and states how the system degrades.

**Solution**: [[solution-video-streaming]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
