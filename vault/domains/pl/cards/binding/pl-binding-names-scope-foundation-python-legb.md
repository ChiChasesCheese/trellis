---
id: pl-binding-names-scope-foundation-python-legb
node: binding.names-scope
type: qa
step: 2
---
## Q
Python 的 LEGB 规则是什么？为什么函数里先读后赋同一个名字会得到 `UnboundLocalError`，`nonlocal` 又解决什么问题？

## A
Python 的作用域是**函数级**的，没有块作用域。查找一个名字依次经过四层，简称 LEGB：局部（Local，当前函数）、外层函数（Enclosing）、全局（Global，当前模块）、内置（Built-in，如 `len`）。

关键规则：**只要函数体里任何位置对名字有赋值，这个名字在整个函数里都是局部变量**。编译器在编译函数时就按这个规则分类，不看执行顺序：

```python
x = 10
def f():
    print(x)      # x is local here, because of the next line
    x = 5
f()
# UnboundLocalError: cannot access local variable 'x'
#   where it is not associated with a value
```

`print(x)` 并没有去读全局的 `10`，因为 `x` 已被判定为局部，而它此刻还没有值。

内层函数想**修改**外层函数的变量，必须声明，否则赋值只会新建一个局部变量：

```python
def counter():
    n = 0
    def inc():
        nonlocal n      # rebind the enclosing n, not a new local
        n += 1
        return n
    return inc
c = counter(); c(); print(c())    # 2
```

`global` 对模块级变量起同样作用。循环变量也不在块里：`for i in range(3): pass` 之后 `i` 仍然存在，值是 `2`。

要记住的事实：Python 把「读」的作用域规则做得宽松（逐层向外找），把「写」的规则做得严格（默认就是局部），目的是不让你无意中改动外层状态。
