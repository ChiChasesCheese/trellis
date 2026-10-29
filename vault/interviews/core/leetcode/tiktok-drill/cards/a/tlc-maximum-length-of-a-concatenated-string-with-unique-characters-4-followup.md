---
id: tlc-maximum-length-of-a-concatenated-string-with-unique-characters-4-followup
node: a.maximum-length-of-a-concatenated-string-with-unique-characters
type: qa
step: 4
---
## Q
**LC 1239 串联字符串的最大长度**｜追问

面试官接着问：（1）要返回具体拼出的那个字符串？（2）用回溯写，怎么剪枝？（3）`arr` 的长度增大到 `30`、字母仍是 26 个，还能不能做？分别怎么答。

## A
1. **返回字符串**：把 `masks` 换成字典 `dict[int, str]`，键是掩码，值是拼出的字符串；合并时 `table[m | cur] = table[m] + s`，同时用 `max(table.values(), key=len)` 取最长。同一个掩码可能由不同选法得到，保留任意一个即可，因为长度相同。
2. **回溯 + 剪枝**：

```python
def max_length_dfs(arr: list[str]) -> int:
    masks: list[int] = []
    for s in arr:
        if len(set(s)) == len(s):
            masks.append(sum(1 << (ord(ch) - 97) for ch in s))
    suffix = [0] * (len(masks) + 1)                     # suffix[i]：从 i 往后所有串的位数之和（乐观上界）
    for i in range(len(masks) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + masks[i].bit_count()
    best = 0

    def dfs(i: int, mask: int) -> None:
        nonlocal best
        best = max(best, mask.bit_count())
        if i == len(masks) or mask.bit_count() + suffix[i] <= best:   # 剪枝：再怎么选也超不过已知最优
            return
        if mask & masks[i] == 0:
            dfs(i + 1, mask | masks[i])                  # 选第 i 个
        dfs(i + 1, mask)                                 # 不选

    dfs(0, 0)
    return best
```

   `["un","iq","ue"]` → `4`，`["cha","r","act","ers"]` → `6`。剪枝用「当前位数加上后面所有串位数之和」当上界，上界不超过已知最优就不再往下。
3. **`n = 30`**：`2^30` 个子集不能枚举，但字母只有 26 个，任何合法选择的掩码最多 26 位，选出的串最多 26 个。回溯加上面的剪枝通常能跑得动；最坏情况仍是指数级，面试里说明这个限制即可。

**Python 提醒**：`nonlocal best` 让内部函数修改外层变量；如果漏掉，`best = max(best, ...)` 会把 `best` 当成内部的局部变量，抛 `UnboundLocalError`。
