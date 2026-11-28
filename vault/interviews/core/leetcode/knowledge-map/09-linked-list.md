# 链表技巧

指针操作的基本功：哑节点、快慢指针、原地反转、合并。LRU 的双向链表、K 个一组翻转都建立在这几个动作上。

**先做（TikTok P1–P4 与经典题单，29 道）**

- [[lct-lru-cache|LC 146 LRU 缓存]]（中等）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-reverse-nodes-in-k-group|LC 25 K 个一组翻转链表]]（困难）· TikTok P1 · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-reverse-linked-list|LC 206 反转链表]]（简单）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100
- [[lct-remove-nth-node-from-end-of-list|LC 19 删除链表的倒数第 N 个结点]]（中等）· TikTok P1 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-merge-k-sorted-lists|LC 23 合并 K 个升序链表]]（困难）· TikTok P2 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-design-hashmap|LC 706 设计哈希映射]]（简单）· TikTok P2
- [[lct-all-oone-data-structure|LC 432 全 O(1) 的数据结构]]（困难）· TikTok P2
- [[lct-intersection-of-two-linked-lists|LC 160 相交链表]]（简单）· TikTok P2 · LeetCode Hot 100
- [[lct-linked-list-cycle|LC 141 环形链表]]（简单）· TikTok P3 · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-design-circular-queue|LC 622 设计循环队列]]（中等）· TikTok P3 · Amazon
- [[lct-add-two-numbers-ii|LC 445 两数相加 II]]（中等）· TikTok P3
- [[lct-populating-next-right-pointers-in-each-node|LC 116 填充每个节点的下一个右侧节点指针]]（中等）· TikTok P4 · Amazon
- [[lct-flatten-a-multilevel-doubly-linked-list|LC 430 扁平化多级双向链表]]（中等）· TikTok P4
- [[lct-remove-duplicates-from-sorted-list|LC 83 删除排序链表中的重复元素]]（简单）· TikTok P4
- [[lct-add-two-numbers|LC 2 两数相加]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-merge-two-sorted-lists|LC 21 合并两个有序链表]]（简单）· TikTok B · Amazon · Blind 75 · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-swap-nodes-in-pairs|LC 24 两两交换链表中的节点]]（中等）· TikTok B · LeetCode Hot 100
- [[lct-rotate-list|LC 61 旋转链表]]（中等）· TikTok B · Amazon · Top Interview 150
- [[lct-remove-duplicates-from-sorted-list-ii|LC 82 删除排序链表中的重复元素 II]]（中等）· TikTok B · Top Interview 150
- [[lct-partition-list|LC 86 分隔链表]]（中等）· TikTok B · Top Interview 150
- [[lct-reverse-linked-list-ii|LC 92 反转链表 II]]（中等）· TikTok B · Amazon · Top Interview 150
- [[lct-flatten-binary-tree-to-linked-list|LC 114 二叉树展开为链表]]（中等）· TikTok B · LeetCode Hot 100 · Top Interview 150
- LC 117 填充每个节点的下一个右侧节点指针 II（中等）· Top Interview 150
- [[lct-copy-list-with-random-pointer|LC 138 随机链表的复制]]（中等）· TikTok B · Amazon · NeetCode 150 · LeetCode Hot 100 · Top Interview 150
- [[lct-linked-list-cycle-ii|LC 142 环形链表 II]]（中等）· TikTok B · Amazon · LeetCode Hot 100
- [[lct-reorder-list|LC 143 重排链表]]（中等）· TikTok B · Blind 75 · NeetCode 150
- [[lct-sort-list|LC 148 排序链表]]（中等）· TikTok B · Amazon · LeetCode Hot 100 · Top Interview 150
- [[lct-palindrome-linked-list|LC 234 回文链表]]（简单）· TikTok B · Amazon · LeetCode Hot 100
- LC 355 设计推特（中等）· NeetCode 150

**再做（其余牌组里的题，14 道）**

- LC 109 有序链表转换二叉搜索树（中等）· Amazon
- [[lct-delete-node-in-a-linked-list|LC 237 删除链表中的节点]]（中等）· TikTok B
- [[lct-odd-even-linked-list|LC 328 奇偶链表]]（中等）· TikTok B · Amazon
- [[lct-plus-one-linked-list|LC 369 给单链表加一]]（中等）· TikTok B
- [[lct-convert-binary-search-tree-to-sorted-doubly-linked-list|LC 426 将二叉搜索树转化为排序的双向链表]]（中等）· TikTok B
- [[lct-lfu-cache|LC 460 LFU 缓存]]（困难）· TikTok B · Amazon
- [[lct-insert-into-a-sorted-circular-linked-list|LC 708 循环有序列表的插入]]（中等）· TikTok C
- [[lct-max-stack|LC 716 最大栈]]（困难）· TikTok C
- LC 876 链表的中间结点（简单）· 
- [[lct-remove-zero-sum-consecutive-nodes-from-linked-list|LC 1171 从链表中删去总和值为零的连续节点]]（中等）· TikTok B
- LC 1472 设计浏览器历史记录（中等）· Amazon
- [[lct-merge-in-between-linked-lists|LC 1669 合并两个链表]]（中等）· TikTok B
- [[lct-reverse-nodes-in-even-length-groups|LC 2074 反转偶数长度组的节点]]（中等）· TikTok B
- [[lct-double-a-number-represented-as-a-linked-list|LC 2816 翻倍以链表形式表示的数字]]（中等）· TikTok B
