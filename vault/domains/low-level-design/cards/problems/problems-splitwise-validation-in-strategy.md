---
id: problems-splitwise-validation-in-strategy
node: problems.marketplaces.splitwise
type: qa
step: 5
tags: [grown]
---
## Q
在分账（Splitwise）设计里，“精确金额之和必须等于总额”“百分比之和必须是 100”这类校验，应该写在记账入口 `add_expense` 里还是写在各个拆分策略里？

## A
写在各个拆分策略自己身上。校验规则是拆分算法的一部分，不是调用方的知识：一旦在入口写成 `if isinstance(split, PercentageSplit): ...` 的类型判断链，每加一种拆分方式都要回头改入口，策略可替换这件事就白做了。入口只负责它自己的职责——用户存不存在、付款人是谁。另外，和具体金额无关的不变式（百分比之和、份额必须为正）要在构造时就抛，越早失败越好；只有和总额、参与人相关的检查（精确金额之和是否等于总额、参与人是否对得上）才留到 `compute`。
