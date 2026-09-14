---
id: cc-input-struct-keep-unknown-keys
node: input.structured
type: qa
---
## Q
Your handler needs only `amount` and `merchant`, but a later part adds rules that can name *any* field of the record. How should the parser hand the record over?

## A
**As the whole dict, not as a projected tuple.**

Extracting `(amount, merchant)` at parse time is the cheapest thing to write and the most expensive to undo: when Part 3 adds `card_country = "US"` rules, the field the rule names was thrown away three functions upstream, and you cannot add it without changing every signature between.

Keep the full mapping, and let each consumer take what it needs. Unknown keys are ignored by the ledger and visible to the rule engine at the same time — that is the whole point of passing the record rather than its summary.

## Q zh
你的 handler 只需要 `amount` 和 `merchant`，但后面的部分会加入可以引用记录里**任意**字段的规则。解析器该怎么把记录交出去？

## A zh
**交出整个 dict，而不是投影出来的元组。**

在解析时抽出 `(amount, merchant)` 是最省事的写法，也是最难撤销的：等 Part 3 加入 `card_country = "US"` 这类规则时，规则引用的字段在上游三个函数之前就被扔掉了，不改动中间所有签名就加不回来。

保留完整映射，让每个消费者各取所需。账本忽略未知 key，同时规则引擎又能看见它们 —— 这正是传记录而不是传摘要的意义。
