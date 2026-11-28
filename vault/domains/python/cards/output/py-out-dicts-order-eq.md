---
id: py-out-dicts-order-eq
node: output.dicts
type: qa
step: 4
---
## Q
**插入顺序、相等与不可哈希的键**｜读代码说输出

```python
d = {"a": 1, "b": 2, "c": 3}
d["a"] = 10
print(list(d))
del d["a"]; d["a"] = 1
print(list(d))
print({"x": 1, "y": 2} == {"y": 2, "x": 1}, [1, 2] == [2, 1])
try:
    {[1]: 2}
except TypeError as e:
    print(e)
```

输出什么？

## A
**输出。**
```
['a', 'b', 'c']
['b', 'c', 'a']
True False
cannot use 'list' as a dict key (unhashable type: 'list')
```

**为什么。**
- 字典按键第一次插入的顺序遍历（Python 3.7 起写进语言规范）。改已有键的值不换位置；删掉再插入才排到最后。
- 字典的 `==` 只比较键值对，不看顺序；列表 `==` 看顺序，所以 `[1, 2] != [2, 1]`。
- 键必须可哈希（hashable）。列表可变，哈希会随内容变，所以不允许做键，元组和 frozenset 可以。

**语言为什么这样设计。**
- 紧凑的字典实现（一个按插入顺序存的条目数组加一个稀疏索引表）既省内存又自带顺序，3.6 在 CPython 里实现，3.7 定为规范，代码才能放心依赖。
- Java 的 `HashMap` 不保证顺序，要顺序用 `LinkedHashMap`；JavaScript 对象保留插入顺序，但整数键会排到最前面。

**怎么写才对。**
```python
from collections import OrderedDict   # 只有需要“顺序参与相等比较”或 move_to_end 时才用
```

**面试里一句话。**
Dicts keep insertion order since Python 3.7 but compare equal regardless of order, and keys must be hashable so mutable lists are rejected.
