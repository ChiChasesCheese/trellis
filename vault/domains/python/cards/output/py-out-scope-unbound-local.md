---
id: py-out-scope-unbound-local
node: output.scope
type: qa
step: 2
---
## Q
**先读后赋值**｜读代码说输出

```python
x = 1
def f():
    print(x)
    x = 2
try:
    f()
except Exception as e:
    print(type(e).__name__, e)
```

输出什么？

## A
**输出。**

```
UnboundLocalError cannot access local variable 'x' where it is not associated with a value
```

**为什么。**

- 编译 `f` 时，只要函数体里有对 `x` 的赋值，`x` 在整个函数里就是局部变量（local）。
- 于是 `print(x)` 去读局部的 `x`，而它还没被赋值，抛出 UnboundLocalError；全局的 `x = 1` 根本没被看一眼。
- 作用域是编译期按名字决定的，不是运行到哪一行才决定。

**语言为什么这样设计。**

- 局部变量存在固定的槽位里（fast locals），按下标读写，比字典查找快；这要求编译期就知道每个名字是不是局部。
- Python 没有变量声明语法，赋值本身就是声明，所以要改全局或外层变量必须用 `global` / `nonlocal` 明说。JavaScript 的 `let` 有类似的暂时性死区（TDZ）；Lua 则相反，默认全局，局部要写 `local`。

**怎么写才对。**

```python
def f():
    global x   # 真要改全局；更好的是传参、返回值
    print(x)
    x = 2
```

**面试里一句话。**

Assigning to a name anywhere in a function makes it local for the whole function, so reading it before the assignment raises UnboundLocalError.
