---
id: pl-memory-value-reference-semantics-pitfall-alias
node: memory.value-reference-semantics
type: qa
step: 6
---
## Q
Python 的 `[[0]*3]*3` 和默认参数 `acc=[]`、Go 的 `append` 到子 slice，这些「别名意外修改」的坑是怎么发生的？

## A
共同根因：你以为在复制，实际复制的是引用，多个名字共享了同一个可变对象。

Python 的两个经典例子：

```python
grid = [[0] * 3] * 3      # 3 references to ONE inner list
grid[0][0] = 1
print(grid)               # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

def add(x, acc=[]):       # the default is built once, at def time
    acc.append(x)
    return acc
print(add(1), add(2))     # [1, 2] [1, 2]
```

浅拷贝也救不了嵌套结构：`copy.copy(a)` 只复制外层列表，内层列表仍共享；需要 `copy.deepcopy`。

Go 的版本：

```go
a := []int{1, 2, 3, 4}
b := a[:2]                // shares a's backing array
b = append(b, 99)         // capacity left, so it writes into a
fmt.Println(a, b)         // [1 2 99 4] [1 2 99]
```

`b` 的容量足够，`append` 直接写进共享数组，覆盖了 `a[2]`。想要独立副本，先 `c := make([]int, 2); copy(c, a)`。

对策：嵌套可变结构用深拷贝或重新构造（`[[0]*3 for _ in range(3)]`）；默认参数用 `None` 再在函数内创建；Go 里需要独立 slice 时显式 `copy`，或用三下标切片 `a[:2:2]` 限制容量。
