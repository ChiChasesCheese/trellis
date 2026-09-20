---
id: quality-fitness-function-definition
node: quality.fitness-functions
type: qa
step: 1
---
## Q
"适应度函数（fitness function）"和一般的单元测试有什么本质区别？

## A
一般的单元测试，被测对象是业务逻辑——给定输入，断言产出的行为符合预期。适应度函数的被测对象是**代码库本身**的结构性质——它读代码库的源文件、import 图、目录结构，断言的是"架构规则有没有被遵守",而不是"某个函数算得对不对"。比如"domain 包里的模块永远不能 import infrastructure 包"，这条规则不属于任何一个函数,只有把整个代码库当作输入才能检查。

这类测试和普通测试跑在同一套 `pytest` 流水线里,失败时会像任何测试失败一样挡住合并,区别只在于它探测的是设计意图有没有随时间被侵蚀——普通测试防止行为退化,适应度函数防止架构退化。
