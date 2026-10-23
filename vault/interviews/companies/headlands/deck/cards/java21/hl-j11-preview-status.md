---
id: hl-j11-preview-status
node: java21.j11-structured-concurrency
type: qa
step: 4
---
## Q
`StructuredTaskScope` 在 Java 21 是什么状态？怎么编译运行？各 JDK 版本的演进是什么？

## A
Java 21 里它是**预览（Preview）API**：编译 `javac --release 21 --enable-preview`，运行 `java --enable-preview`。预览意味着后续版本可不兼容地改。

演进：JDK 19、20 孵化 → **21 预览** → 22–24 继续预览 → **25 API 大改** → 26 第六次预览。

编译器只做一件事：看到预览 API 要求 `--enable-preview`，并在 class 文件打上「依赖预览」标记，所以用预览编出的类必须带 `--enable-preview` 运行，且只能在同一大版本的 JVM 上运行。
