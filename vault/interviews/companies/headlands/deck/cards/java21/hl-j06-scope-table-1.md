---
id: hl-j06-scope-table-1
node: java21.j06-instanceof-pattern
type: qa
step: 5
---
## Q
绑定变量 `s` 在下面四种写法里哪里可用：(1) `if (o instanceof String s) { A } else { B }`；(2) `o instanceof String s && s.isEmpty()`；(3) `o instanceof String s || s.isEmpty()`；(4) `!(o instanceof String s) || s.isEmpty()`？

## A
| 写法 | `s` 可用的位置 | 理由 |
|---|---|---|
| (1) if / else | 只在 `A` | 进入 A 说明匹配了；进入 B 说明没匹配 |
| (2) `&&` | `&&` 右边 | 右边只在左边为真时才算 |
| (3) `\|\|` | **哪里都不行**（`cannot find symbol`） | 右边在左边为**假**时才算，此时没匹配 |
| (4) `!(...) \|\|` | `\|\|` 右边 | 左边为假 = 匹配成功 |
