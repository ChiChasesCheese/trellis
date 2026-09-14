---
id: patterns-chain-of-responsibility
node: patterns.behavioral
type: qa
---
## Q
What request shape calls for chain of responsibility, and how does it differ from a decorator stack (same "linked wrappers" look)?

## A
Use it when a request should pass along a pipeline of handlers where **each may handle, transform, or reject, and the set/order must be configurable**: HTTP middleware (auth → rate-limit → validate), approval escalation (manager → director → VP), logging levels, support-ticket routing.

```java
abstract class Handler {
    Handler next;
    void handle(Request r) { if (!process(r) && next != null) next.handle(r); }
}
```

Vs decorator: a decorator **always delegates** — every layer runs, the point is *accumulating behavior*. A CoR handler **may stop the chain** — the point is *finding who deals with it* (or filtering). Also be explicit about the fall-through policy: what happens when no handler accepts (default handler vs error).

## Q zh
什么样的请求形状需要 Chain of Responsibility，它与 decorator 栈（相同的「链式包装器」外观）有何不同？

## A zh
当请求应沿着一条处理程序管道传递，其中**每一个可能处理、转换或拒绝，且集合/顺序必须可配置**时使用它：HTTP 中间件（auth → rate-limit → validate）、批准升级（经理→总监→副总）、日志级别、支持工单路由。

```java
abstract class Handler {
    Handler next;
    void handle(Request r) { if (!process(r) && next != null) next.handle(r); }
```

Decorator 修饰单个对象；Chain 让多个对象有机会处理请求。
