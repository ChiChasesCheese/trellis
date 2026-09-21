---
id: dataclass-eq-field-by-field
node: classes.dataclasses
type: qa
source: python-docs
---
## Q
`@dataclass(eq=True)`（默认值）生成的 `__eq__()` 具体怎么比较两个实例？对类型不同的两个实例会怎样？

## A
按字段定义顺序逐个比较（3.13 起是 `self.a == other.a and self.b == other.b ...` 这种逐字段比较，3.12 及更早是打包成元组再比较），且要求两个实例是完全相同的类型，类型不同直接不相等。逐字段比较比打包元组更快，但在字段用 `float('nan')` 这类「按恒等相等但按值不等」的对象时，结果可能与旧版本不同。
