---
id: hi-lld-design-principles-8-dip
node: qb.lld.kv-store-eviction.pre-lld-in-a-hurry-design-principles
type: qa
step: 8
---
## Q
**DIP 与依赖注入，以及 SOLID 的现实地位**｜低层设计 · 速览

依赖倒置（DIP）是什么，和依赖注入有什么区别？面试里应该怎样看待 SOLID？

## A
**DIP。** 代码应依赖抽象，不依赖具体实现。「倒置」指契约由谁定：由业务逻辑按自己的需要定义接口（如 `MessageSender`），实现去适配它。

```python
class NotificationService:
    def __init__(self, sender: MessageSender) -> None:  # 注入抽象，不自己 new EmailSender
        self.sender = sender
```

**收益。** 单元测试可注入假实现而不真发邮件；换成短信只需传另一个实现。

**区别。** DIP 是原则，依赖注入（构造函数传入依赖）是实现手段。

**现实。** SOLID 出自 Java 的深继承与重接口时代；在其他语言里组合与函数更常见。别为凑原则破坏 KISS。
