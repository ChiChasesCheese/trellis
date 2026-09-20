---
id: principles-shallow-abstraction-test
node: principles.simplicity
type: qa
---
## Q
一个抽象何时太浅了？如何测试抽象是否有价值？

## A
一个抽象太浅了，当它：
- 只是为一个实现提供一个不同的名称（例如：`interface Logger { void log(String msg); }` 对 `System.out.println` 的 15 行包装）
- 没有隐藏任何复杂性或做任何有趣的事情
- 实现是微不足道的，抽象不能处理变化

测试抽象是否有价值：
1. 你能实现 2-3 个不同的、有意义的版本吗？（如果不能，太浅了）
2. 能否在不更改调用者的情况下切换实现？
3. 它是否降低了调用者代码的复杂性或提高了理解性？
