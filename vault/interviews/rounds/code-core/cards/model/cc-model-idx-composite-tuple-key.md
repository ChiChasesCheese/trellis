---
id: cc-model-idx-composite-tuple-key
node: model.index
type: cloze
---
When a rule counts "transactions by the same customer at the same merchant in the same hour", the key is the tuple {{c1::`(merchant, customer, hour)`}} in a single flat dict — not three levels of nested dicts, which cost you {{c2::a `setdefault` at every level and a nested loop to iterate}}. Tuples work as keys because they are {{c3::hashable when their elements are}}, so a list or a dict inside the key is what breaks it.

## zh
当规则要统计「同一顾客在同一商户同一小时内的交易数」时，key 就是单层扁平 dict 里的元组 {{c1::`(merchant, customer, hour)`}} —— 而不是三层嵌套 dict，那会让你付出 {{c2::每一层一次 `setdefault`，外加遍历时的嵌套循环}}。元组能当 key 是因为 {{c3::当其元素可哈希时它就可哈希}}，所以把 list 或 dict 放进 key 才是出问题的地方。
