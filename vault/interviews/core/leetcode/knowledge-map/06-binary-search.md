# 二分查找

从有序数组上的查找，推广到「答案单调」的判定：最小化最大值、能否在 x 内完成。旋转数组、找边界都是在维护一个不变量。和堆、平衡树一起，是「有序 + log n」的三件套。

**先做（TikTok P1–P4 与经典题单，29 道）**

- [[lct-numbers-at-most-n-given-digit-set|LC 902 最大为 N 的数字组合]]（困难）· TikTok P1
- [[lct-search-in-rotated-sorted-array|LC 33 搜索旋转排序数组]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-longest-increasing-subsequence|LC 300 最长递增子序列]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-block-placement-queries|LC 3161 物块放置查询]]（困难）· TikTok P2
- [[lct-minimum-size-subarray-sum|LC 209 长度最小的子数组]]（中等）· TikTok P2 · Top Interview 150
- [[lct-find-first-and-last-position-of-element-in-sorted-array|LC 34 在排序数组中查找元素的第一个和最后一个位置]]（中等）· TikTok P2 · Amazon · LeetCode Hot 100 · Top Interview 150
- [[lct-single-element-in-a-sorted-array|LC 540 有序数组中的单一元素]]（中等）· TikTok P2 · Amazon
- [[lct-median-of-two-sorted-arrays|LC 4 寻找两个正序数组的中位数]]（困难）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-sqrtx|LC 69 x 的平方根 ]]（简单）· TikTok P3 · Amazon · Top Interview 150
- [[lct-word-break|LC 139 单词拆分]]（中等）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-koko-eating-bananas|LC 875 爱吃香蕉的珂珂]]（中等）· TikTok P4 · Amazon · NeetCode 150
- [[lct-max-consecutive-ones-iii|LC 1004 最大连续1的个数 III]]（中等）· TikTok P4 · Amazon
- [[lct-find-minimum-in-rotated-sorted-array|LC 153 寻找旋转排序数组中的最小值]]（中等）· TikTok P4 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-kth-smallest-element-in-a-sorted-matrix|LC 378 有序矩阵中第 K 小的元素]]（中等）· TikTok P4
- [[lct-time-based-key-value-store|LC 981 基于时间的键值存储]]（中等）· TikTok P4 · NeetCode 150
- [[lct-search-insert-position|LC 35 搜索插入位置]]（简单）· TikTok P4 · Amazon · LeetCode Hot 100 · Top Interview 150
- [[lct-find-minimum-in-rotated-sorted-array-ii|LC 154 寻找旋转排序数组中的最小值 II]]（困难）· TikTok P4
- [[lct-swim-in-rising-water|LC 778 水位上升的泳池中游泳]]（困难）· TikTok P4 · NeetCode 150
- [[lct-kth-smallest-subarray-sum|LC 1918 第 K 小的子数组和]]（中等）· TikTok P4
- [[lct-successful-pairs-of-spells-and-potions|LC 2300 咒语和药水的成功对数]]（中等）· TikTok P4
- [[lct-search-a-2d-matrix|LC 74 搜索二维矩阵]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-find-peak-element|LC 162 寻找峰值]]（中等）· TikTok B · Top Interview 150
- [[lct-two-sum-ii-input-array-is-sorted|LC 167 两数之和 II - 输入有序数组]]（中等）· TikTok C · Amazon · NeetCode 150 · Top Interview 150
- LC 222 完全二叉树的节点个数（中等）· Top Interview 150
- [[lct-search-a-2d-matrix-ii|LC 240 搜索二维矩阵 II]]（中等）· TikTok B · Amazon · LeetCode Hot 100
- LC 268 丢失的数字（简单）· Amazon · Blind 75 · NeetCode 150
- [[lct-find-the-duplicate-number|LC 287 寻找重复数]]（中等）· TikTok B · NeetCode 150 · LeetCode Hot 100
- [[lct-binary-search|LC 704 二分查找]]（简单）· TikTok B · NeetCode 150
- LC 1851 包含每个查询的最小区间（困难）· NeetCode 150

**再做（其余牌组里的题，45 道）**

