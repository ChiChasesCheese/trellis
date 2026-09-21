---
id: builtins-namespace-lookup-via-dunder
node: runtime.namespaces-execution
type: qa
source: python-docs
---
## Q
`print` 这种内置名字，Python 是怎么在一个模块里找到它的？`__builtins__` 能不能自己去改？

## A
名字解析先查当前作用域的局部/全局命名空间，都找不到才查内置命名空间——这个内置命名空间实际是通过在当前模块的全局命名空间里查找 `__builtins__` 这个名字拿到的（`__main__` 模块里它就是 `builtins` 模块本身，其它模块里是 `builtins` 模块的字典）。`__builtins__` 被官方文档明确标注为「实现细节」，不建议直接读写；想覆盖内置名字应该 `import builtins` 之后修改 `builtins` 模块的属性。
