---
id: uth-compose-interceptor-chain-4-real-world
node: compose.interceptor-chain
type: qa
step: 4
---
## Q
**真实实现多做的事：缓存链、动态匹配、复制游标**｜Spring AOP · 7.0

真实的 Spring AOP 在“列表加游标”上还做了什么？为什么要重试的拦截器必须复制调用对象？

## A
**细节。**

- 链按方法缓存：`AdvisedSupport` 的 `methodCache`（方法 → 拦截器列表）；增删通知（`adviceChanged()`）就整张清空。没有任何通知时，代理直接反射调用目标，连调用对象都不创建
- 动态匹配：列表里有的项带运行时条件，按实际参数再判断一次；不匹配就跳过这一环，继续 `proceed()`
- 游标属于这次调用：每次调用新建 `ReflectiveMethodInvocation`，列表共享
- 复制游标：`invocableClone()` 复制调用对象，共用列表和目标，游标独立

**为什么。** 游标放在每次调用自己的对象里，列表才能被所有线程共享、缓存。

**坑。** 想重试的拦截器直接再调一次 `proceed()`：游标已在链尾，后面的拦截器被跳过，只会再调一次目标方法。要在进入这一环时先 `invocableClone()`，每次重试对一份副本 `proceed()`。

**对应 LeetCode：** 无直接对应的题
