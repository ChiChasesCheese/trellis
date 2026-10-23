---
id: hl-j01-float-nan
node: java21.j01-record
type: qa
step: 25
---
## Q
`record` 含 `float` / `double` 组件时，`equals` 对 `NaN` 和 `-0.0` 的行为有什么需要注意？金额该不该用 `double`？

## A
生成的 `equals` 对 `float` / `double` 用 `Float.compare` / `Double.compare`，所以：
- `NaN` 与 `NaN` 视为相等；
- `0.0` 与 `-0.0` 视为不等。

这对"按内容比较"合理，但容易让人意外。**金额别用 `double`**，用 `long` 最小单位。
