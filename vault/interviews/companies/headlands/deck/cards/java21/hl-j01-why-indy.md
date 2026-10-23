---
id: hl-j01-why-indy
node: java21.j01-record
type: qa
step: 16
---
## Q
`record` 的 `equals` / `hashCode` / `toString` 为什么用 `invokedynamic` 引导方法生成，而不是把展开的代码写进 class 文件？有哪三个好处？

## A
1. **class 文件小**：不管多少组件，`equals` 都只占一条指令。
2. **以后可升级**：JDK 想换更快的生成方式，只改引导方法，你的代码不用重新编译。
3. **复用同一套机制**：模式匹配 `switch`（`switch` pattern matching）也用同样的 `invokedynamic` 思路。

对比：Java 8 手写 30 行 `equals`，每个组件都占字节码；record 只留一条指向引导方法的指令。
