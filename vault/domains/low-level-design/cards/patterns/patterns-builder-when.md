---
id: patterns-builder-when
node: patterns.creational
type: qa
---
## Q
Builder 解决哪两个构造问题，什么时候它会过度设计？

## A
- **伸缩式构造函数**：很多参数，几个可选——`new Pizza(12, true, false, null, true)` 难以阅读且容易出错。Builder 提供命名的、顺序无关的步骤。
- **分阶段构造的不可变对象**：可变地收集值，在 `build()` 中验证所有内容，输出不可变结果——没有半初始化对象会逃逸。

当类只有≤3个必需参数且没有可选参数时跳过它——普通构造函数（或有命名意图的静态工厂）更清晰。GoF 中的「director」角色在实践中几乎不需要；流式 builder 形式是面试期望的。
