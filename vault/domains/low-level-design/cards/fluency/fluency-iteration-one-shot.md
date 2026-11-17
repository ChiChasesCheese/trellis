---
id: fluency-iteration-one-shot
node: fluency.iteration
type: qa
step: 1
---
## Q
函数收到一个“关键词的可迭代对象”，先 `len(...)` 校验、再遍历匹配。调用方传的是生成器或 `map(...)`，为什么第二次遍历什么都没有？怎么写才对一次性迭代器安全？

## A
**迭代器只能走一遍：先读成快照**

- **可迭代（iterable）与迭代器（iterator）**：`list`、`tuple`、`dict`、`str` 每次 `for` 都从头开始；生成器、`map`、`zip`、`filter`、文件对象本身就是迭代器，走完就空了，不会重置；
- **没有错误提示**：第二次遍历得到零个元素，代码把它当成“没有数据”，结果悄悄变成空；
- **`len()` 和 `if it:`**：迭代器没有长度，`len(gen)` 抛 `TypeError`；`bool(gen)` 永远是 `True`，不能用来判断是否为空；
- **`x in it` 也会消耗**：它从当前位置往后找，找到之前的元素都被吃掉；
- **做法**：入口先 `items = tuple(items)` 或 `list(items)`，之后随便遍历、取长度、检查；这也让函数不受调用方之后再改原列表的影响；
- **数据量大、只想走一遍时**：就保持为迭代器、只遍历一次，不要同时又要长度。

```python
def total(words):
    words = tuple(words)               # 快照：可以重复遍历，也有长度
    if not words:
        raise ValueError("empty")
    return len(words), sum(len(w) for w in words)

gen = (w for w in ["ab", "c"])
print(list(gen), list(gen), bool(gen))   # ['ab', 'c'] [] True
print(total(w for w in ["ab", "c"]))     # (2, 3)
it = iter([1, 2, 3]); print(1 in it, list(it))   # True [2, 3]
```

**知识点：**迭代写法（Iteration Style）