- [[lct-search-in-rotated-sorted-array-ii|LC 81 搜索旋转排序数组 II]]（中等）· TikTok B
- [[lct-3sum-smaller|LC 259 较小的三数之和]]（中等）· TikTok C
- LC 278 第一个错误的版本（简单）· 
- LC 349 两个数组的交集（简单）· Amazon
- [[lct-russian-doll-envelopes|LC 354 俄罗斯套娃信封问题]]（困难）· TikTok C
- [[lct-nth-digit|LC 400 第 N 位数字]]（中等）· TikTok C
- LC 410 分割数组的最大值（困难）· Amazon
- LC 456 132 模式（中等）· Amazon
- [[lct-heaters|LC 475 供暖器]]（中等）· TikTok C
- LC 493 翻转对（困难）· Amazon
- [[lct-random-pick-with-weight|LC 528 按权重随机选择]]（中等）· TikTok B · Amazon
- [[lct-find-k-closest-elements|LC 658 找到 K 个最接近的元素]]（中等）· TikTok C · Amazon
- [[lct-maximum-length-of-repeated-subarray|LC 718 最长重复子数组]]（中等）· TikTok B
- [[lct-find-k-th-smallest-pair-distance|LC 719 找出第 K 小的数对距离]]（困难）· TikTok B
- [[lct-my-calendar-i|LC 729 我的日程安排表 I]]（中等）· TikTok C
- [[lct-preimage-size-of-factorial-zeroes-function|LC 793 阶乘函数后 K 个零]]（困难）· TikTok B
- LC 852 山脉数组的峰顶索引（中等）· Amazon
- [[lct-shortest-subarray-with-sum-at-least-k|LC 862 和至少为 K 的最短子数组]]（困难）· TikTok B · Amazon
- [[lct-super-egg-drop|LC 887 鸡蛋掉落]]（困难）· TikTok B
- [[lct-fair-candy-swap|LC 888 公平的糖果交换]]（简单）· TikTok B
- [[lct-capacity-to-ship-packages-within-d-days|LC 1011 在 D 天内送达包裹的能力]]（中等）· TikTok B · Amazon
- [[lct-longest-duplicate-substring|LC 1044 最长重复子串]]（困难）· TikTok B
- [[lct-longest-repeating-substring|LC 1062 最长重复子串的长度]]（中等）· TikTok B
- [[lct-two-sum-less-than-k|LC 1099 小于 K 的两数之和]]（简单）· TikTok B
- [[lct-snapshot-array|LC 1146 快照数组]]（中等）· TikTok B
- [[lct-maximum-profit-in-job-scheduling|LC 1235 规划兼职工作]]（困难）· TikTok B · Amazon
- [[lct-find-positive-integer-solution-for-a-given-equation|LC 1237 找出给定方程的正整数解]]（中等）· TikTok C
- [[lct-search-suggestions-system|LC 1268 搜索推荐系统]]（中等）· TikTok C · Amazon
- [[lct-find-two-non-overlapping-sub-arrays-each-with-target-sum|LC 1477 找两个和为目标值且不重叠的子数组]]（中等）· TikTok B
- LC 1482 制作 m 束花所需的最少天数（中等）· Amazon
- [[lct-kth-missing-positive-number|LC 1539 第 k 个缺失的正整数]]（简单）· TikTok B
- LC 1552 两球之间的磁力（中等）· Amazon
- [[lct-shortest-subarray-to-be-removed-to-make-array-sorted|LC 1574 删除最短的子数组使剩余数组有序]]（中等）· TikTok C
- [[lct-maximum-value-at-a-given-index-in-a-bounded-array|LC 1802 有界数组中指定下标处的最大值]]（中等）· TikTok B
- LC 1838 最高频元素的频数（中等）· Amazon
- LC 2024 考试的最大困扰度（中等）· Amazon
- LC 2055 蜡烛之间的盘子（中等）· Amazon
- LC 2271 毯子覆盖的最多白色砖块数（中等）· Amazon
- LC 2448 使数组相等的最小开销（困难）· Amazon
- LC 2812 找出最安全路径（中等）· Amazon
- [[lct-minimum-absolute-difference-between-elements-with-constraint|LC 2817 限制条件下元素之间的最小绝对差]]（中等）· TikTok C
- [[lct-find-maximum-non-decreasing-array-length|LC 2945 找到最大非递减数组的长度]]（困难）· TikTok C
- LC 3413 收集连续 K 个袋子可以获得的最多硬币数量（中等）· Amazon
- LC 3620 恢复网络路径（困难）· Amazon
- LC 3733 完成所有送货任务的最少时间（中等）· Amazon
