---
id: craft-hash-map-plus-ordered-structure-1-lru-two-structures
node: craft.patterns.hash-map-plus-ordered-structure
type: qa
step: 1
---
## Q
**哈希表 + 有序结构 · 为什么 LRU 要两个结构配合**｜写法

LRU 缓存要同时做到：按 key 查找是 O(1)，访问后把条目标记成「最近使用」是 O(1)，满了淘汰「最久未用」的也是 O(1)。只用一个 `dict` 能做到吗？`dict` 加一个 `list` 记录顺序呢？

## A
**要点。** 一个结构只擅长一件事：哈希表擅长按 key 定位，不擅长按「新旧」排序；列表记录了顺序，但在中间摘除一个已知 key 要先 O(n) 找到它。需要两份结构分工，并且摘除要是 O(1)，经典答案是 dict（key→链表节点）加双向链表；Python 里 `OrderedDict` 已经把这套封好了，`move_to_end` 和 `popitem(last=False)` 两个调用就是 LRU。

```python
def get(self, k):
    if k not in self.d: return None
    self.d.move_to_end(k)              # 标记为最近使用：O(1)
    return self.d[k]

def put(self, k, v):
    self.d[k] = v
    self.d.move_to_end(k)
    if len(self.d) > self.cap:
        self.d.popitem(last=False)     # 弹出最久未用：O(1)

# 对照 LRUList：order.remove(k) 是 O(n) 查找
```

LeetCode 经典例子（容量 2，放 1、2，访问 1，放 3），以及 2 万个条目依次访问的耗时：

```
LeetCode 例子: key 2 被淘汰 -> None key 1 还在 -> 1
LRUOrdered  20000 次 get 耗时 0.001s
LRUList     20000 次 get 耗时 0.044s
```

耗时数字随机器变化；差别随容量增大线性放大（一边 O(n)，一边 O(1)）。

**代价。** 两份结构必须同步增删，否则 dict 里有的 key 链表里没有（或反过来）。不变式要写出来，操作都在同一把锁里（见第 4 张卡）。
