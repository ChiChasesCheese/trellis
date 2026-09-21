---
id: exec-eval-skip-enclosing-closure-scope
node: runtime.namespaces-execution
type: qa
source: python-docs
---
## Q
在一个嵌套函数内部直接调用不带参数的 `eval()`/`exec()`，它能访问到跟普通代码完全一样的名字解析环境吗？

## A
不能。普通代码里的自由变量按「最近的外层作用域」逐层查找（闭包链）；而 `eval()`/`exec()` 只能拿到调用者当时的局部命名空间和全局命名空间这两层，自由变量一律直接在全局命名空间里查找，跳过中间的闭包层。所以在嵌套函数里用 `exec()` 执行一段引用了外层函数局部变量的代码，很可能因为这个变量根本不在全局命名空间里而报 `NameError`——这也是为什么 `exec`/`eval` 只适合当开发工具，不能直接照搬普通代码的作用域直觉。
