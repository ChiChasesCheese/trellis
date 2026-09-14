---
id: cc-verification-determinism-set-iteration
node: verification.determinism
type: cloze
---
Iterating a `set` yields an order you must never print: it depends on insertion history and on the per-process hash seed. A `dict` has preserved {{c1::insertion}} order since Python 3.7, but that is still an accident of the input rather than a specification of your output — call {{c2::sorted()}} with a complete key before writing anything a grader compares.

## zh
遍历 `set` 得到的顺序绝不能拿去打印：它取决于插入历史和每个进程的哈希种子。`dict` 从 Python 3.7 起保持{{c1::插入}}顺序，但那仍然是输入的偶然产物，而不是你输出的规格 —— 在写出任何会被评测机比对的东西之前，先用完整的键调用 {{c2::sorted()}}。
