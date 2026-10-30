---
id: uth-python-typing-dataclasses-5-mutable-default
node: python.typing-dataclasses
type: qa
step: 5
---
## Q
**为什么 dataclass 拒绝 list 默认值**｜Python · CPython 3.14

普通类里写 `x = []` 能用，dataclass 里写 `xs: list = []` 却直接报 `ValueError`。它在防什么？正确写法是什么？

## A
**背景。** Python 把默认值存成类属性，所有实例共用同一个对象。普通类里写 `x = []`，两个实例的 `o1.x is o2.x` 为真：一个往里追加，另一个也看得到。

**结构。** `@dataclass` 创建类时检查默认值：它的类 `__hash__` 是 `None`（不可哈希，被当作「可变」的代理判断），就抛 `ValueError: mutable default <class 'list'> for field xs is not allowed: use default_factory`。正确写法是 `field(default_factory=list)`：没传参数时，生成的 `__init__` 每次调用 `list()` 现造一个。

```python
@dataclass
class W:
    xs: list = field(default_factory=list)
# W().xs is W().xs  ->  False，各有各的列表
```

**细节。**

- 判据是「不可哈希」，所以自己写的、可变但定义了 `__hash__` 的类不会被拦住。
- 没有默认值的字段不能排在有默认值的字段后面（`TypeError`），规则和函数参数一样；`kw_only=True`（3.10 起）可以绕开。
- `slots=True`（3.10 起）改用 `__slots__`，实例不再带 `__dict__`。

**例题：** LC 49 字母异位词分组

把字符串数组 `strs` 里互为字母异位词的分到同一组。例：`["eat","tea","tan","ate","nat","bat"]` → `[["bat"],["nat","tan"],["ate","eat","tea"]]`。`defaultdict(list)` 缺键时现造一个新列表，和 `default_factory` 是同一个想法。

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # 26 个字母的出现次数就是指纹
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # list 不可哈希，转成 tuple 才能当键
    return list(groups.values())
```
