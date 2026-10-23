---
id: hl-j12-implicit-param
node: java21.j12-scoped-values
type: qa
step: 1
---
## Q
什么是「隐式参数」问题？`ThreadLocal` 是怎么解决它的、内部结构是什么？

## A
一个下单请求要经过十几层方法（`controller → service → risk → pricing → audit → logger`），最底层的 `logger` 想打出**当前请求的 traceId 和账户号**。

- 办法一：每个方法加个 `RequestContext ctx` 参数一路传，十几个签名全被污染，第三方回调接口更改不了。
- 办法二：放进「线程私有的全局变量」，谁需要谁取，这就是 `ThreadLocal`：

```java
static final ThreadLocal<String> USER = new ThreadLocal<>();
USER.set("alice");   // 存到当前线程自己的小表里
USER.get();          // 只取当前线程的；别的线程取不到
```
内部：每个 `Thread` 里有张 `ThreadLocalMap`，`ThreadLocal` 对象只是 key，所以「每线程一份」。
