---
id: patterns-chain-of-responsibility
node: patterns.behavioral
type: qa
---
## Q
什么样的请求形状需要 Chain of Responsibility，它与 decorator 栈（相同的「链式包装器」外观）有何不同？

## A
当请求应沿着一条处理程序管道传递，其中**每一个可能处理、转换或拒绝，且集合/顺序必须可配置**时使用它：HTTP 中间件（auth → rate-limit → validate）、批准升级（经理→总监→副总）、日志级别、支持工单路由。

```java
abstract class Handler {
    Handler next;
    void handle(Request r) { if (!process(r) && next != null) next.handle(r); }
```

Decorator 修饰单个对象；Chain 让多个对象有机会处理请求。
