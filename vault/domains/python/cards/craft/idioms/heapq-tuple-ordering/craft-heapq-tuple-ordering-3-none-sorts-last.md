---
id: craft-heapq-tuple-ordering-3-none-sorts-last
node: craft.idioms.heapq-tuple-ordering
type: qa
step: 3
---
## Q
**heapq 的元组序 · 「永不过期」怎么排在最后，又不让 None 和 datetime 比较**｜写法

额度包有的有到期时间，有的永不过期（`None`）。扣费要先扣快到期的，最后才扣永不过期的。直接把 `expires_at` 放进排序键会怎样？排序键 `(g.expires_at is None, g.expires_at, ...)` 为什么两个 `None` 之间也不会出错？

## A
**要点。** `None` 不能和 `datetime` 比较，`TypeError`。解法是在真正的值前面加一个**布尔标记**：`(expires_at is None, expires_at, ...)`。`False < True`，所以有到期时间的排在前面，`None` 的全部排到后面。标记已经把两类分开了，`None` 和 `datetime` 不会在同一位置被比较。

```python
t0 = datetime(2026, 1, 1)
grants = [("p1", None), ("p2", t0 + timedelta(days=3)), ("p3", t0 + timedelta(days=1)), ("p4", None)]

# 朴素版：expires_at 直接进元组，None 与 datetime 碰到一起就崩
try:
    heapq.heapify([(exp, gid) for gid, exp in grants])
except TypeError as e:
    print("直接放 None:", e)

# 键函数：先比「是不是永不过期」(False < True)，再比到期时间
def expiry_key(gid, exp):
    return (exp is None, exp, gid)

h = [expiry_key(g, e) for g, e in grants]
heapq.heapify(h)

print("先到期先扣, 永不过期最后:", [heapq.heappop(h)[2] for _ in grants])

# 为什么两个 None 比较不会崩：元组比较先用 == 找第一个不相等的位置，
# 只有找到了才对那一位用 <。两个 None 相等，就跳过去比下一位
print((True, None, "p1") < (True, None, "p4"))
```

实际输出：

```
直接放 None: '<' not supported between instances of 'datetime.datetime' and 'NoneType'
先到期先扣, 永不过期最后: ['p3', 'p2', 'p1', 'p4']
True
```

**为什么两个 None 也安全。** 元组比较先用 `==` 找第一个不相等的位置，找到后才对那一位用 `<`。两个 `None` 相等，直接跳到下一位去比，不会调用 `None < None`。

**代价。** 这个写法依赖「只有同一类的值才会走到同一位的比较」，所以后面的字段也要同样可比较（这里用 `gid` 兜底）。同一个思路可以泛化：任何「有的缺失」的排序键，都用 `(缺失吗, 值)` 来处理。
