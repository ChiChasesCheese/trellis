---
id: amz-dag-runner-how-asked-and-three-questions
node: amazon.amz-dag-runner
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「DAG 执行器与依赖安装（DAG Runner）」是怎么问的？开场先问哪三个澄清问题？

## A
报告（Hello Interview，2026-10-01）：给依赖邻接表，返回安装顺序，有环就抛异常；另有代码评审形态：改一段算 Step Function 执行顺序的 bug 代码。三问：(1) deps[a]=[b] 是 a 依赖 b 还是反过来——方向反了顺序全倒；(2) 有环只抛异常还是说出环——后者可直接告诉用户改哪条；(3) 多个合法顺序要哪个——要确定性就得定平局规则。
