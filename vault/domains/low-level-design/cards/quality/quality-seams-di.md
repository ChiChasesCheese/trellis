---
id: quality-seams-di
node: quality.testability
type: qa
step: 1
---
## Q
可测性意义上的"接缝（seam）"是什么？为什么在方法内部直接实例化协作者会把这个接缝焊死？

## A
接缝（Michael Feathers 的定义）是代码里一个"不修改被测代码本身就能改变程序行为"的位置——也就是某个协作者可以被替换成别的实现的地方。

```python
class OrderService:
    def place(self, order):
        gateway = StripeGateway()  # 没有接缝：测试必须真的打一次 Stripe
        gateway.charge(order.total)
```
`gateway = StripeGateway()` 把具体实现硬编码在了使用点上，测试代码没有任何位置能把它换成假的实现，除非去 monkeypatch 内部细节。修法是通过构造函数把依赖作为参数接收，测试传入 fake，生产环境的装配统一发生在应用入口（composition root）。经验法则：一个方法可以自己创建**值对象**（不带副作用的数据），但凡是涉及网络、时间、随机性、或者本身有值得被替换的行为的对象，都该被注入进来而不是内部 `new` 出来。
