---
id: tlc-python-pitfalls-3-mutable-share
node: python.pitfalls
type: qa
step: 3
---
## Q
**Python 陷阱｜可变默认参数，以及回溯里 `res.append(path)` 为什么全变成空列表**

函数默认参数写 `acc=[]` 会怎样？回溯收集结果时，`res.append(path)` 和 `res.append(path[:])` 差在哪里？

## A
**默认参数只在定义函数时求值一次**，之后每次调用共用同一个对象：

```python
def bad(x: int, acc: list[int] = []) -> list[int]:
    acc.append(x)
    return acc
print(bad(1), bad(2))     # [1, 2] [1, 2]：两次调用共享同一个列表
def good(x: int, acc: list[int] | None = None) -> list[int]:
    acc = [] if acc is None else acc    # 每次调用新建
    acc.append(x)
    return acc
print(good(1), good(2))   # [1] [2]
```

**回溯同理**：`path` 是一个被反复 `append` / `pop` 的列表，结果里存的若是同一个对象的引用，回溯结束时它已经被弹空：

```python
res: list[list[int]] = []
path: list[int] = []
def bt(i: int) -> None:
    if i == 2:
        res.append(path[:])      # 拷贝一份；写成 res.append(path) 最后得到 [[], [], [], []]
        return
    for x in (0, 1):
        path.append(x); bt(i + 1); path.pop()
bt(0)
print(res)                       # [[0, 0], [0, 1], [1, 0], [1, 1]]
```

- 拷贝写法：`path[:]`、`list(path)`、`path.copy()`；元素是列表的嵌套结构要 `copy.deepcopy`。
- 适用题型：LC 39、40、46、47、77、78、79 等所有回溯题；也包括 LC 113 路径总和 II（`path` 在 DFS 里增删）。
- 用 `path + [x]` 作为参数传下去每层都会新建列表，不用手动 `pop`，也不会出现别名，代价是多一次 `O(len)` 拷贝。
