---
id: uth-python-deque-ordereddict-3-ordereddict
node: python.deque-ordereddict
type: qa
step: 3
---
## Q
**OrderedDict 怎么 O(1) 移到末尾**｜Python · CPython 3.14

普通 `dict` 已经保序了，`OrderedDict` 还多做了什么？`move_to_end` 为什么能 O(1)？

## A
**结构。** `dict` 之外再挂一条双向链表记顺序；另有一个数组镜像 `dict` 的条目顺序，存每个 key 的节点指针，用来 O(1) 找节点。

**细节。**

- `move_to_end(k)` 摘下节点接到链表尾，`popitem(last=False)` 弹出链表头，都是 O(1)。
- 两个 `OrderedDict` 相等要求顺序也一样（实测 `False`），普通 `dict` 则不要求（实测 `True`）。

**为什么。** 单纯加链表会让删除中间节点退化成 O(n)，所以必须有从 key 直达节点的映射。

**坑。** 实测 1000 个键，`OrderedDict` 占 85400 字节，普通 `dict` 占 36952。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
