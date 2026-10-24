---
id: pl-meta-annotations-philosophy-declare-vs-execute
node: metaprogramming.annotations-decorators
type: qa
step: 8
---
## Q
Java 注解和 Python 装饰器看起来都是写在函数上方的 `@xxx`，它们在哲学上有什么根本区别？

## A
**Java 注解只是数据**。`@Transactional` 这一行本身什么都不做，它只是一个事实声明：「这个方法需要事务」。真正的行为发生在别的地方：Spring 容器启动时扫描、给 bean 套一层代理。读代码的人要知道框架存在、知道它怎样读标签，才能理解这个方法的运行时行为。这就是所谓的「远距离作用」（action at a distance）：行为的原因和结果不在同一处。

**Python 装饰器是代码**。`@cache` 就是 `f = cache(f)`，你可以打开 `cache` 的源码，看到它怎样包装函数，用调试器单步进去，也可以不用 `@` 语法手动调用。行为在定义时就确定，没有容器。

**这反映各自的价值观**：Java 相信「关注点分离」，由容器统一治理横切逻辑，代价是对框架的依赖与魔法感；Python 相信「显式优于隐式」（The Zen of Python），函数就是函数，没有额外一层规则。Go 站在更远处：它拒绝两种做法，用 struct tag 保持最小，横切逻辑则用显式的中间件函数链，宁可多写几行，也要让读者顺着调用栈走完全部逻辑。

**实践后果**：Java 项目调试 `@Transactional` 失效时要懂代理机制；Python 项目调试装饰器时只需要读一个函数。
