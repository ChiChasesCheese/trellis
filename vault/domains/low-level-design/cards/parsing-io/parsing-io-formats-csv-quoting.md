---
id: parsing-io-formats-csv-quoting
node: parsing-io.formats
type: qa
step: 1
---
## Q
读一个导出的 CSV，用 `line.split(",")` 解析，遇到备注 `"hello, world"` 或跨两行的备注就出错。为什么？该用什么，写文件时又要注意什么？

## A
**用 `csv` 模块，文件以 `newline=""` 打开**

- **引号规则**：字段里有逗号、引号、换行时要用引号包起来，引号本身写成两个引号；`split` 不认识这些；
- **跨行的字段**：一条记录可以占多行，按行读文件再 `split` 一定切坏；`csv.reader` 从整个文件对象里读，自己决定一条记录到哪里结束；
- **`newline=""`**：打开文件时必须加，否则文本层先把 `\r\n` 换成 `\n`，引号内部的换行被改写，记录内容变了；
- **`DictReader`**：用表头当键，字段多了少了都能看出来；列数不对的行要自己处理（缺的列是 `None`，多的列放在 `None` 键下）；
- **写**：`csv.writer` 自动加引号，不要自己拼字符串。

```python
import csv, io

raw = 'id,note\n1,"hello, world"\n2,"line1\nline2"\n3,"say ""hi"""\n'
print(raw.splitlines()[1].split(","))                    # ['1', '"hello', ' world"']：切坏了
rows = list(csv.DictReader(io.StringIO(raw, newline="")))
print(rows[0]["note"], repr(rows[1]["note"]), rows[2]["note"])   # hello, world 'line1\nline2' say "hi"
out = io.StringIO(); csv.writer(out, lineterminator="\n").writerow(["4", 'a,"b"'])
print(out.getvalue(), end="")                            # 4,"a,""b"""
```

**知识点：**CSV 与 JSON 的稳健读写（CSV & JSON）
