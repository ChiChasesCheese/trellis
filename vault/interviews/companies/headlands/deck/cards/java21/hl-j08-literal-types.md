---
id: hl-j08-literal-types
node: java21.j08-var
type: qa
step: 10
---
## Q
`var a = 18_950;`、`var b = 18_950L;`、`var c = 1.5;`、`var d = 'x';` 各是什么类型？

## A
- `18_950` → `int`
- `18_950L` → `long`
- `1.5` → `double`
- `'x'` → `char`

（用 `getClass()` 看到的是装箱类型 `Integer Long Double Character`。）

这是 `var` 最容易出事的地方：数字字面量悄悄是 `int`，类型不再写在左边。
