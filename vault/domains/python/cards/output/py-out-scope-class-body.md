---
id: py-out-scope-class-body
node: output.scope
type: qa
step: 4
---
## Q
**类体里的推导式**｜读代码说输出

```python
class A:
    x = 10
    try:
        ys = [x for _ in range(2)]
    except NameError as e:
        print(e)
    zs = [i for i in range(x)]
    ws = [x] * 2
print(A.zs[-1], A.ws)
```

输出什么？

## A
**输出。**

```
name 'x' is not defined
9 [10, 10]
```

**为什么。**

- 类体（class body）是一个临时作用域，只在执行类体的那一刻存在；嵌套的函数和推导式（comprehension）看不到它的名字。
- `[x for _ in range(2)]` 里的 `x` 在推导式内部查找，找不到类体里的 `x`，报 NameError；Python 3.12 起推导式被内联（PEP 709），这条规则仍然保留。
- `range(x)` 是推导式最外层的可迭代对象，它在类体里先求值，所以 `x` 能找到，`zs` 正常。

**语言为什么这样设计。**

- 类体作用域不参与闭包，是为了让方法里的名字不会悄悄指到类属性：方法里要用类属性必须写 `self.x` 或 `A.x`，一眼看出来自哪里。
- Java 和 C++ 的方法可以直接写成员名（隐式 `this`）；Python 选了显式，代价就是类体里这种嵌套写法会踩坑。

**怎么写才对。**

```python
ws = [x] * 2   # 直接在类体里用；方法里写 self.x
```

**面试里一句话。**

A class body is not an enclosing scope, so functions and comprehensions nested in it cannot see its names except the outermost iterable.
