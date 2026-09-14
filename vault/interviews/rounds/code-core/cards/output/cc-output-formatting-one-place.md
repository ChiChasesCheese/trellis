---
id: cc-output-formatting-one-place
node: output.formatting
type: qa
---
## Q
Amounts print as `$12.34` in one part, `1234` in another and `12.34` in a third. How do you stop that from becoming a bug farm?

## A
**One formatter per output shape, called only at the print site.** State stays in its canonical type — integer minor units, integer minutes, an exact `Decimal` — from parse to print, and the formatter is the only code that knows about symbols, decimals and separators.

- A value stored as a formatted string will be re-parsed, compared or summed by a later part, and it will drift.
- Name the units in the function: `fmt_cents`, `fmt_minutes`. A mismatch then shows up at the call site instead of in the diff.
- When a part changes the shape, add a formatter rather than branching on the part number inside the old one more than once.
- The rounding decision belongs in the formatter too, so it happens exactly once, at the edge — never per row on the way in.

## Q zh
金额在某个 part 打印成 `$12.34`，在另一个 part 是 `1234`，第三个又是 `12.34`。怎么避免它变成 bug 的温床？

## A zh
**每种输出形态一个格式化函数，只在打印处调用。** 状态从解析到打印一直保持规范类型 —— 整数最小单位、整数分钟、精确的 `Decimal` —— 而格式化函数是唯一知道符号、小数位和分隔符的代码。

- 以格式化字符串形式存下的值，会被后面的 part 重新解析、比较或求和，并且一定会漂移。
- 把单位写进函数名：`fmt_cents`、`fmt_minutes`。这样不匹配会在调用处暴露，而不是在 diff 里。
- 当某个 part 改变了形态，就新增一个格式化函数，而不是在旧函数里反复按 part 号分支。
- 舍入决定也属于格式化函数，这样它恰好在边界处发生一次 —— 绝不在读入时逐行做。
