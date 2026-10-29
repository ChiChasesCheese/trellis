---
id: uth-compose-spring-three-level-cache-5-real-world
node: compose.spring-three-level-cache
type: qa
step: 5
---
## Q
**真实实现多做的事：并发、检查、默认禁止环**｜Spring Framework · 7.0

真实的 `DefaultSingletonBeanRegistry` 比三张表多处理了什么？使用时最容易踩的坑是什么？

## A
**细节。**

- 并发：三张表都是 `ConcurrentHashMap`，取成品先不加锁查一次；要现场产出早期引用才拿锁。6.1 用 `synchronized (singletonObjects)`，6.2 起换成 `ReentrantLock`，`tryLock` 失败就返回空，不在别的线程里造早期引用
- 一致性检查：早期引用已借出，自己却在初始化阶段被包成另一个对象，就抛 `BeanCurrentlyInCreationException`（“被注入的是原始版本”）。`@Async` 的后处理器只在初始化后包代理、不参与早期引用，是典型触发者
- 无解的环：构造器注入（对象还没 `new` 出来，工厂登记不了）；多例（prototype）Bean 不走这套缓存，直接抛错
- 只有单例且 `allowCircularReferences` 为真才登记工厂

**为什么。** 三级缓存是让环“凑合能跑”的补丁，代价是别人会拿到没造完的对象。Spring 的文档建议拆出第三个 Bean 放共同逻辑。

**坑。** Spring Boot 2.6 起默认禁止循环依赖，有环的老项目升级后启动失败；`spring.main.allow-circular-references=true` 可以临时打开。

**对应 LeetCode：** 无直接对应的题
