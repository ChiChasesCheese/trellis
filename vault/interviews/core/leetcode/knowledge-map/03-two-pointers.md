# 双指针

利用有序或单调，把两层循环压成一次扫描：相向夹逼、快慢指针、原地分区。滑动窗口是同向双指针的特例；链表的找中点、判环也是快慢指针；归并排序的合并就是两个指针。

**先做（TikTok P1–P4 与经典题单，45 道）**

- [[lct-longest-substring-without-repeating-characters|LC 3 无重复字符的最长子串]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-longest-palindromic-substring|LC 5 最长回文子串]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-remove-nth-node-from-end-of-list|LC 19 删除链表的倒数第 N 个结点]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-trapping-rain-water|LC 42 接雨水]]（困难）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-merge-sorted-array|LC 88 合并两个有序数组]]（简单）· TikTok P2 · Amazon · Top Interview 150
- [[lct-meeting-rooms-ii|LC 253 会议室 II]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150
- [[lct-3sum|LC 15 三数之和]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-two-sum|LC 1 两数之和]]（简单）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-longest-increasing-subsequence|LC 300 最长递增子序列]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-find-median-from-data-stream|LC 295 数据流的中位数]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-add-strings|LC 415 字符串相加]]（简单）· TikTok P2
- [[lct-rotate-array|LC 189 轮转数组]]（中等）· TikTok P2 · Amazon · LeetCode Hot 100 · Top Interview 150
- [[lct-intersection-of-two-linked-lists|LC 160 相交链表]]（简单）· TikTok P2 · LeetCode Hot 100
- [[lct-longest-mountain-in-array|LC 845 数组中的最长山脉]]（中等）· TikTok P2
- [[lct-reverse-words-in-a-string|LC 151 反转字符串中的单词]]（中等）· TikTok P3 · Top Interview 150
- [[lct-linked-list-cycle|LC 141 环形链表]]（简单）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-candy|LC 135 分发糖果]]（困难）· TikTok P4 · Amazon · Top Interview 150
- [[lct-interval-list-intersections|LC 986 区间列表的交集]]（中等）· TikTok P4
- [[lct-successful-pairs-of-spells-and-potions|LC 2300 咒语和药水的成功对数]]（中等）· TikTok P4
- [[lct-longest-string-chain|LC 1048 最长字符串链]]（中等）· TikTok P4
- [[lct-container-with-most-water|LC 11 盛最多水的容器]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- LC 26 删除有序数组中的重复项（简单）· Amazon · Top Interview 150
- LC 27 移除元素（简单）· Amazon · Top Interview 150
- LC 28 找出字符串中第一个匹配项的下标（简单）· Amazon · Top Interview 150
- [[lct-next-permutation|LC 31 下一个排列]]（中等）· TikTok B · LeetCode Hot 100
- [[lct-rotate-list|LC 61 旋转链表]]（中等）· TikTok B · Amazon · Top Interview 150
- [[lct-sort-colors|LC 75 颜色分类]]（中等）· TikTok B · Amazon · LeetCode Hot 100
- [[lct-remove-duplicates-from-sorted-array-ii|LC 80 删除有序数组中的重复项 II]]（中等）· TikTok B · Top Interview 150
- [[lct-remove-duplicates-from-sorted-list-ii|LC 82 删除排序链表中的重复元素 II]]（中等）· TikTok B · Top Interview 150
- [[lct-partition-list|LC 86 分隔链表]]（中等）· TikTok B · Top Interview 150
- [[lct-valid-palindrome|LC 125 验证回文串]]（简单）· TikTok B · Amazon · Blind 75 · NeetCode 150 · Top Interview 150
- [[lct-linked-list-cycle-ii|LC 142 环形链表 II]]（中等）· TikTok B · Amazon · LeetCode Hot 100
- [[lct-reorder-list|LC 143 重排链表]]（中等）· TikTok B · Blind 75 · NeetCode 150
- [[lct-sort-list|LC 148 排序链表]]（中等）· TikTok B · Amazon · LeetCode Hot 100 · Top Interview 150
- LC 149 直线上最多的点数（困难）· Top Interview 150
- [[lct-two-sum-ii-input-array-is-sorted|LC 167 两数之和 II - 输入有序数组]]（中等）· TikTok C · Amazon · NeetCode 150 · Top Interview 150
- [[lct-happy-number|LC 202 快乐数]]（简单）· TikTok C · Amazon · NeetCode 150 · Top Interview 150
- [[lct-palindrome-linked-list|LC 234 回文链表]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- [[lct-product-of-array-except-self|LC 238 除了自身以外数组的乘积]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-move-zeroes|LC 283 移动零]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- [[lct-find-the-duplicate-number|LC 287 寻找重复数]]（中等）· TikTok B · NeetCode 150 · LeetCode Hot 100
- LC 392 判断子序列（简单）· Amazon · Top Interview 150
- [[lct-permutation-in-string|LC 567 字符串的排列]]（中等）· TikTok B · Amazon · NeetCode 150
- [[lct-palindromic-substrings|LC 647 回文子串]]（中等）· TikTok B · Blind 75 · NeetCode 150
- LC 763 划分字母区间（中等）· NeetCode 150 · LeetCode Hot 100

**再做（其余牌组里的题，34 道）**

- [[lct-3sum-closest|LC 16 最接近的三数之和]]（中等）· TikTok B · Amazon
- [[lct-4sum|LC 18 四数之和]]（中等）· TikTok B · Amazon
- [[lct-compare-version-numbers|LC 165 比较版本号]]（中等）· TikTok B
- [[lct-3sum-smaller|LC 259 较小的三数之和]]（中等）· TikTok C
- [[lct-find-the-celebrity|LC 277 搜寻名人]]（中等）· TikTok C · Amazon
- [[lct-create-maximum-number|LC 321 拼接最大数]]（困难）· TikTok B
- LC 344 反转字符串（简单）· Amazon
- LC 349 两个数组的交集（简单）· Amazon
- [[lct-valid-word-abbreviation|LC 408 有效单词缩写]]（简单）· TikTok C
- [[lct-string-compression|LC 443 压缩字符串]]（中等）· TikTok C · Amazon
- [[lct-assign-cookies|LC 455 分发饼干]]（简单）· TikTok B
- [[lct-heaters|LC 475 供暖器]]（中等）· TikTok C
- LC 557 反转字符串中的单词 III（简单）· Amazon
- [[lct-shortest-unsorted-continuous-subarray|LC 581 最短无序连续子数组]]（中等）· TikTok B
- [[lct-find-k-closest-elements|LC 658 找到 K 个最接近的元素]]（中等）· TikTok C · Amazon
- [[lct-valid-palindrome-ii|LC 680 验证回文串 II]]（简单）· TikTok B · Amazon
- [[lct-count-binary-substrings|LC 696 计数二进制子串]]（简单）· TikTok C
- [[lct-find-k-th-smallest-pair-distance|LC 719 找出第 K 小的数对距离]]（困难）· TikTok B
- [[lct-candy-crush|LC 723 粉碎糖果]]（中等）· TikTok C
- LC 876 链表的中间结点（简单）· 
- [[lct-boats-to-save-people|LC 881 救生艇]]（中等）· TikTok B · Amazon
- [[lct-sort-array-by-parity|LC 905 按奇偶排序数组]]（简单）· TikTok B
- [[lct-maximum-width-ramp|LC 962 最大宽度坡]]（中等）· TikTok C
- [[lct-squares-of-a-sorted-array|LC 977 有序数组的平方]]（简单）· TikTok B · Amazon
- [[lct-two-sum-less-than-k|LC 1099 小于 K 的两数之和]]（简单）· TikTok B
- [[lct-find-positive-integer-solution-for-a-given-equation|LC 1237 找出给定方程的正整数解]]（中等）· TikTok C
- [[lct-dot-product-of-two-sparse-vectors|LC 1570 两个稀疏向量的点积]]（中等）· TikTok C
- [[lct-shortest-subarray-to-be-removed-to-make-array-sorted|LC 1574 删除最短的子数组使剩余数组有序]]（中等）· TikTok C
- [[lct-lowest-common-ancestor-of-a-binary-tree-iii|LC 1650 二叉树的最近公共祖先 III]]（中等）· TikTok C · Amazon
- LC 1768 交替合并字符串（简单）· Amazon
- [[lct-sentence-similarity-iii|LC 1813 句子相似性 III]]（中等）· TikTok C
- LC 2149 按符号重排数组（中等）· Amazon
- [[lct-merge-operations-to-turn-array-into-a-palindrome|LC 2422 使用合并操作将数组转换为回文序列]]（中等）· TikTok C
- LC 2938 区分黑球与白球（中等）· Amazon
