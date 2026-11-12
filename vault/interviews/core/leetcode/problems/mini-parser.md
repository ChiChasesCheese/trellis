---
slug: mini-parser
---
## Q
**LC 385 迷你语法分析器**｜Medium

把表示嵌套整数列表的字符串 `s`（如 `"[123,[456,[789]]]"`）解析成 `NestedInteger`。

## A
**一句话。** 正则切成 `[`、`]`、整数三种记号，共享迭代器做递归下降。

```python
def deserialize(s):
    tokens = iter(re.findall(r"\[|\]|-?\d+", s))

    def parse(tok):
        if tok != "[":
            return NestedInteger(int(tok))
        lst = NestedInteger()
        for nxt in tokens:       # 共享迭代器 = 读指针
            if nxt == "]":
                break
            lst.add(parse(nxt))
        return lst

    return parse(next(tokens))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 逐字符处理数字：`"[123,-4]"` 变成 `[1,2,3,4]`，多位数被拆、负号丢失。
- 每层递归新建迭代器：`"[[1]]"` 每次从头读，永远读不完。
- 嵌套深度可达约 `25000`：超过默认递归上限，要调高或改显式栈。

**追问。**
- 显式栈怎么写？：遇 `[` 压新列表，整数加进栈顶，遇 `]` 弹出并加进新栈顶；整串只是一个整数要单独先处理。
- 反过来序列化？：递归拼接，整数输出数字，列表输出 `"[" + ",".join(...) + "]"`。

**同模式。** LC 394 字符串解码、LC 224 基本计算器、LC 339 嵌套列表加权和、LC 341 扁平化嵌套列表迭代器
