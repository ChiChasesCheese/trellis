---
id: uth-python-lru-cache-3-method-leak
node: python.lru-cache
type: qa
step: 3
---
## Q
**给方法加 lru_cache 为什么会内存泄漏**｜Python · CPython 3.14

在类的方法上用 `@lru_cache(maxsize=None)`，实例 `del` 之后为什么还活着？

## A
**结构。** 缓存挂在函数上，不在实例上；`self` 也是参数，成了缓存 key 的一部分。

**细节。**

- 缓存的 `dict` 持有 key，也就持有了 `self`，实例的引用计数不会归零。
- 实测：调用 `a.m(1)` 后 `del a`，再 `gc.collect()`，弱引用仍然指向存活的实例。
- 有大小上限时，实例要等被淘汰出缓存才会释放。

**为什么。** 缓存的寿命等同函数本身，key 必须强引用才能比较。

**坑。** 要按实例缓存，就在 `__init__` 里给每个实例单独包一个缓存函数。

**对应 LeetCode：** LC 139 单词拆分 · LC 322 零钱兑换
