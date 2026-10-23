---
id: hl-javaq-c-q09-traps
node: java-questions.c-languages
type: qa
step: 11
---
## Q
Java 里行为"确定"但会坑人的整数 / 数值陷阱有哪些？给出具体结果。

## A
- **溢出回绕**：`Integer.MAX_VALUE + 1 = -2147483648`；想要检查就用 `Math.addExact`，会抛 `integer overflow`。
- **窄化转换**：`(int) 3_000_000_000L = -1294967296`，`(byte) 200 = -56`。
- **移位次数取模**：`1 << 33 = 2`（移位数只取低 5 位），`1L << 33 = 8589934592`。
- `0.1 + 0.2 != 0.3`；`-7 % 2 == -1`（余数符号随被除数）。
- `Integer` 装箱缓存导致 `==` 行为怪异；`char` 是**无符号 16 位**。
- 金融代码：金额用 `long`（最小单位）或 `BigDecimal` + 明确舍入；累加用 `Math.addExact` / `multiplyExact` 防止悄悄回绕。
