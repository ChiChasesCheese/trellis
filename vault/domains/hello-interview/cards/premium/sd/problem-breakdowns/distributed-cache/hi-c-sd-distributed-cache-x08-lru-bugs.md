---
id: hi-c-sd-distributed-cache-x08-lru-bugs
node: sd.problem-breakdowns.distributed-cache.exam
type: qa
step: 8
---
## Q
**分布式缓存 · 找错：LRU 的 get 里有什么 bug**｜考点 · 必会

下面的 get 在键过期时返回空。找出问题，说明运行一段时间之后会发生什么。

```python
def get(self, key):
    n = self.map.get(key)
    if n is None:
        return None
    self._unlink(n); self._push_front(n)   # 先标记最近使用
    if n.expiry and self.clock() > n.expiry:
        del self.map[key]                  # 过期：从哈希表删
        return None
    return n.value
```

## A
- **bug 一，只删了一边：** 过期节点仍挂在链表里，成了幽灵节点。之后链表尾被淘汰到它时，`del self.map[tail.key]` 抛 `KeyError`；实测容量为 2 的缓存在第三次插入后就崩溃。容量记账也不准，因为链表比哈希表长。
- **bug 二，顺序不对：** 过期的键先被移到表头再检查，浪费了一次操作，并且一个死节点占住"最近使用"的位置，让真正该留的数据更早被淘汰。应当先检查过期，再移动。
- **bug 三，`if n.expiry`：** 到期时间是 0.0 时被当成"没有过期时间"（假值），用注入时钟从 0 开始测试时过期永远不触发。应写 `is not None`。
- **边界：** 比较用 `>=` 还是 `>` 要和 set 里的定义一致，到期时刻本身算不算过期。
- **修复：** 过期与淘汰都走同一个 `_drop`，保证链表和哈希表一起删。
- **模式。** 单点写入：让所有"删除"只经过一个函数，不变量（两个结构一致）才守得住。
