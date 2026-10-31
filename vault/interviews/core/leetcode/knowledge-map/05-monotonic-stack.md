# 单调栈与单调队列

栈 / 队列里保持单调，每个元素进出一次：下一个更大元素、柱状图最大矩形、接雨水、滑动窗口最大值。是「找左右第一个比我大 / 小」这一类问题的通用骨架。

**先做（TikTok P1–P4 与经典题单，13 道）**

- [[tlc-best-time-to-buy-and-sell-stock-0-whole|LC 121 买卖股票的最佳时机]]（简单）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-trapping-rain-water-0-whole|LC 42 接雨水]]（困难）· TikTok P2 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-valid-parentheses-0-whole|LC 20 有效的括号]]（简单）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-remove-duplicate-letters-0-whole|LC 316 去除重复字母]]（中等）· TikTok P2 · Amazon
- [[tlc-longest-valid-parentheses-0-whole|LC 32 最长有效括号]]（困难）· TikTok P2 · Amazon · LeetCode Hot 100
- [[tlc-block-placement-queries-0-whole|LC 3161 物块放置查询]]（困难）· TikTok P2
- [[tlc-minimum-size-subarray-sum-0-whole|LC 209 长度最小的子数组]]（中等）· TikTok P2 · Top Interview 150
- [[tlc-sliding-window-maximum-0-whole|LC 239 滑动窗口最大值]]（困难）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-largest-rectangle-in-histogram-0-whole|LC 84 柱状图中最大的矩形]]（困难）· TikTok P4 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-container-with-most-water-0-whole|LC 11 盛最多水的容器]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-daily-temperatures-0-whole|LC 739 每日温度]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-car-fleet-0-whole|LC 853 车队]]（中等）· TikTok B · NeetCode 150
- [[tlc-maximum-sum-circular-subarray-0-whole|LC 918 环形子数组的最大和]]（中等）· TikTok C · Amazon · Top Interview 150

**再做（其余牌组里的题，24 道）**

- [[tlc-maximal-rectangle-0-whole|LC 85 最大矩形]]（困难）· TikTok B · Amazon
- [[tlc-verify-preorder-sequence-in-binary-search-tree-0-whole|LC 255 验证二叉搜索树的前序遍历序列]]（中等）· TikTok C
- [[tlc-create-maximum-number-0-whole|LC 321 拼接最大数]]（困难）· TikTok B
- [[tlc-remove-k-digits-0-whole|LC 402 移掉 K 位数字]]（中等）· TikTok B · Amazon
- LC 456 132 模式（中等）· Amazon
- [[tlc-next-greater-element-i-0-whole|LC 496 下一个更大元素 I]]（简单）· TikTok C · Amazon
- [[tlc-next-greater-element-ii-0-whole|LC 503 下一个更大元素 II]]（中等）· TikTok C · Amazon
- [[tlc-shortest-unsorted-continuous-subarray-0-whole|LC 581 最短无序连续子数组]]（中等）· TikTok B
- LC 643 子数组最大平均数 I（简单）· Amazon
- [[tlc-asteroid-collision-0-whole|LC 735 小行星碰撞]]（中等）· TikTok B · Amazon
- [[tlc-shortest-subarray-with-sum-at-least-k-0-whole|LC 862 和至少为 K 的最短子数组]]（困难）· TikTok B · Amazon
- LC 901 股票价格跨度（中等）· Amazon
- [[tlc-sum-of-subarray-minimums-0-whole|LC 907 子数组的最小值之和]]（中等）· TikTok C · Amazon
- [[tlc-maximum-width-ramp-0-whole|LC 962 最大宽度坡]]（中等）· TikTok C
- [[tlc-smallest-subsequence-of-distinct-characters-0-whole|LC 1081 不同字符的最小子序列]]（中等）· TikTok B · Amazon
- [[tlc-remove-all-adjacent-duplicates-in-string-ii-0-whole|LC 1209 删除字符串中的所有相邻重复项 II]]（中等）· TikTok B
- LC 1475 商品折扣后的最终价格（简单）· Amazon
- [[tlc-shortest-subarray-to-be-removed-to-make-array-sorted-0-whole|LC 1574 删除最短的子数组使剩余数组有序]]（中等）· TikTok C
- [[tlc-find-the-most-competitive-subsequence-0-whole|LC 1673 找出最具竞争力的子序列]]（中等）· TikTok B
- [[tlc-number-of-visible-people-in-a-queue-0-whole|LC 1944 队列中可以看到的人数]]（困难）· TikTok C
- LC 2281 巫师的总力量和（困难）· Amazon
- [[tlc-subarray-with-elements-greater-than-varying-threshold-0-whole|LC 2334 元素值大于变化阈值的子数组]]（困难）· TikTok B
- LC 2762 不间断子数组（中等）· Amazon
- [[tlc-find-maximum-non-decreasing-array-length-0-whole|LC 2945 找到最大非递减数组的长度]]（困难）· TikTok C
