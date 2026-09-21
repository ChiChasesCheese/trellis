---
id: types-typeddict-runtime-is-plain-dict
node: types.typeddict-literal
type: qa
source: python-docs
---
## Q
`class Point2D(TypedDict): x: int; y: int` 定义之后，运行时创建出来的 `Point2D` 实例本质上是什么？漏掉一个必需键会立刻报错吗？

## A
运行时“`TypedDict` 实例”就是普通的 `dict`，`TypedDict` 不生成新的运行时类型，也不做任何键存在性或值类型的校验。比如 `b: Point2D = {'z': 3, 'label': 'bad'}` 只会被静态检查器判为错误（缺 x/y、多了 z），代码本身照常运行、`b` 就是个普通字典，直到真正读取缺失的键时才会在运行时抛 `KeyError`。
