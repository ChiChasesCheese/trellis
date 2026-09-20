---
id: problems-proximity-nearby-friends-pull-vs-push
node: problems.geo.proximity
type: qa
step: 6
tags: [grown]
---
## Q
In a nearby-friends feature where users report their location roughly every 15 seconds and have an average of 150 friends with about 15 online at once, why does a pull model (compute nearby friends only when queried) beat a push model (notify all friends on every location update) as the default design, even though it means friends don't get instantly notified when someone enters range?

## A
A push model's fan-out cost scales with location update rate times online friends per user, which in this scenario produces a worst-case notification rate roughly equal to the location update rate itself (each update potentially notifying up to 15 online friends), while a pull model only pays the cost of a lookup when a user actually opens the nearby-friends view — a much rarer event than a location ping. Since query frequency is far lower than location-update frequency, computing nearby friends on demand from a TTL-based location cache is cheaper overall; a push-based subscription model only becomes worth its fan-out cost when the product specifically needs an instant 'friend entered range' notification.

## Q zh
在一个附近好友功能中，用户大约每 15 秒上报一次位置，平均有 150 个好友、约 15 个同时在线，为什么拉模型（只在被查询时才计算附近好友）比推模型（每次位置更新都通知所有好友）更适合作为默认设计，即便这意味着好友进入范围时不会被立刻通知？

## A zh
推模型的扇出成本正比于'位置更新频率 × 每用户在线好友数'，在这个场景下得到的最坏情况通知速率大致等于位置更新速率本身（每次更新最多通知 15 个在线好友），而拉模型只在用户真正打开'附近好友'页面时才付出一次查询成本——这比位置上报频率低得多。由于查询频率远低于位置更新频率，从一个带 TTL 的位置缓存按需计算附近好友总体更便宜；只有当产品明确需要'好友进入范围立刻通知'这种即时推送时，基于订阅的推模型才值得承担它的扇出成本。
