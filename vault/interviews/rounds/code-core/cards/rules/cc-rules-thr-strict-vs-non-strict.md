---
id: cc-rules-thr-strict-vs-non-strict
node: rules.thresholds
type: cloze
---
English maps to comparisons like this: "exceeds", "more than", "over" mean {{c1::strict `>`}}; "at least", "reaches", "no fewer than", "or more" mean {{c2::non-strict `>=`}}; "up to" and "no more than" mean `<=`. When the statement is ambiguous the deciding input is always {{c3::the exactly-equal case}} — so write that test first and keep the operator behind a single named comparison you can flip.

## zh
英文到比较运算符的映射是这样的：「exceeds」「more than」「over」表示 {{c1::严格的 `>`}}；「at least」「reaches」「no fewer than」「or more」表示 {{c2::非严格的 `>=`}}；「up to」「no more than」表示 `<=`。题面含糊时，决定性的输入永远是 {{c3::恰好相等的那一例}} —— 所以先写这个测试，并把运算符收在一处可翻转的具名比较里。
