---
id: hi-lld-patterns-3-factory
node: qb.lld.kv-store-eviction.pre-lld-in-a-hurry-patterns
type: qa
step: 3
---
## Q
**工厂：集中创建逻辑**｜低层设计 · 速览

低层设计面试里什么时候用工厂？请写出一个通知类型的简单工厂，并说明它和 GoF 工厂方法的区别，以及它和策略的分工。

## A
```python
class NotificationFactory:
    @staticmethod
    def create(kind: str) -> Notification:
        if kind == "email":
            return EmailNotification()
        if kind == "sms":
            return SMSNotification()
        raise ValueError("Unknown type")
```

**用法。** 需求出现“支持不同的通知类型”“支持多种支付方式”时，调用方只写 `create(kind)`，新增推送通知只需改工厂这一处。

**区别。** 这其实是简单工厂（Simple Factory）；GoF 的工厂方法用抽象工厂类加子类重写，更复杂，面试里很少见，说“用工厂”时人们指的就是上面这种。

**分工。** 工厂决定实例化哪个类；策略决定对象建好之后用哪种行为。

**易错。** 工厂在 Java 之外有争议，被看作过度设计，用之前看一眼面试官的表情。
