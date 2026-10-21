---
id: amz-dag-runner-common-mistake-no-length-check
node: amazon.amz-dag-runner
type: qa
step: 9
tags: [grown]
---
## Q
在 Amazon DAG 执行器里，最常见的错误是 Kahn 排完不核对数量。给出一个会暴露它的输入和正确做法。

## A
输入 {"a": ["b"], "b": ["a"]}：没有入度为 0 的节点，循环一次不进，返回 []，调用方以为没东西要装。正确做法：循环后比较 len(out) 与节点总数，不等就抛 CycleError 并带上具体的环。这类 bug 在普通示例上不出现，只能靠评审清单发现：节点是否全登记、重复边怎么数、数量是否核对。
