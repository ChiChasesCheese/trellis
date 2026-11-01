---
id: hi-lld-design-principles-7-lsp-isp
node: lld.in-a-hurry.design-principles
type: qa
step: 7
---
## Q
**LSP 与 ISP：子类别违约，接口别太肥**｜低层设计 · 速览

里氏替换（LSP）与接口隔离（ISP）分别要求什么？企鹅和机器人的经典反例该怎么改？

## A
**LSP。** 凡是用到父类的地方换成任何子类都不该出错：子类可以增加行为，但不能删掉或破坏父类承诺的行为。子类对父类提供的方法抛异常、或迫使调用方写 `instanceof Penguin` 的特例，就是违反。

**改法。** 把会飞单独分出去：Bird 只有 `eat`，FlyingBird 继承 Bird 并加 `fly`，Sparrow 实现 FlyingBird，Penguin 只继承 Bird。

**ISP。** 偏好小而专的接口，别逼类实现用不到的方法。Robot 继承含 `eat`、`sleep` 的 Worker，只能写空实现，是坏味道；拆成 Workable、Feedable、Restable，Human 全实现，Robot 只实现 Workable。
