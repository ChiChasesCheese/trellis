---
id: cc-output-formatting-minor-units
node: output.formatting
type: cloze
---
For `cents = -350`, `cents // 100` is {{c1::-4}} and `cents % 100` is {{c2::50}}, so the naive `f"{cents//100}.{cents%100:02d}"` prints {{c3::-4.50}} instead of `-3.50` — Python's floor division and modulo do not split a signed amount into sign, whole part and remainder. The fix is to pull the sign out first: {{c4::`sign = "-" if cents < 0 else ""; cents = abs(cents)`}}, then format the magnitude. The `:02d` is what keeps `5` cents printing as {{c5::05}}.

## zh
当 `cents = -350` 时，`cents // 100` 是 {{c1::-4}}、`cents % 100` 是 {{c2::50}}，所以朴素的 `f"{cents//100}.{cents%100:02d}"` 打印出 {{c3::-4.50}} 而不是 `-3.50` —— Python 的向下取整除法和取模不会把带符号金额拆成符号、整数部分和余数。修法是先把符号取出来：{{c4::`sign = "-" if cents < 0 else ""; cents = abs(cents)`}}，再格式化绝对值。`:02d` 正是让 `5` 分打印成 {{c5::05}} 的东西。
