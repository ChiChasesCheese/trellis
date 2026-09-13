# od09 Queue -> Service — report

## Summary
从一个"类 Python deque"的玩具队列出发，逐步逼近真实云队列服务的故障语义：SQS 风格的 ack +
可见性超时（at-least-once，同一条消息可能因超时被重复投递）→ 崩溃模拟（消费者/服务重启，所有
未 ack 的 in-flight 消息立即重新排队，已 ack 的永远不会复活）。是"队列语义"这条 S13 技能线
最直接的编码投影，也是 sd05（Distributed Queue Service）系统设计题在编码轮的对应版本。

## Sources & confidence
主题与追问方向 **HIGH**——1point3acres 一手挂经（t.me/s/usinterview/29299，onsite SD，候选人
未通过）原话给出"Queue class（类 deque）→ 云端 queue service"这个演进路径，追问汇总明确点出
"enqueue 故障下是否需要落盘再返回"、"at-least-once vs exactly-once"、"多消费者公平调度"、
"背压"四个方向，本题的并发追问逐条对应。但挂经**没有给出具体方法签名**——`MessageQueue` 的
ack/visibility-timeout API、`requeue_all_in_flight` 崩溃模拟接口，都是本仓库按业界标准 SQS
模式做的**重建**，problem.md 在 API 契约一节明确标注。

## Approach by part
1. `SimpleQueue` 直接包一层 `collections.deque`：空队列 `dequeue`/`peek` 让 `IndexError`
   自然冒泡（不吞异常、不返回哨兵），这是 Part2"暂时没消息返回 `None`"的对照组——两种"空"的
   语义不同：Part1 是调用方的错误，Part2 的"没消息可投递"是消费者轮询的正常状态。
2. `MessageQueue` 维护三块状态：待投递的 `_ready` 队列、`_payloads` 字典、`_in_flight`
   （message_id -> (可见性截止时间, 投递序号)）。`dequeue` 每次先扫一遍 `_in_flight`，把
   截止时间 `<= now` 的消息按**截止时间升序**放回 `_ready` **队尾**（被动式超时重新投递），
   再从 `_ready` 队首弹出这次真正投递的消息。`ack` 只在 `message_id` **当前**处于 in-flight
   状态时才生效——用 id 本身兼任"消息标识"和"当前这次投递的凭证"（不像真实 SQS 那样每次投递
   发一个独立 receipt handle），这是一个刻意简化，写在 problem.md 边界清单里。
3. `requeue_all_in_flight`（Part3，重建）模拟"服务整体重启，不再信任任何在途租约"：把当前所有
   in-flight 消息**立即**（不等超时）按**原始投递顺序升序**塞回 `_ready` **队首**——这个排序
   规则刻意与 Part2 的"按截止时间排队尾"不同：崩溃恢复要让最老的未完成工作优先被重新处理，且
   排在那些从未投递过的新消息前面，测试文件用"先投递的短超时 vs 后投递的长超时"这种截止时间与
   投递顺序相反的构造专门区分两种排序规则。

## Pitfalls hidden tests target
- Part1 空队列抛异常，Part2"没消息"返回 `None`——两种设计刻意不同，不能混用
- 可见性截止半开区间：`now==截止时间` 算超时（重新投递），`now==截止时间-1` 仍在途
- 同一条消息可能被投递多次（at-least-once 的字面含义）；`ack` 只在消息**当前**处于 in-flight
  时才成功——消息超时后回到待投递队列、但**尚未被重新取走**的这段窗口里 `ack` 必须返回 `False`
  （不能凭空标记一个"当前根本没在被处理"的消息为完成）
- `ack` 未知 id / 已 ack 过的 id 都返回 `False`，不抛异常
- `requeue_all_in_flight` 已 ack 的消息永不复活；排序按**投递顺序**而非**截止时间**（测试专门
  构造两者相反的场景来区分，不能用"看起来都对"的实现蒙混过关）
- 崩溃恢复的未完成工作排在从未投递过的新消息前面

## Complexity & measured cost
`enqueue`/`ack` O(1)；`dequeue` 的超时清扫是 O(当前 in-flight 中已超时的条目数)，均摊下与总
操作数成正比但不重复；`requeue_all_in_flight` O(当前 in-flight 大小)。10 万条混合操作通过
`run_script` 实测 well under 2s / 256MB。

## Test inventory
21 tests — part1: 5（含 1 fmt）· part2: 10（含 1 io、1 perf）· part3: 6（含 1 io）；edge 12 ·
fmt 1 · io 2 · perf 1。

## Skills exercised
S13 队列语义（at-least-once、落盘确认追问、背压追问）· S09 类设计先定 API 契约（Part1 抛异常
vs Part2 返回 `None` 的刻意区分，写清楚而不是含糊）· S10（并发追问：dequeue 的原子 claim）·
S11（持久化追问：enqueue 落盘，呼应 od01/od02/od05）
