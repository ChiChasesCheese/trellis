# pc10 Distributed Tree Count — report

## Summary
Snowflake 电面池"Distributed Tree Counting State Machine"：只靠一个全局 FIFO 信道的消息，模拟根发起、叶子应答、内部节点汇总上报的计数协议，并逐条记录投递日志。2-part：Part 1 可靠信道（按来源样例逐行复现 9 行轨迹）→ Part 2 丢消息 + 重试一次 + 放弃后按缺失子树给出 `PARTIAL` 结果 **(reconstructed)**。

## Sources & confidence
MED——fastprep（Phone Screen，2026-07，含样例）· prachub "Distributed Tree Node Count with Two Messages" · 1p3a 面经索引标题；三者题面结构一致。`REPORT` 的逐字格式来源未给出，本题定为 `REPORT <v>`。Part 2 为重建。

## Approach by part
1. 由 `parent` 建孩子表（天然按 id 升序），校验恰好一个根、无越界、无环。单节点直接 `ROOT_COUNT:1`。全局 `deque` 模拟信道；每个节点维护 `pending`（未报告孩子数）与 `total`（1 + 已收报告）。`GET_COUNT` 到叶子就回 `REPORT 1`，到内部节点就向孩子扇出；`REPORT v` 到达时 `pending -= 1`，为 0 时向上报告或在根处结束。
2. 发送时分配全局发送号。投递时若发送号在 `drops`：首次丢失记 `LOST` 并重发（新发送号入队尾）；重发也丢失记 `GIVEUP`，由这条边上的父节点记该孩子贡献 0 并视为已报告，同时置 `partial`。

## Pitfalls hidden tests target
- 日志逐字：`from->to:GET_COUNT`、`from->to:REPORT v`、`ROOT_COUNT:n`
- 孩子必须按 id 升序发送；根不在下标 0
- 单节点、两节点、链状树
- 非法输入 6 种（空、无根、双根、越界、自环、环）
- 无丢失时日志行数恰为 `2(n-1)+1`（每边一去一回）
- Part 2：丢的是 `REPORT` 时同样由父节点计 0；`PARTIAL` 当且仅当出现 `GIVEUP`；有 `GIVEUP` 时计数在 `[1, n)`
- 10^5 节点 2 秒内（`pending` 计数，不重复扫描孩子）

## Complexity & measured cost
O(n) 消息、O(n) 时间与空间。编排者验证：3000 棵随机树（节点编号随机打乱）上无丢失计数恒为 n 且日志行数为 `2(n-1)+1`；随机丢包下总能终止，且 `PARTIAL` 与 `GIVEUP` 一一对应，0 失败。perf：10^5 节点端到端 < 2 s。

## Test inventory
22 tests — part1 14（含 6 参数化非法输入、1 perf、1 io/fmt）· part2 8（含 1 io）；edge 11 · fmt 1 · perf 1 · io 2。

## Skills exercised
S07 消息传递模拟 / 异步聚合 · S09 协议契约先行 · S10 失败语义与部分结果
