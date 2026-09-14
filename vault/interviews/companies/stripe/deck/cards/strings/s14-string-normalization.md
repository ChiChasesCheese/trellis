---
id: s14-string-normalization
node: stripe.strings
type: qa
---

## Q
公司名注册、邮箱、语言标签、卡号这些题为什么都要先归一化再比较？归一化函数该怎么写才不出错？

## A
**为什么考**：公司名注册、邮箱、语言标签、卡号 —— 都要先归一化再比较。

**做法：归一化是一个纯函数，在边界调用一次，全程只比较归一化后的值。**

```python
def canonical(name: str) -> str:
    s = name.casefold()                       # 不是 lower()：处理 ß → ss
    s = re.sub(r"[^a-z0-9 ]+", " ", s)        # 标点变空格
    s = re.sub(r"\s+", " ", s).strip()        # 折叠空白
    for suffix in ("inc", "llc", "ltd", "corp"):   # 公司后缀
        if s.endswith(" " + suffix):
            s = s[: -len(suffix) - 1]
    return s
```

**必须留住原文**：输出通常要求原始拼写，归一化的值只做 key。
`registry[canonical(name)] = name`。

**顺序有讲究**：先去标点还是先去后缀？题面的样例决定。`"A.B.C. Inc."` 两种顺序结果不同。
