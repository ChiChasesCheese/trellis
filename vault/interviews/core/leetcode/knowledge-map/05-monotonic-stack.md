# 单调栈与单调队列

栈 / 队列里保持单调，每个元素进出一次：下一个更大元素、柱状图最大矩形、接雨水、滑动窗口最大值。是「找左右第一个比我大 / 小」这一类问题的通用骨架。

**先做（TikTok P1–P4 与经典题单，13 道）**

- [[lct-best-time-to-buy-and-sell-stock|LC 121 买卖股票的最佳时机]]（简单）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-trapping-rain-water|LC 42 接雨水]]（困难）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-valid-parentheses|LC 20 有效的括号]]（简单）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-remove-duplicate-letters|LC 316 去除重复字母]]（中等）· TikTok P2 · Amazon
- [[lct-longest-valid-parentheses|LC 32 最长有效括号]]（困难）· TikTok P2 · Amazon · LeetCode Hot 100
- [[lct-block-placement-queries|LC 3161 物块放置查询]]（困难）· TikTok P2
- [[lct-minimum-size-subarray-sum|LC 209 长度最小的子数组]]（中等）· TikTok P2 · Top Interview 150
- [[lct-sliding-window-maximum|LC 239 滑动窗口最大值]]（困难）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-largest-rectangle-in-histogram|LC 84 柱状图中最大的矩形]]（困难）· TikTok P4 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-container-with-most-water|LC 11 盛最多水的容器]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-daily-temperatures|LC 739 每日温度]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100
- [[lct-car-fleet|LC 853 车队]]（中等）· TikTok B · NeetCode 150
- [[lct-maximum-sum-circular-subarray|LC 918 环形子数组的最大和]]（中等）· TikTok C · Amazon · Top Interview 150

**再做（其余牌组里的题，24 道）**

- [[lct-maximal-rectangle|LC 85 最大矩形]]（困难）· TikTok B · Amazon
- [[lct-verify-preorder-sequence-in-binary-search-tree|LC 255 验证二叉搜索树的前序遍历序列]]（中等）· TikTok C
- [[lct-create-maximum-number|LC 321 拼接最大数]]（困难）· TikTok B
- [[lct-remove-k-digits|LC 402 移掉 K 位数字]]（中等）· TikTok B · Amazon
- LC 456 132 模式（中等）· Amazon
- [[lct-next-greater-element-i|LC 496 下一个更大元素 I]]（简单）· TikTok C · Amazon
- [[lct-next-greater-element-ii|LC 503 下一个更大元素 II]]（中等）· TikTok C · Amazon
- [[lct-shortest-unsorted-continuous-subarray|LC 581 最短无序连续子数组]]（中等）· TikTok B
- LC 643 子数组最大平均数 I（简单）· Amazon
- [[lct-asteroid-collision|LC 735 小行星碰撞]]（中等）· TikTok B · Amazon
- [[lct-shortest-subarray-with-sum-at-least-k|LC 862 和至少为 K 的最短子数组]]（困难）· TikTok B · Amazon
- LC 901 股票价格跨度（中等）· Amazon
- [[lct-sum-of-subarray-minimums|LC 907 子数组的最小值之和]]（中等）· TikTok C · Amazon
- [[lct-maximum-width-ramp|LC 962 最大宽度坡]]（中等）· TikTok C
- [[lct-smallest-subsequence-of-distinct-characters|LC 1081 不同字符的最小子序列]]（中等）· TikTok B · Amazon
- [[lct-remove-all-adjacent-duplicates-in-string-ii|LC 1209 删除字符串中的所有相邻重复项 II]]（中等）· TikTok B
- LC 1475 商品折扣后的最终价格（简单）· Amazon
- [[lct-shortest-subarray-to-be-removed-to-make-array-sorted|LC 1574 删除最短的子数组使剩余数组有序]]（中等）· TikTok C
- [[lct-find-the-most-competitive-subsequence|LC 1673 找出最具竞争力的子序列]]（中等）· TikTok B
- [[lct-number-of-visible-people-in-a-queue|LC 1944 队列中可以看到的人数]]（困难）· TikTok C
- LC 2281 巫师的总力量和（困难）· Amazon
- [[lct-subarray-with-elements-greater-than-varying-threshold|LC 2334 元素值大于变化阈值的子数组]]（困难）· TikTok B
- LC 2762 不间断子数组（中等）· Amazon
- [[lct-find-maximum-non-decreasing-array-length|LC 2945 找到最大非递减数组的长度]]（困难）· TikTok C
