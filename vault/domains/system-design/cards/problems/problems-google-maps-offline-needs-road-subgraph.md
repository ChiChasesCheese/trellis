---
id: problems-google-maps-offline-needs-road-subgraph
node: problems.geo.google-maps
type: qa
step: 7
tags: [grown]
---
## Q
In a Google Maps-style design, why does an offline map download need to include more than just the map tiles for the selected region in order to support turn-by-turn navigation while offline?

## A
Tiles only let the client display the map visually; computing a route requires access to the road graph itself, so the offline package must also include a self-contained subgraph of the road network for that region, extracted with a buffer extending past the selected boundary so routes that briefly leave and re-enter the region (for example, to go around an overpass) still resolve correctly. Because this offline subgraph can't reach the online live-traffic service, offline routing can only use static speed limits and historical average speeds, and offline rerouting can't benefit from live-traffic-informed replanning the way online navigation can.

## Q zh
在一个类 Google Maps 的设计中，为什么离线地图下载想要支持离线状态下的逐向导航（turn-by-turn navigation），就必须包含的不只是所选区域的地图瓦片？

## A zh
瓦片只能让客户端把地图画出来，计算路线需要访问路网图本身，所以离线包还必须包含这个区域一份自成一体的路网子图——提取时要在所选边界之外再多留一圈缓冲区，这样即便路线短暂离开又重新进入这个区域（比如绕过一座立交桥），依然能正确解算。因为这份离线子图无法连接在线的实时路况服务，离线路径规划只能使用静态限速和历史平均车速，离线状态下的重新规划也无法像在线导航那样受益于基于实时路况的重新规划。
