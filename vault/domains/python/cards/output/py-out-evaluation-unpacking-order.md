---
id: py-out-evaluation-unpacking-order
node: output.evaluation
type: qa
step: 4
---
## Q
**解包赋值的顺序**｜读代码说输出

```python
a = [0, 0]
i = 0
i, a[i] = 1, 5
print(i, a)
x, y = 1, 2
x, y = y, x + y
print(x, y)
b = [1, 2, 3]
j = 0
j, b[j] = b[j], 99
print(j, b)
```

输出什么？

## A
**输出。**

```
1 [0, 5]
2 3
1 [1, 99, 3]
```

**为什么。**

- 赋值先把右边整个求值完，得到一个元组，然后从左到右依次给目标赋值。
- `i, a[i] = 1, 5`：先 `i = 1`，轮到 `a[i]` 时才计算下标，此时 `i` 已是 1，所以改的是 `a[1]`，不是 `a[0]`。
- `x, y = y, x + y` 右边先算出 `(2, 3)`，所以不需要临时变量就能交换；最后一段右边是 `(1, 99)`，同样先 `j = 1` 再 `b[1] = 99`。

**语言为什么这样设计。**

- 语言参考规定：右边先求值，左边目标按从左到右赋值，目标里的下标表达式在轮到它时才求值；这条规则让交换和斐波那契迭代一行写完。
- Go 的元组赋值把左边的下标表达式也提前求值：同样的 `i, a[i] = 1, 5` 在 Go 里得到 `1 [5 0]`，改的是 `a[0]`。

**怎么写才对。**

```python
idx = i
a[idx], i = 5, 1     # 目标里依赖被赋值的名字时，拆开写或先保存
```

**面试里一句话。**

Python evaluates the whole right side first and then assigns targets left to right, so a subscript on the left sees names that were already reassigned.
