---
id: test-mock-autospec-catches-typo
node: engineering.testing
type: qa
source: python-docs
---
## Q
用裸的 `Mock()`（不传 `spec`）替换被测对象，测试代码哪怕调用了一个真实类里根本不存在的方法名，或者传错了参数个数，为什么还是会「测试通过」？用什么机制能让这类错误在测试阶段就暴露？

## A
`Mock` 对象访问任何属性或方法都会即时创建并返回一个新的 Mock，不会检查这个属性/方法在真实对象上是否存在，也不检查调用签名，所以拼错方法名或传错参数依然「调用成功」。用 `create_autospec()`（或 `patch(..., autospec=True)`）创建的 mock 会复制真实对象的属性、方法列表和调用签名，访问不存在的属性会抛 `AttributeError`，用错误的参数调用会抛 `TypeError`，让 mock 在用错的方式上和真实代码表现一致。
