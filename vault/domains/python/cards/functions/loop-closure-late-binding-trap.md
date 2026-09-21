---
id: loop-closure-late-binding-trap
node: functions.scope-closure
type: qa
source: python-docs
---
## Q
用 `for` 循环批量创建多个 lambda（等价于 `[lambda: x**2 for x in range(5)]`）时，为什么调用它们全部返回同一个结果，而不是各自对应循环当时的 x？应该怎么修？

## A
闭包（closure）捕获的是自由变量本身的绑定，不是定义那一刻的值；调用 lambda 时才去外层作用域读取 `x` 的当前值，此时循环早已结束，`x` 停在最后一次迭代的值上，所以所有 lambda 返回同一个结果——这叫「迟绑定」（late binding）。修法：用默认参数在定义时把值固定下来，例如 `lambda x=x: x**2`，或者写一个工厂函数 `def make(x): return lambda: x**2`，让每次调用都产生独立的局部变量。
