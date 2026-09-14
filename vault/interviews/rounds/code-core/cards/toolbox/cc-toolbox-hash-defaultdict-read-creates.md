---
id: cc-toolbox-hash-defaultdict-read-creates
node: toolbox.hash
type: cloze
---
`d = defaultdict(list)` turns a *read* into a write: after `if d[k]:` the key {{c1::exists, holding an empty list}}, so a later `len(d)` or an iteration over `d` sees a phantom entry. Use {{c2::`d.get(k)`}} to look without creating, `d.setdefault(k, [])` when you want the plain-dict version of the same insert, and keep `defaultdict` for the pure accumulate loop {{c3::`d[k].append(v)`}}. `Counter` is the exception — `c[missing]` returns {{c4::0 without inserting}}.

## zh
`d = defaultdict(list)` 会把一次*读*变成写：执行 `if d[k]:` 之后这个 key {{c1::已经存在，值是一个空 list}}，于是后面的 `len(d)` 或对 `d` 的遍历会看到一个幽灵条目。想查而不创建就用 {{c2::`d.get(k)`}}，想要同样插入的普通 dict 写法就用 `d.setdefault(k, [])`，把 `defaultdict` 留给纯累加循环 {{c3::`d[k].append(v)`}}。`Counter` 是例外 —— `c[missing]` 返回 {{c4::0 且不插入}}。
