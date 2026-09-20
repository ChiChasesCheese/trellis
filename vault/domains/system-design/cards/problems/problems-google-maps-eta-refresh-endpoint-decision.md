---
id: problems-google-maps-eta-refresh-endpoint-decision
node: problems.geo.google-maps
type: qa
step: 2
tags: [grown]
---
## Q
In a Google Maps-style navigation design, why does the API expose a separate lightweight `eta-refresh` endpoint for in-trip updates instead of having the client call the same route-planning endpoint it used to start the trip?

## A
The route-planning endpoint does a full point-to-point search over the road graph plus a heavy ETA-model inference combining live traffic and historical patterns, sized for the much lower request rate of trips being started. In-trip refreshes happen far more often than new trips start (about 40x more often at typical trip-length and refresh-interval assumptions), and the client's position and remaining route are already known, so a refresh only needs to apply the latest traffic delta to the remaining legs of the existing route rather than re-searching the graph from scratch — treating it as a distinct, cheap endpoint keeps the expensive full-planning path sized for its actual (much lower) load.

## Q zh
在一个类 Google Maps 的导航设计中，为什么 API 要为行程中的更新单独暴露一个轻量的 `eta-refresh` 端点，而不是让客户端复用它一开始发起行程时调用的路线规划端点？

## A zh
路线规划端点要在路网图上做一次完整的点对点搜索，还要跑一次结合实时路况和历史模式的重量级 ETA 模型推理，它的容量是按发起新行程这个低得多的请求速率设计的。行程中的刷新请求远比新行程的发起频繁（在典型的行程时长和刷新间隔假设下约高出 40 倍），而且此时客户端的位置和剩余路线已经知道，一次刷新只需要把最新的路况增量应用到既有路线的剩余路段上，不需要在图上重新搜索——把它做成一个独立的轻量端点，能让昂贵的完整规划路径按它真实（低得多）的负载来设计容量。
