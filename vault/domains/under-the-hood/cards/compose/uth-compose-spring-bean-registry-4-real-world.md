---
id: uth-compose-spring-bean-registry-4-real-world
node: compose.spring-bean-registry
type: qa
step: 4
---
## Q
**真实实现多做的事：写时复制、冻结、派生缓存**｜Spring Framework · 7.0

真实的 `DefaultListableBeanFactory` 在这个骨架上还加了什么？为什么不是简单的 Map 加 List？

## A
**细节。**

- 读多写少：`beanDefinitionMap` 是 `ConcurrentHashMap`；名字列表在启动阶段直接 `add`，一旦开始创建 Bean（`hasBeanCreationStarted()`），改成“复制整张列表、改副本、再换掉引用”（写时复制，copy-on-write），正在遍历的线程看到的列表不会被改动
- 冻结：`freezeConfiguration()` 把名字列表拷成数组，之后遍历直接读数组；再注册定义就把它清空
- 派生缓存要同步失效：`allBeanNamesByType`（类型 → 名字）等缓存，在 `addSingleton` 时清掉受影响类型的条目，配置冻结后再注册定义则整体清空
- 销毁：`disposableBeans` 是 `LinkedHashMap`，按创建的顺序记录、反序销毁；`destroyBean` 先销毁 `dependentBeanMap` 里的依赖者，再销毁自己，最后清依赖表

**为什么。** 注册集中在启动阶段，读发生在所有线程。把“写”限制在启动，读路径就不用加锁。

**坑。** 同名定义：Framework 默认允许后者覆盖前者；Spring Boot 2.1 起默认关闭，重名直接启动失败（`spring.main.allow-bean-definition-overriding=true` 可打开）。

**对应 LeetCode：** 无直接对应的题
