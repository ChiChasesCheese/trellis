---
id: oop-interface-width-by-client
node: oop.interfaces
type: qa
---
## Q
In a 90-minute design, how do you decide where to split an interface — and what makes a split *too* fine?

## A
Split by **client**, not by method count. If every caller of a 4-method interface uses all 4, it is cohesive and splitting it just multiplies files. Split when one client uses a strict subset, e.g. the pricing engine only ever `read`s the catalog while the admin flow `write`s it → `CatalogReader` + `CatalogWriter`, one class implementing both.

- **Too fine**: one-method interfaces per client of the *same* role, so a single implementation is declared `implements A, B, C, D` and every wiring site names four types.
- Signal that you split correctly: some client's constructor got **narrower**, and its test fake got shorter.

The purpose is shrinking what a client can depend on, not shrinking the interface.

## Q zh
在 90 分钟的设计里，你依据什么决定在哪里拆接口——又是什么让一次拆分**过细**？

## A zh
按**调用方**拆，不按方法数量拆。如果一个 4 方法接口的每个调用方都用满这 4 个，它就是内聚的，拆开只是徒增文件。当某个调用方只用到严格子集时才拆，比如定价引擎永远只 `read` 目录、而管理流程要 `write` → 拆成 `CatalogReader` + `CatalogWriter`，由同一个类实现两者。

- **过细**：为*同一个角色*的每个调用方都建单方法接口，于是一个实现被写成 `implements A, B, C, D`，每个装配点都要写出四个类型名。
- 拆对了的信号：某个调用方的构造函数**变窄了**，它的测试 fake 也变短了。

目的是缩小一个调用方所能依赖的东西，而不是缩小接口本身。
