---
id: hi-c-lld-design-principles-n10-lsp
node: lld.in-a-hurry.design-principles.notes
type: qa
step: 10
---
## Q
**设计原则 · LSP：子类能顶替父类**｜摘要 · 必会

里氏替换原则（LSP）的判断标准是什么？`Penguin` 继承 `Bird` 并在 `fly()` 里抛异常错在哪，怎么改？

## A
- **标准：** 凡是用到父类的地方，换成任何一个子类都不能出问题；子类可以增加行为，但不能删除或破坏父类承诺的行为。
- **红旗：** 子类对父类提供的方法抛异常，或调用方为了避开某个子类被迫写 `instanceof Penguin` 这样的特判——说明父类的承诺子类并没兑现。
- **改法：** `Bird` 只保留所有鸟都有的行为（比如吃），"会飞"另放在 `FlyingBird` 里；`Sparrow` 继承 `FlyingBird`，`Penguin` 只继承 `Bird`。
- **面试里：** 设计类层级时，认真想清楚哪些方法属于基类、哪些只属于部分子类。
