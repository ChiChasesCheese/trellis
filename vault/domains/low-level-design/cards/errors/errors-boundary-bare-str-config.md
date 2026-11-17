---
id: errors-boundary-bare-str-config
node: errors.boundary-validation
type: qa
step: 7
---
## Q
构造函数接收一个“关键词列表”配置，调用方误传了单个字符串 `"spam"`，`for w in words: 校验(w)` 为什么没报错？应该怎么挡？

## A
**先查整体形状，再查每个元素**

- **`str` 本身可迭代**：`list("spam")` 是 `['s', 'p', 'a', 'm']`，每个字符都是合法的非空 `str`，黑名单悄悄变成四个单字母；
- **`bytes` 迭代出的是 `int`**：更晚才炸，错误离原因更远；
- **做法**：先拒绝 `str`/`bytes`，再 `list(x)` 读成快照，最后逐个校验元素；
- **快照**：校验的和保存的是同一份，调用方事后改原列表影响不了服务；一次性迭代器也只迭代一次；
- **元素的空串**：`"" in "任何文本"` 恒为 `True`，空关键词会命中所有内容。

```python
def parse_words(words) -> tuple[str, ...]:
    if isinstance(words, (str, bytes)):
        raise ValueError("pass a list of words, not one string")
    items = list(words)                          # 快照，迭代器只读一次
    for w in items:
        if not isinstance(w, str) or not w.strip():
            raise ValueError(f"bad entry: {w!r}")
    return tuple(items)

print(parse_words(["spam", "ads"]))
```

<details class="pt"><summary>延伸</summary>

`None`、整数这类不可迭代的配置，合同没写时要在动手前问清：本实现归入“非法输入”比让 `list(None)` 抛出的 `TypeError` 更稳，错误类型和别的校验失败一致。

</details>

**知识点：**边界校验（Validate at the Boundary）
