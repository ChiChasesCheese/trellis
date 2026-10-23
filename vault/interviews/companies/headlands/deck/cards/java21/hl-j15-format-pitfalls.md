---
id: hl-j15-format-pitfalls
node: java21.j15-math-string-utils
type: qa
step: 20
---
## Q
`String.format` / `formatted` 有哪些坑？`repeat` 的参数有什么限制？

## A
- **默认用当前 Locale**：德国 Locale 下 `%.2f` 输出 `189,57`。要稳定输出用 `String.format(Locale.ROOT, ...)`，`formatted` 没有带 Locale 的版本。
- **钱不要用 `double`**：存储与计算用 `long` 最小单位或 `BigDecimal`。
- `%d` 不接受 `double`，抛 `IllegalFormatConversionException`。
- `"x".repeat(-1)`、`sb.repeat('0', -1)` 抛 `IllegalArgumentException`；补零宽度算出负数（已比目标宽）会炸，先 `Math.max(0, ...)`。
