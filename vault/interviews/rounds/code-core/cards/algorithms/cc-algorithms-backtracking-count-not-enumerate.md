---
id: cc-algorithms-backtracking-count-not-enumerate
node: algorithms.backtracking
type: cloze
---
When the question is "how many expansions" rather than "list them", never materialize: a template of independent groups has {{c1::the product of the group sizes}} expansions, which can be {{c2::10^20}} — beyond any list, and instantly computable as a Python `int`. The same split applies to {{c3::the k-th element}}: rank it by counting how many completions each prefix admits and descending, which costs O(length × alphabet) instead of {{c4::enumerating everything and indexing}}.

## zh
当问题是「有多少种展开」而不是「把它们列出来」时，绝不要真的构造：由独立分组构成的模板有 {{c1::各组大小之积}} 种展开，可能高达 {{c2::10^20}} —— 任何列表都装不下，但作为 Python `int` 可以瞬间算出。同样的区分适用于 {{c3::第 k 个元素}}：通过统计每个前缀能接多少种补全并逐层下降来给它定位，代价是 O(长度 × 字母表大小)，而不是 {{c4::全部枚举出来再取下标}}。
