---
id: comprehension-in-class-body-cannot-see-class-scope
node: runtime.namespaces-execution
type: qa
source: python-docs
---
## Q
为什么在类体里写 `b = list(a + i for i in range(10))`（`a` 是类体里刚定义的属性）会报 `NameError`，但把同样的引用换成嵌套类定义就不会？

## A
推导式/生成器表达式自己是一个独立的作用域，它按普通函数作用域规则向外层查找——而类体命名空间刻意不参与这条普通作用域链查找（为了避免类体里的名字意外泄漏进方法），所以推导式内部看不到类体里定义的 `a`，只能看到模块/内置作用域，从而报错。嵌套类定义不同：它是在类体里直接执行的语句，执行发生在类体命名空间仍然存在、还没打包成 `__dict__` 的那一刻，所以能直接引用类体里定义的名字。
