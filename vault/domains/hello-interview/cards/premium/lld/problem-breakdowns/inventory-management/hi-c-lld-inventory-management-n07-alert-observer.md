---
id: hi-c-lld-inventory-management-n07-alert-observer
node: lld.problem-breakdowns.inventory-management.notes
type: qa
step: 7
---
## Q
**库存管理 · AlertConfig 与 AlertListener：观察者**｜摘要 · 必会

告警为什么拆成配置对象加监听器接口？Python 里一定要写接口类吗？

## A
- **`AlertConfig`：** 阈值加监听器配成一对，两个字段创建后不变。用具名类型的价值是清晰：`list[AlertConfig]` 一眼就懂，而 `dict[int, Listener]` 要猜键是不是阈值。
- **`AlertListener`：** 一个方法，`on_low_stock(warehouse_id, product_id, current_qty)`，三个参数告诉监听器是哪个仓库、哪个商品、现在剩多少。
- **实现多样：** 邮件、webhook、写日志都是不同实现，库存系统不知道也不关心，只调用接口方法。这是观察者模式（Observer）：仓库在有趣的事情发生时通知监听者，监听者决定怎么处理。
- **依赖倒置：** 高层的 `Warehouse` 不依赖 `EmailSender`、`WebhookClient` 等低层通知机制，二者都依赖 `AlertListener` 抽象；换通知方式不用改仓库。
- **语言适配：** 现代语言里简单的观察者常用回调函数代替接口（JavaScript 函数、Python 的 lambda 或可调用对象、Go 的函数类型）。面试里写接口是为了把结构说清；生产代码按语言习惯来。
- **只定义接口即可：** 除非被要求，不必实现具体的监听器类，把不同实现怎么工作讲清楚就能体现多态。
