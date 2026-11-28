---
id: py-out-mutation-augmented-assign
node: output.mutation
type: qa
step: 3
---
## Q
**+= 与 = 的区别**｜读代码说输出

```python
a = [1]
b = a
b += [2]
print(a)
b = b + [3]
print(a, b)
t = (1, 2)
u = t
u += (3,)
print(t, u)
```

输出什么？

## A
**输出。**

```
[1, 2]
[1, 2] [1, 2, 3]
(1, 2) (1, 2, 3)
```

**为什么。**

- 列表的 `b += [2]` 调用 `__iadd__`，在原对象上原地扩展，再把名字绑回同一个对象；`a` 和 `b` 是别名（alias），所以 `a` 也变了。
- `b = b + [3]` 用 `+` 造出一个新列表再绑给 `b`，`a` 保持不动。
- 元组不可变，没有 `__iadd__`，`+=` 退回到 `+`，造新元组；原来的 `t` 不变。

**语言为什么这样设计。**

- `+=` 先找 `__iadd__`，是为了让大对象原地修改、不必整体复制；找不到才退回 `__add__`，所以同一个运算符对可变和不可变类型表现不同。
- Java 的 `String +=` 总是新建对象，因为字符串不可变；Python 把这个选择交给类型自己决定。

**怎么写才对。**

```python
b = a.copy()      # 要独立副本
b = b + [3]       # 要新对象
```

**面试里一句话。**

Augmented assignment on a list mutates it in place via __iadd__, so every alias sees the change, while x = x + y rebinds to a new object.
