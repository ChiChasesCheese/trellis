---
id: cc-output-formatting-decimal-shapes
node: output.formatting
type: qa
---
## Q
Three specs for the same rate: "6 decimals", "6 decimals with trailing zeros stripped", "always 2 decimals". Give each expression and what each prints for 88.0 and 0.7142857.

## A
**They are not interchangeable — read which shape is wanted.**

- Fixed: `f"{x:.6f}"` → `88.000000`, `0.714286`.
- Trimmed: `f"{x:.6f}".rstrip("0").rstrip(".")` → `88`, `0.714286` (guard the all-zeros case, which trims to the empty string).
- Money: two decimals always, produced from integer minor units, never from a float ([[cc-output-formatting-minor-units]]) → `88.00`.

Rounding inside an f-string is round-half-to-even applied to the *binary* value, so `f"{2.675:.2f}"` gives `2.67`. If the spec says half-up, round explicitly with `Decimal(...).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` before formatting, and do it once at the edge.

## Q zh
同一个 rate 的三种 spec：「6 位小数」「6 位小数并去掉尾随零」「始终 2 位小数」。给出各自的表达式，以及对 88.0 和 0.7142857 的输出。

## A zh
**它们不可互换 —— 读清楚要哪一种形态。**

- 定长：`f"{x:.6f}"` → `88.000000`、`0.714286`。
- 去尾：`f"{x:.6f}".rstrip("0").rstrip(".")` → `88`、`0.714286`（要防住全零被裁成空串的情况）。
- money：始终 2 位小数，由整数最小单位产生，绝不由 float 产生（[[cc-output-formatting-minor-units]]）→ `88.00`。

f-string 里的舍入是对*二进制*值做 round-half-to-even，所以 `f"{2.675:.2f}"` 给出 `2.67`。如果 spec 要 half-up，就在格式化前显式用 `Decimal(...).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`，并且只在边界处做一次。
