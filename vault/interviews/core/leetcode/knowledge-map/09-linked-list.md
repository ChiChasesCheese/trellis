# 链表技巧

指针操作的基本功：哑节点、快慢指针、原地反转、合并。LRU 的双向链表、K 个一组翻转都建立在这几个动作上。

**先做（TikTok P1–P4 与经典题单，29 道）**

- [[tlc-lru-cache-0-whole|LC 146 LRU 缓存]]（中等）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-reverse-nodes-in-k-group-0-whole|LC 25 K 个一组翻转链表]]（困难）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-reverse-linked-list-0-whole|LC 206 反转链表]]（简单）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100
- [[tlc-remove-nth-node-from-end-of-list-0-whole|LC 19 删除链表的倒数第 N 个结点]]（中等）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-merge-k-sorted-lists-0-whole|LC 23 合并 K 个升序链表]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-design-hashmap-0-whole|LC 706 设计哈希映射]]（简单）· TikTok P3
- [[tlc-intersection-of-two-linked-lists-0-whole|LC 160 相交链表]]（简单）· TikTok P3 · LeetCode Hot 100
- [[tlc-linked-list-cycle-0-whole|LC 141 环形链表]]（简单）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-design-circular-queue-0-whole|LC 622 设计循环队列]]（中等）· TikTok P3 · Amazon
- [[tlc-add-two-numbers-ii-0-whole|LC 445 两数相加 II]]（中等）· TikTok P3
- [[tlc-all-oone-data-structure-0-whole|LC 432 全 O(1) 的数据结构]]（困难）· TikTok P4
- [[tlc-flatten-a-multilevel-doubly-linked-list-0-whole|LC 430 扁平化多级双向链表]]（中等）· TikTok P4
- [[tlc-remove-duplicates-from-sorted-list-0-whole|LC 83 删除排序链表中的重复元素]]（简单）· TikTok P4
- [[tlc-populating-next-right-pointers-in-each-node-0-whole|LC 116 填充每个节点的下一个右侧节点指针]]（中等）· TikTok P4 · Amazon
- [[tlc-add-two-numbers-0-whole|LC 2 两数相加]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-merge-two-sorted-lists-0-whole|LC 21 合并两个有序链表]]（简单）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-swap-nodes-in-pairs-0-whole|LC 24 两两交换链表中的节点]]（中等）· TikTok B · LeetCode Hot 100
- [[tlc-rotate-list-0-whole|LC 61 旋转链表]]（中等）· TikTok B · Amazon · Top Interview 150
- [[tlc-remove-duplicates-from-sorted-list-ii-0-whole|LC 82 删除排序链表中的重复元素 II]]（中等）· TikTok B · Top Interview 150
- [[tlc-partition-list-0-whole|LC 86 分隔链表]]（中等）· TikTok B · Top Interview 150
- [[tlc-reverse-linked-list-ii-0-whole|LC 92 反转链表 II]]（中等）· TikTok B · Amazon · Top Interview 150
- [[tlc-flatten-binary-tree-to-linked-list-0-whole|LC 114 二叉树展开为链表]]（中等）· TikTok B · LeetCode Hot 100 · Top Interview 150
- LC 117 填充每个节点的下一个右侧节点指针 II（中等）· Top Interview 150
- [[tlc-copy-list-with-random-pointer-0-whole|LC 138 随机链表的复制]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[tlc-linked-list-cycle-ii-0-whole|LC 142 环形链表 II]]（中等）· TikTok B · Amazon · LeetCode Hot 100
- [[tlc-reorder-list-0-whole|LC 143 重排链表]]（中等）· TikTok B · Blind 75 · NeetCode 150
- [[tlc-sort-list-0-whole|LC 148 排序链表]]（中等）· TikTok B · Amazon · LeetCode Hot 100 · Top Interview 150
- [[tlc-palindrome-linked-list-0-whole|LC 234 回文链表]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- LC 355 设计推特（中等）· NeetCode 150

**再做（其余牌组里的题，12 道）**

- LC 109 有序链表转换二叉搜索树（中等）· Amazon
- [[tlc-delete-node-in-a-linked-list-0-whole|LC 237 删除链表中的节点]]（中等）· TikTok B
- [[tlc-odd-even-linked-list-0-whole|LC 328 奇偶链表]]（中等）· TikTok B · Amazon
- [[tlc-plus-one-linked-list-0-whole|LC 369 给单链表加一]]（中等）· TikTok B
- [[tlc-convert-binary-search-tree-to-sorted-doubly-linked-list-0-whole|LC 426 将二叉搜索树转化为排序的双向链表]]（中等）· TikTok B
- [[tlc-lfu-cache-0-whole|LC 460 LFU 缓存]]（困难）· TikTok B · Amazon
- LC 876 链表的中间结点（简单）· 
- [[tlc-remove-zero-sum-consecutive-nodes-from-linked-list-0-whole|LC 1171 从链表中删去总和值为零的连续节点]]（中等）· TikTok B
- LC 1472 设计浏览器历史记录（中等）· Amazon
- [[tlc-merge-in-between-linked-lists-0-whole|LC 1669 合并两个链表]]（中等）· TikTok B
- [[tlc-reverse-nodes-in-even-length-groups-0-whole|LC 2074 反转偶数长度组的节点]]（中等）· TikTok B
- [[tlc-double-a-number-represented-as-a-linked-list-0-whole|LC 2816 翻倍以链表形式表示的数字]]（中等）· TikTok B
