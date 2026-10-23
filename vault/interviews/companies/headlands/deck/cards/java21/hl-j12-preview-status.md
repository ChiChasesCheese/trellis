---
id: hl-j12-preview-status
node: java21.j12-scoped-values
type: qa
step: 5
---
## Q
`ScopedValue` 在 Java 21 是什么状态，历史和转正版本是什么？怎么编译运行？

## A
Java 21 里是**预览（Preview）API**：编译 `javac --release 21 --enable-preview`，运行 `java --enable-preview`。

历史：JDK 20 孵化（incubator）→ **21 第一次预览** → 22–24 继续预览 → **JDK 25 转正**，是预览特性里最早毕业的。JDK 21 写法与 25 最终版有出入。
