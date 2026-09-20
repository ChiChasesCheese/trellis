%% trellis:begin %%
# Photo Sharing (Instagram)
*Design Problems / Social, Feeds & Messaging*

Upload and media processing, feed generation, and serving images globally.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/storage.object|Object Storage & Separation]], [[domains/system-design/map/networking.cdn|CDN]]

## Readings
- [[solution-instagram|设计题解：图片分享（Photo Sharing，Instagram）]]
- [[src-algomaster-instagram|Design Instagram]]
- [[src-instagram-engineering-sharding-ids|Sharding & IDs at Instagram]]
- [[src-meta-engineering-instagram|Reducing Instagram's basic video compute time by 94 percent]]
- [[src-usenix-haystack-instagram|Finding a Needle in Haystack: Facebook's Photo Storage]]

## Drills
- [[design-instagram|Drill: Design a photo/video sharing app like Instagram]]

## Cards (8)
1. [[problems-instagram-read-write-ratio-forces-cdn]]
2. [[problems-instagram-presigned-url-direct-upload]]
3. [[problems-instagram-repackage-vs-retranscode]]
4. [[problems-instagram-small-file-metadata-problem]]
5. [[problems-instagram-origin-shield-request-coalescing]]
6. [[problems-instagram-media-status-gates-fanout]]
7. [[problems-instagram-transcode-worker-failure-isolation]]
8. [[problems-instagram-100x-storage-tiering]]
%% trellis:end %%

## Notes
