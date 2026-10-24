---
id: pl-types-numbers-best-practice
node: types.numbers
type: qa
step: 5
---
## Q
处理金额、计数、时间戳、哈希这类数值时，资深工程师在 Go、Java、Rust、Python 里各怎么做才不会被溢出和精度坑到？

## A
按场景选类型和运算，而不是用默认的 `int`/`float`。

- 金额：不用二进制浮点。用整数存最小货币单位（分），或者十进制类型：Java 的 `BigDecimal`（用字符串构造，`new BigDecimal(0.1)` 会把误差带进来），Python 的 `Decimal`。
- 浮点比较：不用 `==`，用容差（`abs(a - b) < eps`）；累加大量浮点数时留意误差累积。
- 业务计数和大小：在系统边界做溢出检查，内部用够宽的类型。Java 用 `long` 存 ID 和时间戳，需要时用 `Math.addExact`、`multiplyExact`；Rust 对来自外部的数据用 `checked_*`；Go 在计算长度、偏移量时手动检查上界。
- 哈希、校验和、随机数发生器：有意回绕，Rust 里写 `wrapping_*`，让读者知道这是故意的。
- Rust 的关键代码：在 release 配置里打开 `overflow-checks = true`，不要只靠 debug 构建的 panic 发现问题。
- 取中点：Java 经典 bug，`(lo + hi) / 2` 在大数组上溢出，写成 `lo + (hi - lo) / 2` 或 `(lo + hi) >>> 1`。

一个对照例子，同一笔钱用浮点和十进制相加：

```python
0.1 + 0.2 == 0.3                                   # False，实际值 0.30000000000000004
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")  # True
```

何时可以破例：科学计算和图形学需要速度，浮点误差在可接受范围内，用 `float64` 是正确选择；关键是知道误差的量级并有意接受。
