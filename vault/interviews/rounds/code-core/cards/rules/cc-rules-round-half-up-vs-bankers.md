---
id: cc-rules-round-half-up-vs-bankers
node: rules.rounding
type: cloze
---
Python's built-in `round` is **banker's** rounding: `round(0.5)` is {{c1::0}} and `round(2.5)` is {{c2::2}}, because halves go to the nearest even. A fee rule that says "rounded to the nearest cent" almost always means half-up, where 10.5 becomes {{c3::11}}. Use `Decimal(...).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` or integer arithmetic, and never leave the mode to a default.

## zh
Python 内置的 `round` 是**银行家舍入**：`round(0.5)` 是 {{c1::0}}，`round(2.5)` 是 {{c2::2}}，因为一半会进到最近的偶数。而写着「四舍五入到分」的手续费规则几乎总是指 half-up，此时 10.5 变成 {{c3::11}}。请用 `Decimal(...).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` 或整数运算，绝不把模式交给默认值。
