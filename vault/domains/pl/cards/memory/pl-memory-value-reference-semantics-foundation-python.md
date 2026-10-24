---
id: pl-memory-value-reference-semantics-foundation-python
node: memory.value-reference-semantics
type: qa
step: 5
---
## Q
Python 里的变量到底是什么？“名字绑定到对象”的模型怎样解释赋值、可变对象和不可变对象？

## A
Python 里没有“装着值的盒子”，只有**对象**和指向对象的**名字**。`a = [1, 2]` 的意思是：在堆上创建一个列表对象，让名字 `a` 指向它。`b = a` 不复制任何东西，只是让 `b` 也指向同一个对象（`a is b` 为 `True`）。

对象分两种：
- **可变**（mutable）：列表、字典、集合、自定义对象。能原地修改，所有指向它的名字都看到变化。
- **不可变**（immutable）：整数、字符串、元组。不能原地修改；看似“修改”的操作其实创建了新对象并重新绑定名字。

```python
a = [1, 2]; b = a
b.append(3)         # mutates the one list
print(a)            # [1, 2, 3]
x = 10; y = x
y += 1              # int is immutable: y now names a new object 11
print(x, y)         # 10 11
```

传参同理：函数的形参只是新增一个名字指向同一个对象，所以函数里 `lst.append(99)` 会影响调用者，而 `lst = [0]` 只是让局部名字改指新对象，调用者不受影响。

要记住的一个事实：Python 里赋值永远不复制对象，只复制“指向”；想要独立副本，要显式调用 `copy.copy` 或 `copy.deepcopy`。
