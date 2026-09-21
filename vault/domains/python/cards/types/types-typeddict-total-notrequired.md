---
id: types-typeddict-total-notrequired
node: types.typeddict-literal
type: qa
source: python-docs
---
## Q
`TypedDict` 默认要求所有键都必须存在吗？怎么单独把某个键标成可以缺省？

## A
默认 `total=True`，类体里声明的每个键都是必需键。给某个键包一层 `NotRequired[...]`（如 `label: NotRequired[str]`）就能单独把它标成可缺省，而不用改变整体的 totality；反过来也可以在 `class Point2D(TypedDict, total=False)` 里把默认改成「全部可选」，再用 `Required[...]` 把个别键改回必需。
