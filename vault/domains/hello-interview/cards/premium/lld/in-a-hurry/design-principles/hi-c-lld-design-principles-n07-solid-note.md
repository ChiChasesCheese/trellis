---
id: hi-c-lld-design-principles-n07-solid-note
node: lld.in-a-hurry.design-principles.notes
type: qa
step: 7
---
## Q
**设计原则 · SOLID 的适用范围**｜摘要 · 必会

SOLID 来自什么环境？在现代语言里该怎么对待，会和哪条原则冲突？

## A
- **由来：** SOLID 是五条面向对象原则（SRP、OCP、LSP、ISP、DIP）的缩写，诞生于 Java 的鼎盛期，那时流行很深的继承层级和很多接口。
- **现状：** 除了 Java 和 C#，过度套用 SOLID 已不流行；现代语言更倾向组合而不是类层级，更倾向函数而不是接口。
- **会和 KISS 冲突：** 如果一个简单方案够用，却为了"符合 SOLID"硬加接口和抽象，就违反了保持简单的原则。
- **面试里的用法：** 题目确实需要时再用这些原则，并能说出什么时候是在为复杂而复杂。
