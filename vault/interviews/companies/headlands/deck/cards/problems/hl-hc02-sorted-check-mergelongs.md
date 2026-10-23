---
id: hl-hc02-sorted-check-mergelongs
node: problems.hc02-merge-k-streams
type: qa
step: 6
---
## Q
堆合并怎样检查输入真的有序？`mergeLongs` 为什么能更快，自底向上建堆的复杂度是多少？

## A
**乱序检查**：每取下一个元素就与**上一个**比较，更小就抛 `UnsortedInputException(序列编号, 位置)`，每个元素 O(1)。「升序」是非降序，必须允许相等，所以用 `compareTo < 0`，不是 `a - b`。惰性版里检查发生在**读到那个元素的时候**，异常从 `hasNext()/next()` 抛出。

**`mergeLongs` 去装箱**：`PriorityQueue<Head<Long>>` 每元素一个 `Long` 对象，堆里是指针，比较时到处跳读（缓存未命中）。改成手写堆：堆里只放 `int` 序列号，数据留在 `long[][]` 里，比较读 `arrays[s][pos[s]]`，无分配、顺序读：约 65 ms（装箱版约 110 ms）。代价：代码长，下沉易写错；面试先写简单版，被追问性能再写。

```java
int[] pos = new int[k], heap = new int[k];
for (int i = n / 2 - 1; i >= 0; i--) siftDown(arrays, pos, heap, n, i);
```
**自底向上建堆** O(k)：从最后一个有孩子的节点 `n/2-1` 往前依次下沉，比 k 次上浮的 O(k log k) 快。序列用完时用堆尾顶替根再下沉；没用完时根的键变大，同样只需 `siftDown(…, 0)`。比较 `less(a,b)`：`va < vb || (va == vb && a < b)`。
