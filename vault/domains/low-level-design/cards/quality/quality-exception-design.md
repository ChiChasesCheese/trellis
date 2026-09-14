---
id: quality-exception-design
node: quality.errors
type: qa
---
## Q
Designing exceptions in an LLD round: what makes a good domain exception, and what are the two handling sins interviewers flag?

## A
A good domain exception:

- Is **specific and semantic** — `SeatAlreadyLockedException(seatId)`, not `RuntimeException("error")`; it names the business rule violated and carries the data needed to react (retry? pick another seat?).
- Extends a small hierarchy (e.g. `BookingException`) so callers can catch at the granularity they care about.

The two sins:

- **Swallowing**: `catch (Exception e) {}` (or log-and-continue) — the system limps on in a corrupt state and the failure surfaces far from its cause.
- **Catch-and-rethrow bare**: wrapping without adding context, or catching just to log then rethrowing — the same error gets logged three times at three layers. Handle where you can act; otherwise let it propagate, translating only at layer boundaries (with the cause chained).

## Q zh
在 LLD 轮里设计异常：什么样的领域异常算好，面试官会挑出哪两宗处理上的罪？

## A zh
一个好的领域异常：

- **具体且有语义** —— `SeatAlreadyLockedException(seatId)`，而不是 `RuntimeException("error")`；它点名被违反的业务规则，并携带做出反应所需的数据（重试？换个座位？）。
- 继承自一个小的层次结构（比如 `BookingException`），让调用方能按自己关心的粒度去捕获。

两宗罪：

- **吞掉**：`catch (Exception e) {}`（或者记个日志就继续）—— 系统带着损坏的状态一瘸一拐地走下去，故障最终在离病因很远的地方浮现。
- **裸接裸抛**：包装时不添加任何上下文，或者仅仅为了记日志而捕获再抛出 —— 同一个错误在三层里被记了三遍。能处理的地方才处理；否则就让它往上传，只在层边界处做转换（并把 cause 串起来）。
