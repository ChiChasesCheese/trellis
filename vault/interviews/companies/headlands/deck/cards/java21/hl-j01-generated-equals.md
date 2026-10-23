---
id: hl-j01-generated-equals
node: java21.j01-record
type: qa
step: 17
---
## Q
`record` 自动生成的 `equals` 怎么逐步比较？不同类型的组件分别怎么比？`hashCode` 的规范要求是什么？

## A
`equals`：先 `instanceof` 判断是同一 record 类型，再**逐组件**比较：
- `int` / `long` 等基本类型：直接比；
- `float` / `double`：用 `Float.compare` / `Double.compare`；
- 引用类型：用 `Objects.equals`。

`hashCode`：组合各组件的哈希。规范只要求"**相同内容 → 相同哈希**"，不规定具体公式。

`equals` 与 `hashCode` 总是同时按全部组件生成，所以放进 `HashMap` 不会像忘了重写时那样查不到。
