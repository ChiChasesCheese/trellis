---
id: cc-rules-grp-running-count-includes-current
node: rules.grouping
type: cloze
---
When a rule fires on "the 3rd and every later transaction of that pair", the counter is incremented {{c1::before the test, so the current row is counted}}: the row whose running count is {{c2::3}} is the first to fire, and the row whose count is 2 does not. Getting this backwards shifts every application by one row and silently changes the total — which is why the {{c3::2nd and 3rd rows}} are the pair a grader feeds you.

## zh
当规则在「该组合的第 3 笔及其后每一笔」上触发时，计数器要在判断**之前**递增，{{c1::使当前这一行被计入}}：滚动计数为 {{c2::3}} 的那一行是第一个触发的，计数为 2 的那一行不触发。搞反了会让每次应用都错开一行并悄悄改变总数 —— 这就是评测机专挑 {{c3::第 2 行和第 3 行}} 喂给你的原因。
