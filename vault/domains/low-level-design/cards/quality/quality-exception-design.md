---
id: quality-exception-design
node: quality.errors
type: qa
---
## Q
在 LLD 轮里设计异常：什么样的领域异常算好，面试官会挑出哪两宗处理上的罪？

## A
一个好的领域异常：

- **具体且有语义** —— `SeatAlreadyLockedException(seatId)`，而不是 `RuntimeException("error")`；它点名被违反的业务规则，并携带做出反应所需的数据（重试？换个座位？）。
- 继承自一个小的层次结构（比如 `BookingException`），让调用方能按自己关心的粒度去捕获。

两宗罪：

- **吞掉**：`catch (Exception e) {}`（或者记个日志就继续）—— 系统带着损坏的状态一瘸一拐地走下去，故障最终在离病因很远的地方浮现。
- **裸接裸抛**：包装时不添加任何上下文，或者仅仅为了记日志而捕获再抛出 —— 同一个错误在三层里被记了三遍。能处理的地方才处理；否则就让它往上传，只在层边界处做转换（并把 cause 串起来）。
