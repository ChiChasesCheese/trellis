---
id: hl-j13-unused-pain
node: java21.j13-unnamed-variables
type: qa
step: 1
---
## Q
Java 要求每个声明的变量都有名字，哪些场景下变量「语法要求声明、我根本不用」？带来哪三个痛点？

## A
场景：`catch (NumberFormatException e)` 里不用 `e`；`for (String ignored : names) n++;` 只数个数；`computeIfAbsent("k", k -> 0)` 的 lambda 参数 `k`；`if (ev instanceof Fill f)` 其实只需知道「是 Fill」。

三个痛点：
1. **读者多想一步**：看到 `e` 得扫一遍 `catch` 体确认没被用；命名 `ignored` 只是人肉约定，编译器不知道。
2. **静态检查器/IDE 报「未使用变量」警告**，只能 `@SuppressWarnings` 或约定名字，噪声大。
3. **模式匹配时更明显**：record 模式 `Fill(var id, var qty, var px)` 只要 `id` 时另两个也得起名并带「未使用」警告，或放弃解构回到 `f.orderId()`。
