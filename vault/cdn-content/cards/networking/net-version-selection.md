---
id: net-version-selection
node: networking.http-versions
type: qa
---
## Q
Why is "HTTP/3 is newer, so force it everywhere" a bad rollout policy?

## A
Protocol value depends on network path, client support, UDP reachability, loss, CPU cost, and implementation maturity. Negotiate with ALPN/Alt-Svc, keep fallback to HTTP/2, and compare TTFB, completion time, handshake success, retransmission/loss, CPU, and error rate by geography and client. Roll out progressively; averages can hide a harmed network segment.

## Q zh
为什么“HTTP/3 更新，所以所有流量都强制使用”是糟糕 rollout policy？

## A zh
protocol 价值取决于 network path、client support、UDP reachability、loss、CPU cost 与 implementation maturity。通过 ALPN/Alt-Svc 协商，保留 HTTP/2 fallback，并按 geography/client 比较 TTFB、completion time、handshake success、retransmission/loss、CPU、error rate。应 progressive rollout，因为 average 会掩盖受损的网络群体。
