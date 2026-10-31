# 前缀和与差分

从哈希长出来：区间和 = 两个前缀相减，「区间和等于 k」就变成「前面出现过某个前缀吗」，正是哈希查找。差分是它的逆运算，处理「很多区间批量加」。和滑动窗口的分界：数组有负数时窗口不单调，只能用前缀和加哈希。

**先做（TikTok P1–P4 与经典题单，10 道）**

- [[tlc-trapping-rain-water-0-whole|LC 42 接雨水]]（困难）· TikTok P2 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-meeting-rooms-ii-0-whole|LC 253 会议室 II]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150
- [[tlc-subarray-sum-equals-k-0-whole|LC 560 和为 K 的子数组]]（中等）· TikTok P3 · Amazon · LeetCode Hot 100
- [[tlc-minimum-size-subarray-sum-0-whole|LC 209 长度最小的子数组]]（中等）· TikTok P3 · Top Interview 150
- [[tlc-count-number-of-nice-subarrays-0-whole|LC 1248 统计「优美子数组」]]（中等）· TikTok P3 · Amazon
- [[tlc-max-consecutive-ones-iii-0-whole|LC 1004 最大连续1的个数 III]]（中等）· TikTok P4 · Amazon
- [[tlc-subarray-sums-divisible-by-k-0-whole|LC 974 和可被 K 整除的子数组]]（中等）· TikTok P4
- [[tlc-product-of-the-last-k-numbers-0-whole|LC 1352 最后 K 个数的乘积]]（中等）· TikTok P4
- [[tlc-count-of-interesting-subarrays-0-whole|LC 2845 统计趣味子数组的数目]]（中等）· TikTok P4
- [[tlc-product-of-array-except-self-0-whole|LC 238 除了自身以外数组的乘积]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150

**再做（其余牌组里的题，29 道）**

- LC 303 区域和检索 - 数组不可变（简单）· Amazon
- LC 410 分割数组的最大值（困难）· Amazon
- [[tlc-continuous-subarray-sum-0-whole|LC 523 连续的子数组和]]（中等）· TikTok B
- [[tlc-contiguous-array-0-whole|LC 525 连续数组]]（中等）· TikTok B · Amazon
- [[tlc-random-pick-with-weight-0-whole|LC 528 按权重随机选择]]（中等）· TikTok B · Amazon
- LC 724 寻找数组的中心下标（简单）· Amazon
- [[tlc-shortest-subarray-with-sum-at-least-k-0-whole|LC 862 和至少为 K 的最短子数组]]（困难）· TikTok B · Amazon
- [[tlc-number-of-submatrices-that-sum-to-target-0-whole|LC 1074 元素和为目标值的子矩阵数量]]（困难）· TikTok B
- LC 1094 拼车（中等）· Amazon
- LC 1140 石子游戏 II（中等）· Amazon
- [[tlc-minimum-swaps-to-group-all-1s-together-0-whole|LC 1151 最少交换次数来组合所有的 1]]（中等）· TikTok B
- LC 1423 可获得的最大点数（中等）· Amazon
- LC 1480 一维数组的动态和（简单）· Amazon
- [[tlc-minimum-moves-to-make-array-complementary-0-whole|LC 1674 使数组互补的最少操作次数]]（中等）· TikTok B
- LC 1703 得到连续 K 个 1 的最少相邻交换次数（困难）· Amazon
- LC 1838 最高频元素的频数（中等）· Amazon
- [[tlc-brightest-position-on-street-0-whole|LC 2021 街上最亮的位置]]（中等）· TikTok B
- LC 2024 考试的最大困扰度（中等）· Amazon
- LC 2055 蜡烛之间的盘子（中等）· Amazon
- [[tlc-count-the-hidden-sequences-0-whole|LC 2145 统计隐藏数组数目]]（中等）· TikTok B
- LC 2271 毯子覆盖的最多白色砖块数（中等）· Amazon
- LC 2281 巫师的总力量和（困难）· Amazon
- LC 2448 使数组相等的最小开销（困难）· Amazon
- [[tlc-find-the-score-of-all-prefixes-of-an-array-0-whole|LC 2640 一个数组所有前缀的分数]]（中等）· TikTok B
- [[tlc-minimum-moves-to-pick-k-ones-0-whole|LC 3086 拾起 K 个 1 需要的最少行动次数]]（困难）· TikTok B
- LC 3413 收集连续 K 个袋子可以获得的最多硬币数量（中等）· Amazon
- LC 3434 子数组操作后的最大频率（中等）· Amazon
- LC 3737 统计主要元素子数组数目 I（中等）· Amazon
- LC 3756 连接非零数字并乘以其数字和 II（中等）· Amazon
