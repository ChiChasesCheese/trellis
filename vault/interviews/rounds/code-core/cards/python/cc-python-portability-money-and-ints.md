---
id: cc-python-portability-money-and-ints
node: python.portability
type: cloze
---
Python's `int` is arbitrary precision, so `10**18 * 10` is exact; Java's `long` and Go's `int64` overflow silently past about {{c1::9.2}}·10^18, and JavaScript's `number` loses integer exactness past 2^{{c2::53}} — reach for `BigDecimal`, `int64` minor units, or `bigint`. A binary float must never hold money in any of the four.

## zh
Python 的 `int` 是任意精度的，所以 `10**18 * 10` 是精确的；Java 的 `long` 和 Go 的 `int64` 超过约 {{c1::9.2}}·10^18 就静默溢出，而 JavaScript 的 `number` 超过 2^{{c2::53}} 就失去整数精确性 —— 该用 `BigDecimal`、`int64` 最小单位、或 `bigint`。这四门语言里都绝不能用二进制浮点装钱。
