---
id: pl-data-strings-pitfall-length
node: data.strings-text
type: qa
step: 11
---
## Q
「字符串长度」在四门语言里的答案为什么不同？按长度截断用户昵称时，具体会出什么事故？

## A
同一个字符串 `"a😀é"`，四门语言给出不同的长度（真实输出）：

| 语言 | 表达式 | 结果 |
|---|---|---|
| Java | `s.length()` | 4（UTF-16 单元） |
| Go | `len(s)` | 7（UTF-8 字节） |
| Rust | `s.len()` | 7（UTF-8 字节） |
| Python | `len(s)` | 3（码点） |

用户看到的是 3 个字符，国旗 `🇯🇵` 和 `👨‍👩‍👧` 则在 Python 里分别是 2 和 5。

**典型事故：截断昵称**。产品要求「昵称最多显示 10 个字符」，代码写成按位置截取。

```java
String h = "😀".substring(0, 1);
// h.length()=1, Character.isSurrogate(h.charAt(0))=true
// bytes when written out as UTF-8: '?'  (lone surrogate cannot be encoded)
```

截断在 emoji 的两个代理单元之间，得到一个孤立代理，编码成 UTF-8 时被替换为 `?`，用户看到乱码。Rust 同样的操作是 panic（`not a char boundary`），Go 则会得到一个非法 UTF-8 字节序列，下游 JSON 序列化会把它变成 `U+FFFD`。

**更隐蔽的版本**：数据库列是 `VARCHAR(10)`（按字节或按码点取决于数据库），应用层按字符数校验，结果在包含中文或 emoji 的输入上截断或报错，只在海外用户出现。

**防线**：明确长度的单位（协议约束用字节，展示用字形簇）；用库按字形簇截断；测试用例必须包含 emoji、组合字符和一个汉字。
