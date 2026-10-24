---
id: pl-functional-closures-foundation-python-cells
node: functional.closures
type: qa
step: 5
---
## Q
Python 的闭包是怎么存放被捕获变量的？`nonlocal` 和「晚绑定」是什么意思？

## A
Python 的内层函数引用外层函数的局部变量时，这个变量被放进一个**单元**（cell）对象，内外两个函数共享这个 cell。闭包持有的是对 cell 的引用，所以读到的永远是变量**当前**的值，而不是定义闭包时的值，这叫**晚绑定**（late binding）。

```python
def outer():
    x = 1
    def get(): return x
    x = 2
    return get
outer()()          # 2，不是 1
```

可以通过 `f.__closure__[0].cell_contents` 直接看到那个 cell 里的值。

读取外层变量不需要任何声明；但**赋值**会被当成创建新的局部变量，所以要修改外层变量必须用 `nonlocal` 声明：

```python
def counter():
    n = 0
    def inc():
        nonlocal n      # 没有这行，n += 1 会报 UnboundLocalError
        n += 1
        return n
    return inc
c = counter(); c(); c()    # 2
```

`nonlocal` 对应的是 Go 里默认就有的能力；Python 要显式写，是因为它的变量没有声明语句，用「赋值即声明」的规则，所以需要一个关键字来区分「改外层的」和「新建局部的」。

晚绑定符合直觉（闭包看到最新值），但在循环里创建闭包时会造成最经典的陷阱（见后文）。
