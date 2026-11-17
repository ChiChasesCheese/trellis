---
id: fluency-mutability-names-not-boxes
node: fluency.mutability
type: qa
step: 1
---
## Q
`b = a` 之后 `b.append(3)`，为什么 `a` 也变了？而 `n = 5; m = n; m += 1` 之后 `n` 还是 5？`is` 和 `==` 各问的是什么？

## A
**变量是贴在对象上的名字，不是装值的盒子**

- **赋值只绑定名字**：`b = a` 没有复制，两个名字指向同一个对象；通过任何一个名字改对象，另一个名字都看得见；
- **可变与不可变对象**：`list`、`dict`、`set` 和自定义类的实例可以原地修改；`int`、`str`、`tuple`、`frozenset` 不能；对不可变值做 `m += 1` 是让 `m` 重新绑定到新对象，`n` 不受影响；
- **`is` 问“同一个对象吗”，`==` 问“值相等吗”**：`list(a) == a` 为 `True`，`list(a) is a` 为 `False`；判断别名关系用 `is`，业务比较用 `==`；
- **函数参数也是别名**：调用时，形参和实参指向同一个对象，函数里原地改，调用方看得见；函数里重新绑定（`xs = xs + [9]`）不影响调用方；
- **定位这类 bug 的办法**：怀疑共享就打印 `id(x)` 或用 `is` 比较，别靠“看起来是两份数据”。

```python
a = [1, 2]
b = a                      # 同一个对象，两个名字
c = list(a)                # 新对象，内容相同
b.append(3)
print(a, c, a is b, a is c)    # [1, 2, 3] [1, 2] True False

n = 5; m = n; m += 1       # int 不可变：m 绑定到新对象 6
t = (1, 2); u = t; t += (3,)
print(n, m, t, u)          # 5 6 (1, 2, 3) (1, 2)
```

**知识点：**可变性与别名（Mutability & Aliasing）
