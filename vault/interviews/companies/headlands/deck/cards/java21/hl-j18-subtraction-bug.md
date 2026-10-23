---
id: hl-j18-subtraction-bug
node: java21.j18-comparators-interfaces
type: qa
step: 3
---
## Q
为什么比较器里写 `return a - b;` 是错的？给一个反例，并说明 `Double.compare` 的优势。

## A
减法可能**溢出**：`Integer.MAX_VALUE - (-1)` 得 `-2147483648`（负数），使得「MAX < -1」，违反传递性/反对称；而 `Integer.compare(a, b)` 给出正确的 `1`。

永远用 `Integer.compare`、`Long.compare`、`Double.compare`。`Double.compare` 还正确处理 `NaN` 与 `-0.0`，用 `<` / `>` 不处理。
