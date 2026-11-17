---
id: fluency-strings-bare-str-config
node: fluency.strings-bytes
type: qa
step: 4
---
## Q
`BlocklistService(keywords="spam")` 本该传列表 `["spam"]`。构造函数里写了 `{k.casefold() for k in keywords}`，测试没挂，上线后为什么所有含 `s`、`p`、`a`、`m` 的内容都被屏蔽了？该怎么防？

## A
**str 本身是可迭代的，边界先拒绝裸 str**

- **根因**：`str` 是字符序列，遍历一个 `str` 得到单个字符；`"spam"` 悄悄变成 `{"s","p","a","m"}`，类型检查看不出问题，因为它仍然是“可迭代的 str”；
- **`bytes` 同理**：遍历 `bytes` 得到 `int`，后面 `.casefold()` 才报 `AttributeError`，离出错的地方已经很远；
- **做法**：在构造函数的边界先 `isinstance(keywords, (str, bytes))` 就拒绝，再接受别的可迭代容器；然后一次性转成 `tuple` 快照；
- **元素也要检查**：每个元素必须是 `str`；空白条目 strip 后为空也要拒绝（空串是任何内容的子串）；
- **同样的坑出现在任何“接受列表”的参数上**：`set("abc")`、`list("abc")`、`",".join("abc")`、`"x" in "xyz"` 都把 `str` 当序列。

```python
def parse_keywords(keywords) -> tuple[str, ...]:
    if isinstance(keywords, (str, bytes)):
        raise TypeError("keywords must be a collection of str, not a bare str")
    items = tuple(keywords)                      # 快照：生成器只能读一次
    if not all(type(k) is str and k.strip() for k in items):
        raise ValueError("keywords must be non-blank str")
    return tuple(k.strip().casefold() for k in items)

print(parse_keywords(["Spam", " Eggs "]))        # ('spam', 'eggs')
print(set("spam"))                               # {'s','p','a','m'}：不拒绝就是这样
try: parse_keywords("spam")
except TypeError as e: print(e)
```

**知识点：**字符串与字节（Strings & Bytes）
