---
id: cc-model-sm-transition-table
node: model.state-machine
type: cloze
---
A payment moves `REQUIRES_ACTION -> PROCESSING -> COMPLETED`. Write the machine as {{c1::an explicit table of (state, command) -> next state}}, and make every command that is not in the table {{c2::do nothing at all — no state change, no output}} when the statement says invalid commands are silently ignored. The table is also the checklist: {{c3::each cell the statement mentions is a hidden test}}, and the empty cells are the ignore-path tests.

## zh
一笔付款按 `REQUIRES_ACTION -> PROCESSING -> COMPLETED` 流转。把这台机器写成 {{c1::一张显式的 (state, command) -> next state 表}}，并让所有不在表中的命令 {{c2::什么都不做 —— 不改状态、不输出}}，只要题面说无效命令被静默忽略。这张表同时是检查清单：{{c3::题面提到的每一格都是一个隐藏测试}}，而空着的格子就是"忽略路径"测试。
