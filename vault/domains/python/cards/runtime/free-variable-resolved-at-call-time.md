---
id: free-variable-resolved-at-call-time
node: runtime.namespaces-execution
type: qa
source: python-docs
---
## Q
一个函数体里引用的自由变量（free variable），是在函数定义时就确定了指向哪个值，还是在函数被调用、真正执行到那一行时才去查？

## A
是在执行到那一行时才按当时的作用域状态去查找，不是在函数定义时就绑死。比如先 `i = 10`，再定义一个引用了 `i` 的函数 `f`，然后把 `i` 改成 42，最后才调用 `f()`——`f` 打印的是 42 而不是定义时的 10。这也是为什么闭包捕获的是变量本身、而不是定义那一刻的值快照。
