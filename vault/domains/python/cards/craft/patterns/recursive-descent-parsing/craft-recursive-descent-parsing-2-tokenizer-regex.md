---
id: craft-recursive-descent-parsing-2-tokenizer-regex
node: craft.patterns.recursive-descent-parsing
type: qa
step: 2
---
## Q
**递归下降解析 · 分词（tokenize）为什么不能 split，运算符为什么要长的在前**｜模式

查询条件 `name = 'a AND b' AND age <= 3` 要先切成 token（词法单元），再交给解析器。`text.split()` 一行就能切，为什么不够？换成正则以后，`<=` 和 `<` 谁写在前面，会有什么后果？

## A
**要点。** 词法要识别的是「字符串字面量」「多字符运算符」「标识符」这些单位，空白只是其中一种分隔。`split()` 把引号里的空格也当分隔，`'a AND b'` 被拆成三块，解析器会把里面的 `AND` 当成关键字。正则从当前位置匹配一个 token，匹配不上就当场报位置，错误不会拖到解析阶段才以奇怪的形式出现。

```python
import re

# 长运算符写前面，否则 <= 会被切成 < 和 =；引号内的整段算一个 token
_TOKEN = re.compile(r"\s*(<=|>=|!=|=|<|>|\(|\)|,|'[^']*'|-?\d+|[A-Za-z_][\w.]*)")

def tokenize(text):
    tokens, pos, text = [], 0, text.rstrip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)           # 只在 pos 处匹配，不跳着找
        if not m: raise ValueError(f"无法识别: {text[pos:]!r}")
        tokens.append(m.group(1)); pos = m.end()
    return tokens

q = "name = 'a AND b' AND age <= 3"
print("split :", q.split())
print("正则  :", tokenize(q))
bad = re.compile(r"\s*(<|>|=|<=|>=|!=)")      # 把短的写在前面
print("短运算符在前:", [bad.match(s, 0).group(1) for s in ["<=", ">=", "!="]], "（期望 <=  >=  !=）")
```

实际输出：

```
split : ['name', '=', "'a", 'AND', "b'", 'AND', 'age', '<=', '3']
正则  : ['name', '=', "'a AND b'", 'AND', 'age', '<=', '3']
短运算符在前: ['<', '>', '!='] （期望 <=  >=  !=）
```

**为什么。** 正则的 `|` 是按书写顺序试，第一个能匹配的分支就胜出，不会回头找最长的。`<` 写在 `<=` 前面，`<=` 永远只被读成 `<`，剩下的 `=` 变成下一个 token，报错信息还指向错误的位置。最后一个例子里 `!=` 能正确匹配，是因为它没有更短的前缀。

**易错。** `\s*` 放在每个 token 前面而不是 `split` 在前：空白只在 token 之间被吃掉，引号内的空白被整个 `'[^']*'` 分支保留。字符串里要转义引号（SQL 的 `''`）时，这个分支要换成能识别转义的写法。
