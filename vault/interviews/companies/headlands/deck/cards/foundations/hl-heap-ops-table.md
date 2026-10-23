---
id: hl-heap-ops-table
node: foundations.heap-priority-queue
type: qa
step: 16
---
## Q
二叉堆的 peek、插入、poll、建堆、查找、删除任意值、按序遍历的复杂度各是多少？

## A
- 查看最小 `peek`：**O(1)**（在根）；
- 插入：**O(log n)**（上浮）；
- 取出最小 `poll`：**O(log n)**（下沉）；
- 建堆 n 个元素：**O(n)**（Floyd）；
- 查找某个值 `contains`：O(n)，只有父子有序，要全扫；
- 删除某个值 `remove(Object)`：O(n)，先找 O(n) 再摘掉 O(log n)；
- 按顺序遍历：不支持，数组顺序不是排序顺序。
