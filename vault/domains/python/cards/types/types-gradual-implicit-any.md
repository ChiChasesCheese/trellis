---
id: types-gradual-implicit-any
node: types.gradual-typing
type: qa
source: python-docs
---
## Q
一个没写参数和返回值类型的函数，比如 `def legacy_parser(text): ...`，静态检查器会怎么处理它的签名？

## A
检查器会把它当作参数和返回值都是 `Any`，等价于显式写成 `def legacy_parser(text: Any) -> Any`。这让未标注的历史代码能和已标注的新代码混用而不报错，是渐进类型化（gradual typing）能逐步引入类型提示、不用一次性给全部代码打标注的机制基础。
