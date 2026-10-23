---
id: hl-cache-locality-vs-algo
node: foundations.cpu-cache-locality
type: qa
step: 12
---
## Q
局部性如何改变算法选择？为什么 `HashMap.get` 要 10 ns、堆排序比快排慢、排好序的数组常打败 `TreeMap`？

## A
- 数组顺序扫描（O(n)）常比更聪明的指针结构（链表、树）更快，即使后者渐近更好；n 不特别大时，**排好序的数组 + 线性或二分查找常打败 `TreeMap`**。
- 哈希表的随机访问基本每次都缓存缺失（桶位置随机），这是 `HashMap.get` 要 10 ns 而不是 1 ns 的原因之一。
- 堆（`PriorityQueue`）虽是数组，但父到子的跳跃（i → 2i+1）在大堆里跨缓存行，所以堆排序比快排慢。
