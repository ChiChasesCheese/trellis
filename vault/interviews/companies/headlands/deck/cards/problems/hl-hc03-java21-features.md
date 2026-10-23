---
id: hl-hc03-java21-features
node: problems.hc03-recursive-sum
type: qa
step: 19
---
## Q
递归求和实现用到哪些 Java 21 特性？record、sealed、模式匹配 switch、switch 表达式、`_` 各自的好处？

## A
- **record**：`Ok`、`Overflow`、`Done`、`More`、`Wide` 值语义，`equals` 白送，测试直接 `assertEquals(new Ok(55), …)`，包括比较 `Overflow` 里的 `BigInteger`。老写法一个 `Ok` 类约 20 行。不适合需要可变状态或继承时。
- **sealed**：`SumResult permits Ok, Overflow`、`Trampoline permits Done, More`，新增变体时所有 `switch` 编译报错；取代返回 `-1` / 抛异常 / `Optional` 的约定。
- **模式匹配 switch + record 解构**：`case Ok(var v) ->`，一步判断类型 + 取字段，编译器检查穷尽；别用 `default` 偷懒，否则编译器不再提醒漏了新变体。
- **switch 表达式**：`return switch (this) { case INT -> …; case LONG -> …; };` 无 `break` / fallthrough，枚举常量必须覆盖。
- **未命名变量 `_`**（预览）：`catch (StackOverflowError _)`。
- **虚拟线程 + `StructuredTaskScope`**（预览，需 `--enable-preview`）。
- **Stream / 数学工具**：`Stream.toList()` 不可变；`Math.ceilDiv` 代替有二次溢出风险的 `(a + b - 1) / b`；`Long.compareUnsigned`。
- `var` 只在类型显然时用。
