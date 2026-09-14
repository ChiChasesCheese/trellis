---
id: cc-python-idioms-fstring-format
node: python.idioms
type: cloze
---
The four format specs worth knowing cold: two decimals {{c1::f"{x:.2f}"}}, zero-padded to width five {{c2::f"{n:05d}"}}, right-aligned in eight columns {{c3::f"{s:>8}"}}, thousands separators {{c4::f"{n:,}"}}. The same mini-language works in `format(x, ".2f")` and `"{:.2f}".format(x)`, and `f"{val=}"` prints `val=<value>` for a one-keystroke debug line.

## zh
四个必须烂熟于心的格式说明符：两位小数 {{c1::f"{x:.2f}"}}、补零到宽度五 {{c2::f"{n:05d}"}}、右对齐到八列 {{c3::f"{s:>8}"}}、千位分隔符 {{c4::f"{n:,}"}}。同一套迷你语言在 `format(x, ".2f")` 和 `"{:.2f}".format(x)` 里同样有效，而 `f"{val=}"` 会打印 `val=<value>`，是最省键的调试行。
