---
id: amz-dag-runner-how-asked-and-three-questions
node: amazon.amz-dag-runner
type: qa
step: 1
tags: [grown]
---
## Q
DAG 执行器与依赖安装（DAG Runner）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是依赖排序：给一张依赖邻接表（每个名字对应它依赖的名字列表），返回能依次装完的顺序，有环（A 等 B、B 又等 A）就抛异常；之后还可能让你评审一段有 bug 的排序代码，或让任务并行执行。三问：(1) deps[a]=[b] 是 a 依赖 b 还是反过来——方向反了顺序全倒；(2) 有环只抛异常还是说出环——后者可直接告诉用户改哪条；(3) 多个合法顺序要哪个——要确定性就得定平局规则。
