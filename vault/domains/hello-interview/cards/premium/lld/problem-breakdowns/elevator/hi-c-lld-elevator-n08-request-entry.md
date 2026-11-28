---
id: hi-c-lld-elevator-n08-request-entry
node: lld.problem-breakdowns.elevator.notes
type: qa
step: 8
---
## Q
**电梯系统 · 控制器的呼叫入口怎么写**｜摘要 · 必会

`request_elevator` 的三步逻辑和边界处理是什么？

## A
- **三步：** 校验→选一部电梯→把请求交给它。
- **校验：** 楼层小于 0 或大于 9 返回 false；类型是目的层也返回 false，因为楼层呼叫只能是上或下。
- **在边界创建 `Request`：** 校验通过后立刻构造请求对象，之后整个系统传递的都是已验证的对象，不必在深处重复检查。
- **选哪部电梯：** 抽成独立的 `select_best_elevator(request)`，这样调度策略可替换，入口本身不变。
- **建议的讲法：** 先实现最简单的，再主动问"要不要考虑方向"，表明你想到了而没有过度设计。
