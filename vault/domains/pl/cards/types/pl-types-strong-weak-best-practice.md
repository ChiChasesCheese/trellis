---
id: pl-types-strong-weak-best-practice
node: types.strong-weak
type: qa
step: 7
---
## Q
在有隐式转换或缩窄转换的语言里，资深工程师怎样避免转换造成的数据错误？

## A
原则：把转换集中在系统边界，核心逻辑只用一种明确的类型；一旦需要缩窄，就用会报错的版本，不用会截断的版本。

具体做法：

- 缩窄转换用「检查型」API：Java 用 `Math.toIntExact`，Rust 用 `i32::try_from`，而不是 `(int)` 强制转换和 `as`。对于 30 亿的 `long`：

```java
long big = 3_000_000_000L;
int a = (int) big;              // -1294967296，静默截断
int b = Math.toIntExact(big);   // ArithmeticException: integer overflow
```

```rust
let big: i64 = 3_000_000_000;
let a = big as i32;          // -1294967296，静默截断
let b = i32::try_from(big);  // Err(TryFromIntError(PosOverflow))
```

- 实际输出就是注释中的值：强制转换得到 `-1294967296`，检查型 API 立刻失败。让失败在转换的那一行出现，而不是几个函数后变成一个奇怪的负数。
- 在 Rust 里启用 `clippy::cast_possible_truncation` 一类的 lint，让 `as` 的有损用法在评审前就被标出。
- 钱和数量不用浮点：Java 用 `BigDecimal` 或以分为单位的 `long`，Python 用 `Decimal`。
- 字符串拼接别依赖隐式转换：Java 的 `"x" + a + b` 受求值顺序影响，用 `String.format` 或模板更稳。

何时可以破例：位运算、哈希、协议编码中，截断本来就是需求（取低 8 位），这时用 `as u8` 或 `(byte)` 并加注释说明意图，而不是用检查型 API。
