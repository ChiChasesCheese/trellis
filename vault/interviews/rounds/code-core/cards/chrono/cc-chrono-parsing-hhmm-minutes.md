---
id: cc-chrono-parsing-hhmm-minutes
node: chrono.parsing
type: cloze
---
`HH:MM` becomes a comparable integer with {{c1::`h, m = map(int, s.split(":")); minutes = h * 60 + m`}} — no `datetime` needed. A UTC offset given in decimal hours must go the same way: `+5.5` is {{c2::330}} minutes and `+5.75` is {{c3::345}}, obtained once as `round(float(off) * 60)`, so that {{c4::no float hours ever reach the arithmetic}}.

## zh
`HH:MM` 用 {{c1::`h, m = map(int, s.split(":")); minutes = h * 60 + m`}} 就变成可比较的整数 —— 不需要 `datetime`。以小数小时给出的 UTC offset 也照此处理：`+5.5` 是 {{c2::330}} 分钟，`+5.75` 是 {{c3::345}}，用 `round(float(off) * 60)` 一次算出，这样 {{c4::浮点小时永远不会进入后续算术}}。
