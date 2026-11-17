---
id: parsing-io-tokenizer-scanner
node: parsing-io.tokenizer
type: qa
step: 1
---
## Q
要给 `12 + 3*(4)` 这样的表达式写解析器，为什么先把字符串切成 token，而不是直接在字符上解析？tokenizer 怎样处理空白和不认识的字符？

## A
**词法与语法分两层，token 带类型和位置**

- **分工**：tokenizer 回答「这一段字符是什么」（数字、运算符、括号）；解析器回答「这些 token 怎么组合」；各管一层，规则都变简单；
- **token 带三样东西**：类型、原文、起始位置；位置用来报错（第几列），原文用来转数字；
- **空白**：匹配后丢弃，不产生 token；
- **兜底分支**：最后放一个匹配任意单个字符的分支，遇到不认识的字符时抛出错误并带位置；没有兜底，`finditer` 会悄悄跳过它；
- **最长匹配**：模式里先写长的再写短的（`<=` 先于 `<`），否则短的会先吃掉前缀。

```python
import re
from typing import NamedTuple

class Tok(NamedTuple): kind: str; text: str; pos: int
SPEC = re.compile(r"(?P<NUM>[0-9]+)|(?P<OP>[-+*/()])|(?P<WS>[ \t]+)|(?P<BAD>.)")

def tokenize(s: str):
    for m in SPEC.finditer(s):
        if m.lastgroup == "WS": continue
        if m.lastgroup == "BAD": raise ValueError(f"bad char {m.group()!r} at {m.start()}")
        yield Tok(m.lastgroup, m.group(), m.start())

print([t.text for t in tokenize("12 + 3*(4)")])    # ['12', '+', '3', '*', '(', '4', ')']
```

**知识点：**词法分析（Tokenizer）
