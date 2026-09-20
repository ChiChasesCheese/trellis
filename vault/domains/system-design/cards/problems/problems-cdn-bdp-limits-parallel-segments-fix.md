---
id: problems-cdn-bdp-limits-parallel-segments-fix
node: problems.foundations.cdn
type: qa
step: 5
tags: [grown]
---
## Q
Downloading a large file through a CDN over a single HTTP connection with a 40ms round-trip time and 100Mbps available bandwidth is limited to roughly 488KB of data in flight at once (the bandwidth-delay product, 100Mbps x 40ms). Why does splitting the same download into parallel Range-request segments across multiple connections raise achievable throughput well past what one connection can reach?

## A
A single TCP connection's throughput is capped near the bandwidth-delay product because that's how much unacknowledged data can be 'in flight' before the sender must wait for ACKs, and real single-connection throughput is pushed further below the theoretical cap by slow start and any packet loss. Opening multiple parallel connections, each fetching a different byte range of the same object via `Range: bytes=...`, gives each connection its own independent congestion window, so the achievable data-in-flight scales roughly with the number of connections rather than staying capped at one connection's window - for example 6 connections at 30Mbps each combine to about 180Mbps aggregate, well above what one connection achieves alone. This requires the CDN's cache to support serving partial byte ranges from a cached object, not only whole-object hits.

## Q zh
通过 CDN 下载一个大文件时，如果只用单一 HTTP 连接，在 RTT 为 40ms、可用带宽为 100Mbps 的情况下，单连接在路上的数据量大约受限于带宽时延积（bandwidth-delay product）约 488KB（100Mbps × 40ms）。为什么把同一个下载拆成多个并行的 Range 请求分段能把实际吞吐量推到远高于单连接的上限？

## A zh
单一 TCP 连接的吞吐量接近受带宽时延积限制，因为这是发送方在必须等待确认前能「在途」的未确认数据量，而真实单连接吞吐量还会因慢启动和丢包而进一步低于理论上限。开多个并行连接，每个通过 `Range: bytes=...` 拉取同一对象的不同字节范围，每个连接都有自己独立的拥塞窗口，所以在途数据量大致随连接数线性增长，而不是被锁定在单连接的窗口上——例如 6 条连接各自 30Mbps，聚合可以达到约 180Mbps 的聚合吞吐量，远高于单连接单独能达到的水平。这要求 CDN 的缓存能对缓存对象支持部分字节范围的命中，而不只是整对象命中。
