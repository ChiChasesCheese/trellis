---
id: problems-google-maps-eta-refresh-vs-route-qps
node: problems.geo.google-maps
type: qa
step: 1
tags: [grown]
---
## Q
In a Google Maps-style navigation design where the average trip lasts 20 minutes and the client polls for an updated ETA every 30 seconds, why does the average request rate for in-trip ETA refreshes end up about 40x higher than the average request rate for initial route requests, and what does that ratio imply for the system's architecture?

## A
A single navigation session issues one initial route request but roughly (20*60)/30 = 40 ETA-refresh requests over the course of the trip, so refresh traffic scales with trip duration divided by refresh interval while route-request traffic scales with the number of trips started — at these parameters the refresh stream is about 40x the route-request stream. This means the in-trip refresh path must be a cheap, separate operation from full route planning: if every refresh re-ran a complete point-to-point route search, the dominant cost in the whole system would be redundant re-planning of routes that mostly haven't changed, so refreshes need to be incremental updates against the already-computed route instead.

## Q zh
在一个类 Google Maps 的导航设计中，假设平均单次行程 20 分钟，客户端每 30 秒轮询一次 ETA 更新，为什么行程中 ETA 刷新请求的平均速率会比初始路线请求的平均速率高出约 40 倍？这个比例对系统架构有什么含义？

## A zh
一次导航会话只发起一次初始路线请求，但整趟行程会产生大约 (20×60)/30 = 40 次 ETA 刷新请求——也就是说刷新流量随「行程时长 / 刷新间隔」扩展，而路线请求流量只随「发起的行程数」扩展，在这组参数下刷新流量约是路线请求流量的 40 倍。这意味着行程中的刷新路径必须是一个和完整路径规划分离、代价很轻的操作：如果每次刷新都重新做一次完整的点对点路径搜索，整个系统里最大的开销会变成对大概率没怎么变化的路线做冗余的重新规划——刷新应该是针对已经算好的路线做增量更新，而不是重新规划。
