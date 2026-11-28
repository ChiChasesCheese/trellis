---
id: hi-c-lld-patterns-n06-decorator
node: lld.in-a-hurry.patterns.notes
type: qa
step: 6
---
## Q
**设计模式 · Decorator：运行时叠加行为**｜摘要 · 必会

Decorator 模式解决什么？什么时候选它而不是子类？

## A
- **作用：** 不改类的前提下给对象叠加行为；触发词：可选功能、叠加、组合多个增强（如日志、加密）
- **做法：** 每个装饰器实现同一接口并包住另一个对象，写入时先压缩再加密再落盘，可任意堆叠
- **对比子类：** 组合爆炸时（`LoggedEncryptedEmail`……）用装饰器；行为在设计期固定、是稳定的类型变体时用子类
- **要点：** 取决于运行时条件就用 Decorator；顺序在真实系统中会影响结果
- **装饰器不是 Python 的 @：** 与 Python 的 `@` 语法同名但不是一回事
