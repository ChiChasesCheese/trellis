---
id: pl-foundations-paradigms-found-python-comprehension
node: foundations.paradigms
type: qa
step: 5
---
## Q
Python 的列表推导式和生成器表达式有什么区别？「一次性」是什么意思？

## A
推导式（comprehension）是 Python 把「过滤加映射」写成一个表达式的语法，形式借自数学里的集合描述 `{x² | x ∈ S, x 为偶数}`。方括号得到的是一个立刻算完的列表；圆括号得到的是生成器表达式（generator expression），它是一个惰性迭代器，每次被要求才算出下一个值。

```python
squares = [i * i for i in range(5) if i % 2 == 0]
g = (i * i for i in range(5) if i % 2 == 0)
print(squares, list(g), list(g))
```

实际输出：`[0, 4, 16] [0, 4, 16] []`。列表可以反复读；生成器被 `list(g)` 耗尽一次之后，第二次得到空列表，因为迭代器没有「倒带」。

要点：列表占内存、可重复遍历；生成器几乎不占内存（只保存当前位置）、只能遍历一次。`sum(i * i for i in ...)` 这种把生成器直接交给聚合函数的写法，是 Python 里最接近函数式管道的惯用法。
