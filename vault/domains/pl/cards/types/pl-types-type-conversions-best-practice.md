---
id: pl-types-type-conversions-best-practice
node: types.type-conversions
type: qa
step: 8
---
## Q
写代码时，资深工程师怎样处理类型转换，才能让转换失败不变成线上问题？

## A
原则：把转换放在系统边界，转换时就校验，转换后的内部代码只处理已经确定的类型。

- 外部输入一律解析并校验：字符串转数字用能报告失败的 API（Java 的 `parseInt` 要捕获异常，Go 的 `strconv` 检查 `err`，Rust 的 `parse` 处理 `Result`，Python 的 `int()` 包在 `try/except ValueError`），然后检查范围，不要假设合法。
- 缩窄转换用会报错的版本：Rust 用 `try_from`，Java 用 `Math.toIntExact`；Go 手写范围检查再转换。只在位操作、哈希、协议编码里有意使用截断，并写明意图。
- 向下转型前先判断类型：
  - Java 16 起用模式匹配 `if (o instanceof String s)`，判断和转型一步完成，不会遗漏检查。
  - Go 一律用逗号 ok 形式 `v, ok := x.(T)`，只有在你能证明类型正确时才用会 panic 的形式。
  - Python 用 `isinstance`，或者干脆依赖鸭子类型不转型。
- 尽量避免需要向下转型的设计：频繁向下转型通常说明抽象有问题，可以用泛型、接口方法或封闭的和类型代替。
- Rust 中给 `as` 加 lint：启用 `clippy::cast_possible_truncation`、`cast_sign_loss`，让有损转换在评审前就被标出。

何时可以破例：热路径上已经证明范围的转换，或底层位操作，可以用 `as`、强制转换，但把这类转换集中在少数几个封装好的函数里，并加测试覆盖边界值（0、最大值、最大值加一、负数）。
