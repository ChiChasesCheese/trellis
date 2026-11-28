---
id: hi-c-lld-design-principles-n12-dip
node: lld.in-a-hurry.design-principles.notes
type: qa
step: 12
---
## Q
**设计原则 · DIP：依赖抽象**｜摘要 · 必会

依赖倒置原则（DIP）里"倒置"的是什么？它和依赖注入是一回事吗？

## A
- **内容：** 业务代码应该依赖抽象，而不是具体实现。`NotificationService` 不要自己创建 `EmailSender`，而是通过构造参数接收一个 `MessageSender` 接口。
- **"倒置"指的是契约由谁来定：** 通常业务逻辑要迁就实现提供的接口；DIP 反过来，先按业务需要定义接口，再让各种实现去适配它。
- **收益：** 测试时可以注入假的发送者，不会真的发邮件；换成短信只需传另一个实现，服务代码不改。
- **区别：** DIP 是设计原则（依赖谁），依赖注入是实现手段（通过构造参数传入），相关但不是同一件事。
