---
id: cc-input-struct-missing-key-policy
node: input.structured
type: cloze
---
A field named by a rule is simply absent from the record. The policy must be an explicit choice, made once: a rule engine in the style of Radar treats a missing field as making the comparison {{c1::False — including `!=`, which does *not* match a missing field}}; a validator may instead {{c2::substitute a stated default}}; a strict reader may reject the record. What you must never do is {{c3::let `KeyError` decide it from wherever the first lookup happens to be}}.

## zh
规则引用的字段在记录里根本不存在。策略必须是一次性的明确选择：Radar 风格的规则引擎把缺失字段视为使该比较 {{c1::为 False —— 包括 `!=`，它对缺失字段**不**匹配}}；校验器则可能 {{c2::代入题面规定的默认值}}；严格的读取器可以直接拒绝这条记录。绝不能做的是 {{c3::让 `KeyError` 在第一次查表恰好发生的地方替你决定}}。
