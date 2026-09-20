---
id: patterns-decorator-vs-proxy
node: patterns.structural
type: qa
---
## Q
Decorator vs Proxy——两者都包装对象。区分的关键是什么，它们在 LLD 中何时竞争？

## A
- **Decorator**：向现有对象**添加行为**，不改变其接口（日志、计时、缓存包装）。调用方知道包装发生了。
- **Proxy**：代表对象，通常隐藏创建或访问的细节（远程代理延迟初始化对象、虚拟代理避免创建）。调用方通常不知道代理。

竞争案例：缓存。Decorator 框架说「缓存是一个增强层」；Proxy 框架说「缓存是对底层的保护」。选择反映你的架构意图：缓存是可堆叠的增强（Decorator）还是隐藏的优化（Proxy）。
