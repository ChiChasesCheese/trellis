---
id: hi-c-lld-logging-service-n07-formatter
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 7
---
## Q
**日志库 · Formatter 是策略，且必须无状态**｜摘要 · 必会

`Formatter` 为什么单独成接口？实现需要加锁吗？

## A
- **接口：** `format(record) -> str`，现在有纯文本和 JSON 两个实现，CSV、键值对等是真实的扩展方向。这是策略模式（Strategy）：同一个约定下可以替换的实现。
- **避免 N×M：** 如果格式写在目的地里，两种格式乘两种目标就是 4 个类。拆出来后，一个 `Destination` 组合一个 formatter 和一个写出目标，任意组合只是构造参数。
- **分工：** formatter 管序列化，destination 管写出，彼此不知道对方的内部。
- **纯函数：** 输入一条记录返回一个字符串，不持有状态，所以两个目的地可以共用同一个 `JsonFormatter` 实例，不需要任何同步。
- **模板：** 真实的纯文本格式一般接受 `"{timestamp} {level} [{thread}] {message}"` 这样的模板，不用改代码就能换输出样式；面试里硬编码即可，被问到再说。
