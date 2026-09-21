---
id: types-basics-pep585-builtin-generics
node: types.basics
type: qa
source: python-docs
---
## Q
Python 3.12 写类型注解时该用 `list[int]` 还是 `typing.List[int]`？两者为什么等价？

## A
优先用内置的 `list[int]`。自 Python 3.9 起（PEP 585），`list`、`dict`、`set`、`tuple`、`type` 等内置容器原生支持 `[]` 下标，可直接当泛型（generic）用；`typing.List` 等只是为兼容旧版本保留的已弃用别名（deprecated alias），官方文档建议新代码不再使用，只是解释器目前还没有为它发出弃用警告。
