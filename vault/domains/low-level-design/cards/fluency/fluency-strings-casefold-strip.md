---
id: fluency-strings-casefold-strip
node: fluency.strings-bytes
type: qa
step: 3
---
## Q
屏蔽词列表里有 `"Straße"`，用户内容里写了 `"STRASSE"`；配置里还可能混进 `" "`。比较时用 `lower()` 还是 `casefold()`？`strip()` 在哪里用、在哪里不能用？

## A
**忽略大小写用 casefold，裁剪只用在配置**

- **`casefold()` 为比较而设计**：`"ß".casefold()` 是 `"ss"`，`"STRASSE".casefold()` 与它相等；`lower()` 只做小写，`"ß".lower()` 还是 `"ß"`；词尾的希腊字母 `Σ`，`lower()` 变 `ς`，`casefold()` 变 `σ`；
- **折叠会改变长度**：`"İ".casefold()` 是两个码点，所以不要假设折叠前后下标对得上；折叠串里的下标不能当成原文里的位置用；
- **规范化配置，不改用户内容**：关键词 `strip().casefold()` 后去重；用户的内容只 `casefold` 来比较，不 `strip`，原文保留；
- **空串是任何串的子串**：`"" in "abc"` 为 `True`；关键词 strip 后为空就是非法配置，不拒绝的话它会命中所有内容；
- **`strip()` 的字符表是 Unicode 空白**：包括 ` `、`　`，不包括零宽空格 `​`；别的语言的 `trim` 字符表不同，边界上要对齐；
- **字面子串不是整词**：`"ass" in "class"` 为 `True`；要整词得用正则的词边界，这是产品选择，不是实现细节。

```python
def keyword(raw: str) -> str:
    k = raw.strip().casefold()
    if not k:
        raise ValueError("empty keyword")       # "" 会命中一切
    return k

def hit(text: str, kw: str) -> bool:
    return kw in text.casefold()                # 内容只折叠，不 strip

print("ß".lower(), "ß".casefold(), hit("STRASSE", keyword(" Straße ")))   # ß ss True
print("ass" in "class", repr("　x​".strip()))                     # True 'x​'
```

**知识点：**字符串与字节（Strings & Bytes）
