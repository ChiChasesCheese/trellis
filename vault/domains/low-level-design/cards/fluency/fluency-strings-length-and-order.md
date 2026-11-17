---
id: fluency-strings-length-and-order
node: fluency.strings-bytes
type: qa
step: 2
---
## Q
名字规则是“1 到 80 个字符”。`len("😀")`、`len("é")`、`len("😀".encode())` 各是多少？校验长度、比较两个名字、给名字排序时，分别按什么算？

## A
**`len(str)` 数码点，不数字节也不数字形**

- **`len(s)` 是码点数（code point）**：`len("😀")` 为 1；同一个 `"é"` 可以是 1 个码点（NFC），也可以是 `e` 加组合符号共 2 个码点（NFD），两者看起来一样，`==` 却是 `False`；
- **字节数是另一回事**：`len(s.encode("utf-8"))` 里 `"😀"` 是 4；数据库列按字节限长就要这样量；JavaScript 按 UTF-16 码元数，`"😀"` 是 2，对端的“80 个字符”和你的不是一个数；合同要写明单位；
- **要把看起来相同的名字当同一个**：先 `unicodedata.normalize("NFC", s)` 再比较；合同如果没要求就不要悄悄规范化，原样存；
- **排序按码点**：`sorted` 比的是码点，大写在小写前（`"B" < "a"`），带重音的字母排在 `z` 之后，这恰好等于 UTF-8 字节序；要按语言习惯排序得用 `locale` 或 ICU，不是 `sorted` 的事；
- **`str` 排序不是 `Path` 排序**：路径对象按路径段比较，`str(path)` 按字符比较，两者对 `a.txt` 与 `a/b` 的先后不同，说好用哪个。

```python
import unicodedata
nfc, nfd = "é", unicodedata.normalize("NFD", "é")
print(len(nfc), len(nfd), nfc == nfd)                       # 1 2 False
print(nfc == unicodedata.normalize("NFC", nfd))             # True
print(len("😀"), len("😀".encode()), len("😀".encode("utf-16-le")) // 2)   # 1 4 2
print(sorted(["a", "B", "é", "Z"]))                         # ['B', 'Z', 'a', 'é']
```

**知识点：**字符串与字节（Strings & Bytes）
