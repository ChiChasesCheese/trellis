---
nodes: [problems.social.instagram, storage.object, networking.cdn]
tags: [problem]
---
# Drill: Design a photo/video sharing app like Instagram

Design the upload, processing, and serving path for a photo-and-video sharing app with
150M daily active users. Assume the follow graph, fan-out, and feed ranking are already
solved exactly as in a generic news feed design — focus this attempt on everything specific
to media: upload, transcoding, storage, and global serving.

**Constraints to state and honor**
- ~7.5M uploads/day (80% photos, 20% short ~15s videos); ~87 average upload QPS.
- Image views while scrolling the feed run at roughly 8,000x the upload QPS — almost all
  read traffic must be absorbed by the CDN, not the application tier.
- Media must reach "publishable" (all derivatives ready) at P90 < 10s after upload
  completes; a post must never appear in a follower's feed pointing at unprocessed media.
- Total media storage is on the order of tens of terabytes per day at this scale, with
  video contributing a disproportionate share relative to its share of uploads.

**Grading points**
- Uses pre-signed URLs for direct client-to-object-store upload instead of proxying media
  bytes through the application server ([[problems-instagram-presigned-url-direct-upload]]).
- Reduces video transcoding cost by repackaging already-encoded frame data into adaptive
  bitrate renditions instead of re-transcoding each rendition from scratch, and can state
  the rough order-of-magnitude difference this makes
  ([[problems-instagram-repackage-vs-retranscode]]).
- Explains why per-photo metadata overhead — not raw data throughput — is the bottleneck a
  naive one-file-per-photo storage layer runs into at billions of photos, and why most
  systems don't need to build a custom fix for it themselves
  ([[problems-instagram-small-file-metadata-problem]]).
- Designs the CDN as pull-based with an origin shield that coalesces concurrent cache
  misses for the same freshly-published object into one origin fetch
  ([[problems-instagram-origin-shield-request-coalescing]]).
- Gates fan-out on a media-readiness status so a post never reaches followers before its
  derivatives are ready ([[problems-instagram-media-status-gates-fanout]]).
- States the read-to-write ratio and explains why it forces almost all traffic onto the CDN
  rather than an application-layer cache ([[problems-instagram-read-write-ratio-forces-cdn]]).
- Identifies that a transcoding worker pool outage degrades only the write/publish path, not
  reads of already-published media ([[problems-instagram-transcode-worker-failure-isolation]]).
- Proposes hot/warm/cold storage tiering as the system scales, and explains why the cost
  question shifts from capacity to access frequency ([[problems-instagram-100x-storage-tiering]]).

**Solution**: [[solution-instagram]] — attempt first, then read. For the fan-out and
ranking mechanism this design reuses, see the News Feed & Timeline solution article.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
