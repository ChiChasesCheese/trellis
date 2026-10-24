---
id: pl-types-algebraic-data-types-best-practice
node: types.algebraic-data-types
type: qa
step: 9
---
## Q
建模「几种状态之一」的数据时，资深工程师用什么规则？在 Rust、Java、Python、Go 里分别怎样落地？

## A
核心规则：用和类型表达状态，让非法组合无法构造；用不带通配分支的穷尽匹配处理，让新增变体时编译器带你找到所有要改的地方。

- 避免「布尔标志加一堆可空字段」。例如订单 `status`、`paidAt`、`cancelReason` 并存，会出现 `status=PAID` 但 `paidAt` 为空的组合。拆成 `Pending`、`Paid { at }`、`Cancelled { reason }` 三个变体，每个只带自己需要的数据。
- Rust：自己定义的 `enum` 不写 `_ =>` 通配分支，因为通配会让新增变体被静默吞掉；请求、状态机、命令都用 `enum`。
- Java：`sealed interface` 加 `record`，`switch` 表达式不写 `default`，新增实现类时编译器报错。
- Python：用 `dataclass` 加联合类型，`match` 的最后一个分支调用 `assert_never`，让 `mypy` 在漏掉变体时报错：

```python
case _ as unreachable: assert_never(unreachable)
# mypy: Argument 1 to "assert_never" has incompatible type "Tri"; expected "Never"
```

- Go：把接口定义为只有未导出方法的「密封接口」限制实现者，配合 `exhaustive` linter；简单场景直接用结构体加枚举常量，并写单元测试覆盖每个值。

何时可以破例：变体集合本来就应该开放（插件系统、用户可扩展的处理器），就用接口，不用封闭的 `enum`；这时用测试和注册表来保证完整，而不是穷尽检查。
