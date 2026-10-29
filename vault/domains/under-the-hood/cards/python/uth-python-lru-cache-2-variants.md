---
id: uth-python-lru-cache-2-variants
node: python.lru-cache
type: qa
step: 2
---
## Q
**lru_cache 的三种模式**｜Python · CPython 3.14

`lru_cache(maxsize=None)`、`maxsize=0`、`functools.cache` 内部分别走什么路径？缓存的 key 是什么？

## A
**结构。** 创建时按 `maxsize` 选三个包装函数之一。

**细节。**

- `maxsize=None`：只用 `dict`，没有链表，也不淘汰，更快。`functools.cache` 就是 `lru_cache(maxsize=None)`。
- `maxsize=0`：不缓存，直接调用原函数。
- key 是位置参数元组（带关键字参数时再拼上分隔标记）；只有一个 `int` 或 `str` 参数时，直接拿它当 key，省掉一个元组。

**为什么。** 无限缓存不用维护顺序，省掉每次命中的链表操作。

**坑。** 参数必须可哈希，传 `list` 会抛 `TypeError: unhashable type: 'list'`。

**对应 LeetCode：** LC 70 爬楼梯 · LC 509 斐波那契数
