---
id: hl-j08-allowed-places
node: java21.j08-var
type: qa
step: 4
---
## Q
`var` 可以用在哪五个位置？lambda 形参用 `var` 有什么条件和目的？

## A
1. 有初始化器的局部变量：`var list = new ArrayList<Fill>();`
2. 传统 `for` 的循环变量：`for (var i = 0; i < n; i++)`
3. 增强 `for` 的循环变量：`for (var e : map.entrySet())`
4. `try-with-resources`：`try (var in = new BufferedReader(...)) { ... }`
5. lambda 的形参（Java 11）：`(var x, var y) -> x + y`

lambda 形参的条件：所有形参**要么全 `var`，要么全不 `var`**；目的是能给形参加注解，如 `(@NonNull var x, ...)`。
