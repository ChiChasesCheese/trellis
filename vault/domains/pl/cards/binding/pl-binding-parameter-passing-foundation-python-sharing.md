---
id: pl-binding-parameter-passing-foundation-python-sharing
node: binding.parameter-passing
type: qa
step: 3
---
## Q
Python 的参数传递叫什么？为什么 `n += 1` 对整数不影响调用者，对列表却会？

## A
Python 的传参叫**传共享**（call by sharing，也有人叫 call by object reference）。形参只是新增一个名字，指向调用者传来的**同一个对象**；函数里给形参赋值，只是让这个局部名字改指别的对象，调用者的名字不受影响。

```python
def rebind(xs): xs = [99]
def mutate(xs): xs.append(99)
def incr(n): n += 1
l = [1]; rebind(l); print(l)   # [1]       rebinding the local name
mutate(l); print(l)            # [1, 99]   same object, changed in place
n = 1; incr(n); print(n)       # 1
```

整数和列表的区别不在传递方式，而在**对象能不能被原地修改**：整数是不可变对象，`n += 1` 的含义是「创建新对象 `2`，让局部名字 `n` 指向它」，调用者的 `n` 仍指向 `1`。列表是可变对象，`append` 在原对象上修改，所有指向它的名字都看到。对列表写 `xs += [1]` 则是原地扩展（调用的是 `__iadd__`），同样会影响调用者。

验证对象确实是同一个：

```python
def ident(x): return id(x)
a = [1]; print(ident(a) == id(a))   # True
```

和 Java 的行为在引用类型上完全一致；区别是 Python 里**没有基本类型**，一切都是对象，所以「是否会被改」只取决于对象本身是否可变。

结论：读 Python 代码时要问的是「这个对象可变吗？」，而不是「怎么传的」。想要独立副本，调用者要显式 `copy.copy` 或 `list(xs)`，函数要保护调用者的数据则在函数里先复制。
