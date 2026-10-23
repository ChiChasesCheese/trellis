---
id: hl-j03-java8-pain
node: java21.j03-pattern-switch
type: qa
step: 1
---
## Q
Java 8 的 `switch` 与 `instanceof` 链在按"类型"分派时有哪五个痛点？模式匹配 `switch`（Java 21 正式，17–20 为预览）一次解决哪些？

## A
痛点：
1. **判断 + 强转是两步**，类型写两遍，改一个忘另一个就是 `ClassCastException`。
2. `if-else` 链不知道"一共几种"，漏一种编译器不报，末尾的 `throw` 只在运行时暴露。
3. 老 `switch` 遇 `null` 必抛 `NullPointerException`。
4. 带 `:` 的老写法会 **fall-through**（忘 `break` 就执行下一分支）。
5. 想对某类型再加条件，只能在分支里嵌 `if`，结构乱。

模式匹配 `switch`：**直接写类型、自动转型、可处理 null、可加条件、漏了就编译报错**。
