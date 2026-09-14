---
id: cc-output-formatting-fixed-width
node: output.formatting
type: qa
---
## Q
Card ranges are held as `bin * 10**10 + offset` and must print as 16 digits. An offset arrived as `0000000000`. What must the code do at each end?

## A
**Parse as an integer, print with an explicit width.** `int("0000000000")` is 0 — the zeros are not data, the width is.

- Output with a format spec: `f"{n:016d}"` (or `str(n).zfill(16)`). Never rebuild the line by concatenating parts — a short offset silently produces a 15-character line and one failed test group.
- Stay in `int`. `4242429999999999` is above 2^53, where a `float` can no longer distinguish adjacent values, so any float step corrupts an endpoint.
- If the field can be negative, `:016d` counts the sign inside the width; pad the magnitude yourself ([[cc-output-formatting-minor-units]]).
- The round trip is the test: parse the sample, print it back, byte-compare.

## Q zh
卡号区间以 `bin * 10**10 + offset` 保存，必须打印成 16 位数字。某个 offset 传入的是 `0000000000`。代码在两端各要做什么？

## A zh
**按整数解析，按显式宽度打印。** `int("0000000000")` 就是 0 —— 那些零不是数据，宽度才是。

- 输出用格式说明符：`f"{n:016d}"`（或 `str(n).zfill(16)`）。绝不要靠拼接分段重建这一行 —— 短一位的 offset 会悄悄产生 15 个字符的一行，直接挂掉一组测试。
- 全程用 `int`。`4242429999999999` 超过 2^53，`float` 已经无法区分相邻值，任何浮点运算都会破坏端点。
- 如果字段可能为负，`:016d` 会把符号算进宽度；请自己给绝对值补位（[[cc-output-formatting-minor-units]]）。
- 检验方法就是往返：解析样例、原样打印回去、逐字节比对。
