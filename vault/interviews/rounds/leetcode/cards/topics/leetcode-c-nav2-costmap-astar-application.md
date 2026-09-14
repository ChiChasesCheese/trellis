---
id: leetcode-c-nav2-costmap-astar-application
node: topics.uncategorised
type: qa
anki: 1787361364993
tags: [algorithm::a-search, algorithm::grid-graph, algorithm::priority-queue, application, case, case::nav2-costmap-astar, category::runtimes-os, chapter::04, chapter::06, leetcode, system::ros-2-nav2]
---
## Q
ROS 2 Nav2 为什么把 costmap 当隐式图，而不是预建 adjacency list？A* 的 heap 存什么？

## A
每个 cell/pose 的邻居可按运动模型即时生成，预建边浪费内存且地图会变化。heap 存 frontier，按 g+h 取最有希望的状态；碰撞检查和 costmap 决定边是否可走及其代价。

**Evidence**

Nav2 官方文档描述 Costmap2D 与 Smac A*/Hybrid-A* planners 的搜索空间、代价和碰撞检查。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FROS%202%20Nav2%EF%BC%9A%E4%BB%A3%E4%BB%B7%E5%9C%B0%E5%9B%BE%E4%B8%8A%E7%9A%84%20A-star%20%E6%90%9C%E7%B4%A2)
