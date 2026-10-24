---
id: pl-data-maps-intro-python
node: data.maps-collections
type: qa
step: 6
---
## Q
Python 的 `dict` 与 `set` 有哪些必须知道的行为？插入顺序保证、可哈希性、`1`/`1.0`/`True` 合并键分别是什么？

## A
**`dict`**：Python 的核心数据结构，类属性、模块命名空间、对象的 `__dict__` 都是它。当前实现是「紧凑字典」：一个稀疏的小索引数组（开放寻址）加一个按插入顺序存放（键、值、哈希）的稠密数组。这样既省内存，又天然保持插入顺序。

**插入顺序是语言保证**（Python 3.7 起，之前是 CPython 3.6 的实现细节）。真实例子：依次插入 `banana, apple, cherry`，把 `banana` 删除再重新插入，遍历结果是 `['apple', 'cherry', 'banana']`；更新已有键的值不改变它的位置。

**可哈希性**：键必须有稳定的 `__hash__`。可变内置类型不可哈希：

```python
{[1, 2]: 1}
# TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
```

自定义类如果重写了 `__eq__` 但没有同时定义 `__hash__`，Python 会把 `__hash__` 设为 `None`，实例就不能当键，真实报错 `unhashable type: 'P'`。这是语言在强制 `equals`/`hash` 契约。

**数值键会合并**：因为 `1 == 1.0 == True` 且哈希相同，`{1: 'a', 1.0: 'b', True: 'c'}` 的结果是 `{1: 'c'}`，只剩一项。

**`set`**：只有键的哈希表，成员检测 O(1)，支持并交差运算。字符串的哈希值每个进程随机化（防洪泛攻击），所以 `set` 的迭代顺序不稳定，而 `dict` 的稳定。

**要记住的一点**：Python 为 `dict` 做了大量优化，因为整个语言运行在它之上；日常能用 `dict` 就不要自造数据结构。
