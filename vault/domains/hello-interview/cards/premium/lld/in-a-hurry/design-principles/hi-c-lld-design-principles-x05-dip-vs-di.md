---
id: hi-c-lld-design-principles-x05-dip-vs-di
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 5
---
## Q
**设计原则 · 注入具体类算 DIP 吗**｜考点 · 必会

`NotificationService.__init__(self, sender: EmailSender)` 通过构造参数传入了发送者。这满足 DIP 吗？满足依赖注入吗？

## A
- **依赖注入：** 满足，依赖由外部传入
- **DIP：** 只算一半，类型标注仍是具体类，业务类知道"邮件"这个实现细节
- **改法：** 参数类型换成 `MessageSender` 抽象（接口、ABC 或 Protocol）
- **检验：** 换成短信实现时，`NotificationService` 要不要改
