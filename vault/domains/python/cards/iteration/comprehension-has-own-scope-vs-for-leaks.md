---
id: comprehension-has-own-scope-vs-for-leaks
node: iteration.comprehensions
type: qa
source: python-docs
---
## Q
`squares = [x**2 for x in range(10)]` 执行完之后，外层作用域里还能不能访问到 `x`？和显式写 `for x in range(10): squares.append(x**2)` 相比有什么不同？

## A
不能，`x` 在推导式结束后不存在于外层作用域——推导式（包括生成器表达式）从 Python 3 起拥有自己独立的作用域（own scope），循环变量只在推导式内部可见，不会覆盖外层同名变量。显式 `for` 循环则相反：循环变量是在当前作用域里直接赋值的，循环结束后仍保留最后一次迭代的值，会覆盖之前同名的任何变量。
