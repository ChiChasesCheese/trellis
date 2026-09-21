---
id: test-mock-side-effect-vs-return-value
node: engineering.testing
type: qa
source: python-docs
---
## Q
`Mock(return_value=3)` 和 `Mock(side_effect=KeyError('foo'))` 有什么区别？要测试「被测代码正确处理依赖抛出的异常」，该配置哪一个？

## A
`return_value` 让 mock 每次被调用都返回同一个固定值。`side_effect` 更灵活：设为一个异常类或异常实例时，mock 被调用会直接抛出这个异常；设为可迭代对象（如列表）时，每次调用依次返回其中的下一个值（用完即报错），可以模拟一连串不同的返回结果。要测试异常处理路径，应把依赖的 mock 设置 `side_effect=SomeError(...)`，让被测代码在调用它时真的收到这个异常。
