# 堆：Top-K、多路归并与调度

只需要反复取最值时用堆：Top-K、K 路归并、双堆求中位数、按时间调度任务。Dijkstra 的本质就是「堆 + 贪心」；很多设计题（定时器、任务调度）的核心也是堆。

**先做（TikTok P1–P4 与经典题单，22 道）**

- [[tlc-kth-largest-element-in-an-array-0-whole|LC 215 数组中的第K个最大元素]]（中等）· TikTok P1 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-top-k-frequent-elements-0-whole|LC 347 前 K 个高频元素]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100
- [[tlc-best-time-to-buy-and-sell-stock-0-whole|LC 121 买卖股票的最佳时机]]（简单）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-merge-k-sorted-lists-0-whole|LC 23 合并 K 个升序链表]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-meeting-rooms-ii-0-whole|LC 253 会议室 II]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150
- [[tlc-find-median-from-data-stream-0-whole|LC 295 数据流的中位数]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-cheapest-flights-within-k-stops-0-whole|LC 787 K 站中转内最便宜的航班]]（中等）· TikTok P2 · NeetCode 150
- [[tlc-single-threaded-cpu-0-whole|LC 1834 单线程 CPU]]（中等）· TikTok P2 · Amazon
- [[tlc-sliding-window-maximum-0-whole|LC 239 滑动窗口最大值]]（困难）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-kth-smallest-element-in-a-sorted-matrix-0-whole|LC 378 有序矩阵中第 K 小的元素]]（中等）· TikTok P4
- [[tlc-time-based-key-value-store-0-whole|LC 981 基于时间的键值存储]]（中等）· TikTok P4 · NeetCode 150
- [[tlc-swim-in-rising-water-0-whole|LC 778 水位上升的泳池中游泳]]（困难）· TikTok P4 · NeetCode 150
- LC 332 重新安排行程（困难）· Amazon · NeetCode 150
- LC 355 设计推特（中等）· NeetCode 150
- LC 373 查找和最小的 K 对数字（中等）· Amazon · Top Interview 150
- LC 502 IPO（困难）· Top Interview 150
- LC 621 任务调度器（中等）· TikTok C · Amazon · NeetCode 150
- LC 703 数据流中的第 K 大元素（简单）· NeetCode 150
- LC 743 网络延迟时间（中等）· NeetCode 150
- LC 973 最接近原点的 K 个点（中等）· NeetCode 150
- LC 1046 最后一块石头的重量（简单）· NeetCode 150
- LC 1851 包含每个查询的最小区间（困难）· NeetCode 150

**再做（其余牌组里的题，34 道）**

- LC 358 K 距离间隔重排字符串（困难）· TikTok C
- [[tlc-trapping-rain-water-ii-0-whole|LC 407 接雨水 II]]（困难）· TikTok B
- [[tlc-sliding-window-median-0-whole|LC 480 滑动窗口中位数]]（困难）· TikTok B · Amazon
- [[tlc-the-maze-iii-0-whole|LC 499 迷宫 III]]（困难）· TikTok B
- LC 505 迷宫 II（中等）· TikTok C
- [[tlc-array-partition-i-0-whole|LC 561 数组拆分]]（简单）· TikTok B · Amazon
- LC 642 设计搜索自动补全系统（困难）· TikTok C
- LC 658 找到 K 个最接近的元素（中等）· TikTok C · Amazon
- [[tlc-top-k-frequent-words-0-whole|LC 692 前K个高频单词]]（中等）· TikTok B · Amazon
- LC 759 员工空闲时间（困难）· TikTok C · Amazon
- [[tlc-reorganize-string-0-whole|LC 767 重构字符串]]（中等）· TikTok B · Amazon
- [[tlc-shortest-subarray-with-sum-at-least-k-0-whole|LC 862 和至少为 K 的最短子数组]]（困难）· TikTok B · Amazon
- LC 871 最低加油次数（困难）· Amazon
- [[tlc-sort-an-array-0-whole|LC 912 排序数组]]（中等）· TikTok B
- LC 1094 拼车（中等）· Amazon
- LC 1167 连接木棍的最低费用（中等）· Amazon
- LC 1268 搜索推荐系统（中等）· TikTok C · Amazon
- LC 1353 最多可以参加的会议数目（中等）· TikTok C
- LC 1383 最大的团队表现值（困难）· TikTok C
- [[tlc-longest-happy-string-0-whole|LC 1405 最长快乐字符串]]（中等）· TikTok B
- LC 1642 可以到达的最远建筑（中等）· TikTok C
- LC 2357 使数组中所有元素都等于零（简单）· Amazon
- [[tlc-meeting-rooms-iii-0-whole|LC 2402 会议室 III]]（困难）· TikTok B
- [[tlc-most-popular-video-creator-0-whole|LC 2456 最流行的视频创作者]]（中等）· TikTok B
- LC 2530 执行 K 次操作后的最大分数（中等）· TikTok C
- LC 2542 最大子序列的分数（中等）· Amazon
- LC 2551 将珠子放入背包中（困难）· TikTok C
- LC 2762 不间断子数组（中等）· Amazon
- LC 2812 找出最安全路径（中等）· Amazon
- LC 2931 购买物品的最大开销（困难）· TikTok C
- LC 3286 穿越网格图的安全路径（中等）· Amazon
- LC 3408 设计任务管理器（中等）· TikTok C
- LC 3607 电网维护（中等）· Amazon
- LC 3620 恢复网络路径（困难）· Amazon
