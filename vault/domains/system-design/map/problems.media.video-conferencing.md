%% trellis:begin %%
# Video Conferencing (Zoom)
*Design Problems / Media, Files & Collaboration*

Real-time media: SFU vs MCU, signalling, NAT traversal, and degrading gracefully on bad networks.

**Requires:** [[domains/system-design/map/networking.realtime|Realtime Delivery]]

## Readings
- [[solution-video-conferencing|设计题解：视频会议（Video Conferencing，Zoom）]]
- [[src-discord-video-conferencing|How Discord Handles Two and a Half Million Concurrent Voice Users using WebRTC]]
- [[src-gcc-video-conferencing|Google Congestion Control (draft-ietf-rmcat-gcc-02)]]
- [[src-rfc8445-video-conferencing|RFC 8445 — Interactive Connectivity Establishment (ICE)]]
- [[src-rfc8656-video-conferencing|RFC 8656 — Traversal Using Relays around NAT (TURN)]]
- [[src-rfc9605-video-conferencing|RFC 9605 — SFrame]]

## Drills
- [[design-video-conferencing|Drill: Design a video conferencing service (Zoom)]]

## Cards (8)
1. [[problems-video-conferencing-mesh-bandwidth-n-squared]]
2. [[problems-video-conferencing-signalling-media-plane-split]]
3. [[problems-video-conferencing-sfu-vs-mcu-compute-cost]]
4. [[problems-video-conferencing-turn-relay-mandatory-fallback]]
5. [[problems-video-conferencing-simulcast-tile-cap-bounds-downlink]]
6. [[problems-video-conferencing-degradation-order-audio-last]]
7. [[problems-video-conferencing-sfu-node-failure-isolated-blast-radius]]
8. [[problems-video-conferencing-cascaded-sfu-decouples-backbone-from-audience]]
%% trellis:end %%

## Notes
