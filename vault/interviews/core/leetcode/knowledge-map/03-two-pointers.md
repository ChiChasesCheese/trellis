# 双指针

利用有序或单调，把两层循环压成一次扫描：相向夹逼、快慢指针、原地分区。滑动窗口是同向双指针的特例；链表的找中点、判环也是快慢指针；归并排序的合并就是两个指针。

**先做（TikTok P1–P4 与经典题单，43 道）**

- [[tlc-longest-substring-without-repeating-characters-0-whole|LC 3 无重复字符的最长子串]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-longest-palindromic-substring-0-whole|LC 5 最长回文子串]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-remove-nth-node-from-end-of-list-0-whole|LC 19 删除链表的倒数第 N 个结点]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-trapping-rain-water-0-whole|LC 42 接雨水]]（困难）· TikTok P2 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-meeting-rooms-ii-0-whole|LC 253 会议室 II]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150
- [[tlc-3sum-0-whole|LC 15 三数之和]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-longest-increasing-subsequence-0-whole|LC 300 最长递增子序列]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-merge-sorted-array-0-whole|LC 88 合并两个有序数组]]（简单）· TikTok P2 · Amazon · Top Interview 150
- [[tlc-two-sum-0-whole|LC 1 两数之和]]（简单）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-add-strings-0-whole|LC 415 字符串相加]]（简单）· TikTok P2
- [[tlc-find-median-from-data-stream-0-whole|LC 295 数据流的中位数]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-intersection-of-two-linked-lists-0-whole|LC 160 相交链表]]（简单）· TikTok P3 · LeetCode Hot 100
- [[tlc-reverse-words-in-a-string-0-whole|LC 151 反转字符串中的单词]]（中等）· TikTok P3 · Top Interview 150
- [[tlc-rotate-array-0-whole|LC 189 轮转数组]]（中等）· TikTok P3 · Amazon · LeetCode Hot 100 · Top Interview 150
- [[tlc-linked-list-cycle-0-whole|LC 141 环形链表]]（简单）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-longest-mountain-in-array-0-whole|LC 845 数组中的最长山脉]]（中等）· TikTok P4
- [[tlc-interval-list-intersections-0-whole|LC 986 区间列表的交集]]（中等）· TikTok P4
- [[tlc-successful-pairs-of-spells-and-potions-0-whole|LC 2300 咒语和药水的成功对数]]（中等）· TikTok P4
- [[tlc-longest-string-chain-0-whole|LC 1048 最长字符串链]]（中等）· TikTok P4
- [[tlc-container-with-most-water-0-whole|LC 11 盛最多水的容器]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- LC 26 删除有序数组中的重复项（简单）· Amazon · Top Interview 150
- LC 27 移除元素（简单）· Amazon · Top Interview 150
- LC 28 找出字符串中第一个匹配项的下标（简单）· Amazon · Top Interview 150
- [[tlc-next-permutation-0-whole|LC 31 下一个排列]]（中等）· TikTok B · LeetCode Hot 100
- [[tlc-rotate-list-0-whole|LC 61 旋转链表]]（中等）· TikTok B · Amazon · Top Interview 150
- [[tlc-sort-colors-0-whole|LC 75 颜色分类]]（中等）· TikTok B · Amazon · LeetCode Hot 100
- [[tlc-remove-duplicates-from-sorted-array-ii-0-whole|LC 80 删除有序数组中的重复项 II]]（中等）· TikTok B · Top Interview 150
- [[tlc-remove-duplicates-from-sorted-list-ii-0-whole|LC 82 删除排序链表中的重复元素 II]]（中等）· TikTok B · Top Interview 150
- [[tlc-partition-list-0-whole|LC 86 分隔链表]]（中等）· TikTok B · Top Interview 150
- [[tlc-valid-palindrome-0-whole|LC 125 验证回文串]]（简单）· TikTok B · Amazon · Blind 75 · NeetCode 150 · Top Interview 150
- [[tlc-linked-list-cycle-ii-0-whole|LC 142 环形链表 II]]（中等）· TikTok B · Amazon · LeetCode Hot 100
- [[tlc-reorder-list-0-whole|LC 143 重排链表]]（中等）· TikTok B · Blind 75 · NeetCode 150
- [[tlc-sort-list-0-whole|LC 148 排序链表]]（中等）· TikTok B · Amazon · LeetCode Hot 100 · Top Interview 150
- LC 167 两数之和 II - 输入有序数组（中等）· Amazon · NeetCode 150 · Top Interview 150
- LC 202 快乐数（简单）· Amazon · NeetCode 150 · Top Interview 150
- [[tlc-palindrome-linked-list-0-whole|LC 234 回文链表]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- [[tlc-product-of-array-except-self-0-whole|LC 238 除了自身以外数组的乘积]]（中等）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-move-zeroes-0-whole|LC 283 移动零]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- [[tlc-find-the-duplicate-number-0-whole|LC 287 寻找重复数]]（中等）· TikTok B · NeetCode 150 · LeetCode Hot 100
- LC 392 判断子序列（简单）· Amazon · Top Interview 150
- [[tlc-permutation-in-string-0-whole|LC 567 字符串的排列]]（中等）· TikTok B · Amazon · NeetCode 150
- [[tlc-palindromic-substrings-0-whole|LC 647 回文子串]]（中等）· TikTok B · Blind 75 · NeetCode 150
- LC 763 划分字母区间（中等）· NeetCode 150 · LeetCode Hot 100

**再做（其余牌组里的题，24 道）**

- [[tlc-3sum-closest-0-whole|LC 16 最接近的三数之和]]（中等）· TikTok B · Amazon
- [[tlc-4sum-0-whole|LC 18 四数之和]]（中等）· TikTok B · Amazon
- [[tlc-compare-version-numbers-0-whole|LC 165 比较版本号]]（中等）· TikTok B
- LC 277 搜寻名人（中等）· Amazon
- [[tlc-create-maximum-number-0-whole|LC 321 拼接最大数]]（困难）· TikTok B
- LC 344 反转字符串（简单）· Amazon
- LC 349 两个数组的交集（简单）· Amazon
- LC 443 压缩字符串（中等）· Amazon
- [[tlc-assign-cookies-0-whole|LC 455 分发饼干]]（简单）· TikTok B
- LC 557 反转字符串中的单词 III（简单）· Amazon
- [[tlc-shortest-unsorted-continuous-subarray-0-whole|LC 581 最短无序连续子数组]]（中等）· TikTok B
- LC 658 找到 K 个最接近的元素（中等）· Amazon
- [[tlc-valid-palindrome-ii-0-whole|LC 680 验证回文串 II]]（简单）· TikTok B · Amazon
- [[tlc-find-k-th-smallest-pair-distance-0-whole|LC 719 找出第 K 小的数对距离]]（困难）· TikTok B
- LC 876 链表的中间结点（简单）· 
- [[tlc-boats-to-save-people-0-whole|LC 881 救生艇]]（中等）· TikTok B · Amazon
- [[tlc-sort-array-by-parity-0-whole|LC 905 按奇偶排序数组]]（简单）· TikTok B
- [[tlc-minimum-area-rectangle-0-whole|LC 939 最小面积矩形]]（中等）· TikTok B
- [[tlc-squares-of-a-sorted-array-0-whole|LC 977 有序数组的平方]]（简单）· TikTok B · Amazon
- [[tlc-two-sum-less-than-k-0-whole|LC 1099 小于 K 的两数之和]]（简单）· TikTok B
- LC 1650 二叉树的最近公共祖先 III（中等）· Amazon
- LC 1768 交替合并字符串（简单）· Amazon
- LC 2149 按符号重排数组（中等）· Amazon
- LC 2938 区分黑球与白球（中等）· Amazon
