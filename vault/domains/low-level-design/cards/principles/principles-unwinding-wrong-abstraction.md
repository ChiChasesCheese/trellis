---
id: principles-unwinding-wrong-abstraction
node: principles.simplicity
type: qa
---
## Q
当你意识到一个抽象是错误的，为什么解开它而不是改进它？

## A
当一个抽象错误时，尝试改进它通常会导致更多的复杂性。更好的方法：

1. 复制代码回到每个调用者（是的，重新引入重复）
2. 现在在隔离的上下文中优化每个版本
3. 一旦它们稳定并且真正的模式出现，提取正确的抽象

这违反了 DRY，但：
- 一个坏的抽象比重复更糟
- 重复暴露了真正的差异
- 改进一个坏的抽象很难；更好地开始就是正确的

这来自 Sandi Metz 的 "All the Little Things" 演讲。
