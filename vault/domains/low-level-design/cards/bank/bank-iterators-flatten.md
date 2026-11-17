---
id: bank-iterators-flatten
node: bank.structures.iterators
type: qa
step: 2
---
## Q
实现 `flatten([1, [2, [3, "ab"]], (4,)])`，按顺序惰性地产出 1、2、3、`"ab"`、4。用 `isinstance(x, Iterable)` 判断「要不要展开」会出什么问题？

## A
**递归生成器，只展开认定的容器类型**

- **递归加 `yield from`**：遇到容器就 `yield from flatten(item)`，否则 `yield item`；惰性，调用方取到哪里就算到哪里；
- **`str` 是陷阱**：`"ab"` 是 `Iterable`，它的元素 `"a"` 还是长度为 1 的 `str`，还是 `Iterable`，永远展开不完，最后 `RecursionError`。代码最后一行的 `list("a")` 就是 `['a']`；
- **写明要展开什么**：`(list, tuple)`，或者先排除 `str` 和 `bytes`，不要靠「能不能迭代」；
- **深度有上限**：递归深度受 `sys.getrecursionlimit()` 限制（默认 1000）。实测嵌套 2000 层的列表会 `RecursionError`；
- **结果是迭代器**：返回的生成器只能走一遍。要做成带 `has_next` 的类，就把它包进一个窥视迭代器（`Peekable`）。

```python
from collections.abc import Iterable
def flatten(x):
    for item in x:
        if isinstance(item, (list, tuple)):          # 只展开容器，不用 Iterable
            yield from flatten(item)
        else:
            yield item

print(list(flatten([1, [2, [3, "ab"]], (4,)])))      # [1, 2, 3, 'ab', 4]
print(isinstance("ab", Iterable), list("a"))         # True ['a']：str 的元素还是 str
```

<details class="pt"><summary>延伸</summary>

嵌套可能很深时，把递归换成显式的迭代器栈：栈里放的是迭代器，不是值；当前迭代器耗尽就弹栈，遇到容器就压入它的迭代器。

```python
def flatten(x):
    stack = [iter(x)]
    while stack:
        for item in stack[-1]:
            if isinstance(item, (list, tuple)):
                stack.append(iter(item)); break      # 先走进去，回来再接着走外层
            yield item
        else:
            stack.pop()                              # 这一层走完
```

实测它能展开 2000 层嵌套的空列表而不报错。

</details>

**知识点：**迭代器设计（Iterator Design）
