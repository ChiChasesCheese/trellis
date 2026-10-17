---
id: amz-linux-find-common-mistake-all-combinations
node: amazon.amz-linux-find
type: qa
step: 9
tags: [grown]
---
## Q
在 Linux find 文件搜索设计里，候选人最常见的结构性错误是什么？给一个会暴露它的追问。

## A
为每种条件组合写一个类（`ExtAndSize`、`ExtOrName` ……），或写一个参数越来越多的 `find(...)`。

暴露它的追问：「再加 NOT，再加 OR 里套 AND」。组合类的数量随条件数指数增长；参数列表则根本表达不了 `(py OR md) AND NOT old*`。

修复：条件是叶子类，组合只有 `And` / `Or` / `Not` 三个，`(Extension("py") | Extension("md")) & ~NameGlob("old*")` 一行写完。
