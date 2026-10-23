---
id: hl-j08-readability-principle
node: java21.j08-var
type: qa
step: 19
---
## Q
OpenJDK 风格指南关于何时用 `var` 的核心原则是什么？适合用的四种情形是什么？

## A
核心原则：**"读代码的人能不能只看这一行就知道类型？"** 能就用，不能就写出来。

适合用：
1. 右边**明确出现类型名**：`var list = new ArrayList<Fill>();`、`var in = new BufferedReader(...)`、`var m = pattern.matcher(s)`；
2. 类型很长且没信息量：嵌套泛型、`Map.Entry<K, List<V>>`；
3. `for` / `try-with-resources` 的变量；
4. 变量名本身说明用途：`var matcher`、`var results`。
