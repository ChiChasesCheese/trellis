---
nodes: [types.numbers, types.type-conversions, types.strong-weak]
tags: [drill]
---
# 练习：计费计数器溢出时，四门语言各发生什么

计费服务用 32 位整数累计用量，某个租户的计数已经到了 `2147483647`，下一条事件再加 1。四个团队分别用 Go、Java、Python、Rust 实现了同一个服务；其中一个团队的告警只监控「错误」和「panic」。你要预测每门语言的行为，判断哪些会被告警发现，再为金额和计数设计各自的安全写法。

**要你给出的**
- `2147483647 + 1`（32 位整数）在 Go（`int32`）、Java（`int`）、Python、Rust（debug 构建与 `-O` release 构建）里的结果。
- 缩窄转换的结果：Java `(int) 3_000_000_000L` 与 `(byte) 200`；Go 里 `x := 300` 后的 `int8(x)`、`uint8(x)`；Rust 里 `300i64 as u8` 与 `u8::try_from(300i64)`。
- 浮点三连：`0.1 + 0.2 == 0.3` 在 Go 里写成常量表达式与写成两个变量相加时，结果一样吗？Java、Python、Rust 呢？
- 哪些语言的默认行为会让「只监控错误」的告警失灵，以及你的修复方案。

**评分要点**
- 加 1 溢出：Go 与 Java 静默回绕成 `-2147483648`，没有任何错误；Python 的整数没有上限，得到 `2147483648`；Rust 的 debug 构建 panic（`attempt to add with overflow`），而 `-O` 的 release 构建同样静默回绕成 `-2147483648` ([[pl-types-numbers-table]], [[pl-types-numbers-found-rust-overflow-modes]])。
- 生产上跑的是 release 构建，所以「Rust 会 panic」的印象在线上不成立：测试里发现不了，线上静默出错。要么在 release 配置里打开 `overflow-checks`，要么对关键计算显式使用 `checked_add`（返回 `None`），`wrapping_add` 回绕，`saturating_add` 得到 `2147483647` ([[pl-types-numbers-pitfall-rust-profile]], [[pl-types-numbers-unique-rust-explicit]])。
- 因此只监控错误的告警对 Go、Java 和 Rust release 都无效：溢出不产生任何信号。修复是把计数改成 64 位，并在边界处主动检查，Java 用 `Math.addExact`（抛出 `ArithmeticException: integer overflow`），Go 自己写检查 ([[pl-types-numbers-best-practice]], [[pl-types-numbers-found-integer-families]])。
- 缩窄转换：Java `(int) 3_000_000_000L` 是 `-1294967296`，`(byte) 200` 是 `-56`；Go 的 `int8(300)` 与 `uint8(300)` 都是 `44`；Rust 的 `300i64 as u8` 是 `44`，而 `u8::try_from(300i64)` 返回 `Err(TryFromIntError(PosOverflow))`。前三者保留低位、不报错，Rust 把「会丢信息」的转换放到可失败的 `TryFrom` 上 ([[pl-types-type-conversions-mechanism]], [[pl-types-type-conversions-pitfall-silent-narrowing]], [[pl-types-type-conversions-unique-rust-tiers]])。
- 浮点：Java、Python、Rust 的 `0.1 + 0.2 == 0.3` 都是 `false`（和是 `0.30000000000000004`）；Go 里写成常量表达式 `0.1+0.2 == 0.3` 却是 `true`，因为常量在编译期用任意精度计算，写成两个变量才是 `false` ([[pl-types-numbers-mechanism]], [[pl-types-numbers-principle]])。
- 金额不用二进制浮点：整数「分」放进 64 位，或者用 `BigDecimal`、`Decimal` 这类十进制类型，并规定舍入模式 ([[pl-types-numbers-found-decimal-types]])。
- 转换规则：数值转换一律走显式且可失败的路径（Rust 的 `TryFrom`；Java 用 `Math.toIntExact`；Go 先比较范围再转换），不要依赖低位截断 ([[pl-types-type-conversions-best-practice]], [[pl-types-strong-weak-best-practice]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
