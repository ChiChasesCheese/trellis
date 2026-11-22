---
id: aid-property-fuzz
node: t05.fuzzing-property-based-testing
type: qa
step: 1
tags: [摘要]
---
## Q
**Fuzzing 与 property-based testing**｜摘要 · 追问

你有一个解析器，手写的 10 个例子都过了。怎么让 agent 帮你找到你想不到的输入？

## A
| 技术 | 做什么 |
|---|---|
| **property-based testing** | 不写具体例子，写"对任意输入都应成立的性质"（不变量），由库生成大量随机输入去试，失败时缩小到最小反例 |
| **fuzzing** | 向程序喂大量随机或变异的输入，看会不会崩溃、挂起 |

**让模型提出不变量：**

| 解析器的不变量 | 例 |
|---|---|
| 往返 | `parse(serialize(x)) == x` |
| 幂等 | `normalize(normalize(x)) == normalize(x)` |
| 永不崩溃 | 任意字节输入，只会返回错误，不会抛异常 |

```python
@given(st.text())
def test_never_crashes(s):
    parse(s)   # 只允许返回结果或抛 ParseError
```

**做：** 让 agent 提出 5 条不变量，**你筛选**（它可能给错的性质）；让它写输入生成器（strategy）。
**别做：** 直接信任它提出的"性质"，错误的性质会产生假失败，或根本测不到东西。

**出处：** 概念；hypothesis 是 Python 常用的 property-based testing 库
