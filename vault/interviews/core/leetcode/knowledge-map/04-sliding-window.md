# 滑动窗口

同向双指针加一个可增量维护的窗口状态（哈希计数、和、单调队列）。前提是单调：窗口变大条件只会变坏或变好。不单调时退回前缀和；要窗口最大值时配单调队列。

**先做（TikTok P1–P4 与经典题单，16 道）**

- [[tlc-longest-substring-without-repeating-characters-0-whole|LC 3 无重复字符的最长子串]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-subarray-sum-equals-k-0-whole|LC 560 和为 K 的子数组]]（中等）· TikTok P3 · Amazon · LeetCode Hot 100
- [[tlc-sliding-window-maximum-0-whole|LC 239 滑动窗口最大值]]（困难）· TikTok P3 · Amazon · NeetCode 150 · LeetCode Hot 100
- [[tlc-longest-substring-with-at-most-k-distinct-characters-0-whole|LC 340 至多包含 K 个不同字符的最长子串]]（中等）· TikTok P3
- [[tlc-minimum-size-subarray-sum-0-whole|LC 209 长度最小的子数组]]（中等）· TikTok P3 · Top Interview 150
- [[tlc-minimum-window-substring-0-whole|LC 76 最小覆盖子串]]（困难）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-count-number-of-nice-subarrays-0-whole|LC 1248 统计「优美子数组」]]（中等）· TikTok P3 · Amazon
- [[tlc-fruit-into-baskets-0-whole|LC 904 水果成篮]]（中等）· TikTok P3 · Amazon
- [[tlc-longest-mountain-in-array-0-whole|LC 845 数组中的最长山脉]]（中等）· TikTok P4
- [[tlc-max-consecutive-ones-iii-0-whole|LC 1004 最大连续1的个数 III]]（中等）· TikTok P4 · Amazon
- [[tlc-longest-repeating-character-replacement-0-whole|LC 424 替换后的最长重复字符]]（中等）· TikTok P4 · Blind 75 · NeetCode 150
- [[tlc-find-all-anagrams-in-a-string-0-whole|LC 438 找到字符串中所有字母异位词]]（中等）· TikTok P4 · Amazon · LeetCode Hot 100
- [[tlc-kth-smallest-subarray-sum-0-whole|LC 1918 第 K 小的子数组和]]（中等）· TikTok P4
- [[tlc-substring-with-concatenation-of-all-words-0-whole|LC 30 串联所有单词的子串]]（困难）· TikTok B · Amazon · Top Interview 150
- LC 219 存在重复元素 II（简单）· Amazon · Top Interview 150
- [[tlc-permutation-in-string-0-whole|LC 567 字符串的排列]]（中等）· TikTok B · Amazon · NeetCode 150

**再做（其余牌组里的题，25 道）**

- [[tlc-repeated-dna-sequences-0-whole|LC 187 重复的DNA序列]]（中等）· TikTok B
- [[tlc-longest-substring-with-at-least-k-repeating-characters-0-whole|LC 395 至少有 K 个重复字符的最长子串]]（中等）· TikTok B · Amazon
- [[tlc-sliding-window-median-0-whole|LC 480 滑动窗口中位数]]（困难）· TikTok B · Amazon
- LC 643 子数组最大平均数 I（简单）· Amazon
- LC 658 找到 K 个最接近的元素（中等）· Amazon
- [[tlc-maximum-length-of-repeated-subarray-0-whole|LC 718 最长重复子数组]]（中等）· TikTok B
- [[tlc-shortest-subarray-with-sum-at-least-k-0-whole|LC 862 和至少为 K 的最短子数组]]（困难）· TikTok B · Amazon
- LC 992 K 个不同整数的子数组（困难）· Amazon
- [[tlc-longest-duplicate-substring-0-whole|LC 1044 最长重复子串]]（困难）· TikTok B
- [[tlc-minimum-swaps-to-group-all-1s-together-0-whole|LC 1151 最少交换次数来组合所有的 1]]（中等）· TikTok B
- LC 1423 可获得的最大点数（中等）· Amazon
- [[tlc-find-two-non-overlapping-sub-arrays-each-with-target-sum-0-whole|LC 1477 找两个和为目标值且不重叠的子数组]]（中等）· TikTok B
- [[tlc-longest-subarray-of-1s-after-deleting-one-element-0-whole|LC 1493 删掉一个元素以后全为 1 的最长子数组]]（中等）· TikTok B
- LC 1703 得到连续 K 个 1 的最少相邻交换次数（困难）· Amazon
- LC 1838 最高频元素的频数（中等）· Amazon
- LC 2024 考试的最大困扰度（中等）· Amazon
- [[tlc-minimum-swaps-to-group-all-1s-together-ii-0-whole|LC 2134 最少交换次数来组合所有的 1 II]]（中等）· TikTok B
- LC 2271 毯子覆盖的最多白色砖块数（中等）· Amazon
- LC 2461 长度为 K 子数组中的最大和（中等）· Amazon
- LC 2762 不间断子数组（中等）· Amazon
- [[tlc-count-complete-subarrays-in-an-array-0-whole|LC 2799 统计完全子数组的数目]]（中等）· TikTok B
- LC 2958 最多 K 个重复元素的最长子数组（中等）· Amazon
- [[tlc-minimum-moves-to-pick-k-ones-0-whole|LC 3086 拾起 K 个 1 需要的最少行动次数]]（困难）· TikTok B
- LC 3090 每个字符最多出现两次的最长子字符串（简单）· Amazon
- LC 3413 收集连续 K 个袋子可以获得的最多硬币数量（中等）· Amazon
