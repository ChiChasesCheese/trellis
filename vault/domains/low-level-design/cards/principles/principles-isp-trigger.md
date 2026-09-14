---
id: principles-isp-trigger
node: principles.solid
type: qa
---
## Q
Your `Machine` interface declares print/scan/fax; the basic printer implements `scan()` and `fax()` as throwing stubs. Which principle, and the refactor?

## A
**ISP** — no client (or implementer) should be forced to depend on methods it doesn't use. Those throwing stubs are also latent LSP bombs: any caller holding a `Machine` can blow up.

Refactor into role interfaces `Printer`, `Scanner`, `Fax`; the multifunction device implements all three; each client takes only the role it needs. Trigger to memorize: **no-op or throwing implementations = fat interface**.

## Q zh
什么时候你知道你的接口违反了接口分离原则？

## A zh
触发器：
- 实现者强制实现它们不使用的方法
- 调用者只调用接口的一部分
- 接口名中有多个概念："Read-Write-Lock"、"Serializable-Comparable"
- 一个类有多个客户端需要不同的操作子集

症状：
- 模拟或存根会伪造不用的方法
- 测试中对实现者不相关的方法进行设置
