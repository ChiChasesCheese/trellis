---
id: cc-output-ordering-string-vs-numeric
node: output.ordering
type: cloze
---
Sorting the ids `acct_2` and `acct_10` as plain strings puts {{c1::`acct_10` before `acct_2`}}, because `'1' < '2'` at the first differing character; the same is true of `m10 < m2`, and `B < a` because {{c2::upper-case letters sort before lower-case in ASCII}}. Numeric order needs an explicit key such as {{c3::`sorted(ids, key=lambda s: int(s.split("_")[1]))`}}. Read the worked example's output to decide which the spec wants — and {{c4::never assume the "natural" one}}.

## zh
把 id `acct_2` 和 `acct_10` 当普通字符串排序，会把 {{c1::`acct_10` 排在 `acct_2` 前面}}，因为在第一个不同的字符处 `'1' < '2'`；`m10 < m2` 同理，而 `B < a` 是因为 {{c2::ASCII 里大写字母排在小写字母之前}}。数值顺序需要显式的 key，例如 {{c3::`sorted(ids, key=lambda s: int(s.split("_")[1]))`}}。看样例输出来判断 spec 要哪一种 —— 而且 {{c4::绝不要假设是「自然的」那一种}}。
