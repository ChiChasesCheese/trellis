---
id: hl-sd01-fu-public-api
node: system-design.sd01-unused-code
type: qa
step: 35
---
## Q
追问：公共 API / 对外发布的库里零引用的符号怎么办？最便宜的删除是什么？

## A
L2 开放世界：快照里零引用不等于没人用。要查：制品仓库下载 / 依赖扫描（其他仓库、其他团队的 `pom.xml` / `build.gradle`）、版本发布说明；先 `@Deprecated(forRemoval=true)` 并发出弃用通知，等一个或多个发布周期。

内部库**收紧可见性**（`public` → 包私有）本身就是对 L2 → L0 的转化，值得单列为一种低风险的「瘦身」。

可以说：「最便宜的删除是收窄可见性，它把 L2 变成编译器可证明的 L0。」
