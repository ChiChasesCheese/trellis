---
id: quality-couplers-refactorings
node: quality.smells
type: qa
step: 5
---
## Q
诊断并修复四种耦合者（coupler）味道：功能依恋（feature envy）、消息链（message chains）、不当亲密关系（inappropriate intimacy）、中间人（middle man）。

## A
功能依恋：一个方法用别的对象的数据比用自己的还多，比如 `order.customer.address.formatted()` 这段格式化逻辑却住在 `InvoicePrinter` 里——修法是搬移方法（move method），把行为搬到数据实际所在的地方，因为行为应该跟着状态走。消息链：`order.customer.address.city` 这种一路点下去的调用，把调用方焊死在整条导航路径上——修法是隐藏委托（hide delegate），让 `order` 自己暴露一个 `order.customer_city()`。

不当亲密关系：两个类频繁互相翻对方的内部字段——修法是把这段交互收进一个类，或者把共享部分抽成第三个类。中间人：一个类的方法几乎全部只是转发给另一个对象——修法是移除中间人（remove middle man），让调用方直接找目标对象说话；注意它和消息链其实互为镜像，一个是"链太长"，一个是"专门为了缩短链而加了一层没有自己逻辑的壳"，治过头就会从一个坏味道换成另一个。
