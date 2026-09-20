---
nodes: [problems.machines.traffic-signal]
url: https://docs.python.org/3/library/typing.html#typing.Protocol
---
# typing.Protocol — 结构化子类型（静态鸭子类型）

值得读：配时方案为什么用协议而不是抽象基类，依据就在这一节。协议是**结构化子类型**
（structural subtyping）：一个类只要有 `hold(ctx) -> bool` 这个方法，就自动满足
`TimingPlan`，不需要继承任何东西、不需要注册。测试里临时写一个"永远返回 True 的假方案"
只要三行，而抽象基类要求你先 `import` 再继承——在机器编码轮里，这是能当场省下的两分钟。

文档里另外两点在这道题上也用得着：`@runtime_checkable` 让 `isinstance` 对协议可用（但它
只查方法名，不查签名，所以别把它当类型检查用）；协议里的方法体写 `...` 就够，不必
`raise NotImplementedError`——协议不是用来被继承的。什么时候仍然该用抽象基类？当你想给所有
实现一段共享的具体代码时；配时方案没有这种共享代码，所以协议是更轻的那一个。
