---
id: cc-input-del-maxsplit
node: input.delimited
type: cloze
---
When the **last** field is free text that may itself contain the delimiter — a payment memo, a reclaim request carrying a company name — split with a bound: {{c1::`line.split(",", 2)`}} yields exactly three pieces and leaves every later comma inside the memo. The mirror case, a free-text field at the **front**, uses {{c2::`rsplit`}} with the same bound. The bug this replaces is {{c3::a memo containing a comma silently shifting every field after it}}.

## zh
当**最后**一个字段是可能含有分隔符的自由文本 —— 付款备注、带公司名的回收请求 —— 就用带上限的切分：{{c1::`line.split(",", 2)`}} 恰好给出三段，备注里后续的逗号全部保留。镜像情形（自由文本在**开头**）则用同样带上限的 {{c2::`rsplit`}}。它替掉的 bug 是 {{c3::备注里的一个逗号悄悄让其后每个字段都错位}}。
