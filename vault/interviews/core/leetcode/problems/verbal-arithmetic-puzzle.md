---
slug: verbal-arithmetic-puzzle
---
## Q
**LC 1307 口算难题**｜Hard

`words` 与 `result` 是由大写字母组成的字符串，给每个字母分配一个不同的数字 `0-9`，使 `words` 的数值之和等于 `result`，且多位数没有前导零。判断是否可解。

## A
**一句话。** 把每个字母的权重算出来（单词里的字母取 `+10^位`，结果里的取 `-10^位`），问题变成：给字母分配互不相同的数字，使 `Σ 权重 × 数字 = 0`，回溯搜索。

```python
def is_solvable(words, result):
    weight = Counter()
    for w in words:
        for k, c in enumerate(reversed(w)):
            weight[c] += 10 ** k            # 加数：正权重
    for k, c in enumerate(reversed(result)):
        weight[c] -= 10 ** k                # 结果：移到左边变负
    if len(weight) > 10:
        return False
    letters = list(weight)
    lead = {w[0] for w in words + [result] if len(w) > 1}
    used = [False] * 10
    def dfs(i, total):
        if i == len(letters):
            return total == 0
        c = letters[i]
        for d in range(10):
            if used[d] or (d == 0 and c in lead):
                continue                    # 数字已用 / 前导零
            used[d] = True
            if dfs(i + 1, total + weight[c] * d):
                return True
            used[d] = False
        return False
    return dfs(0, 0)
```

**复杂度。** 时间 最坏 `O(10!)`，空间 `O(10)`。

**易错点。**
- 逐列带进位搜索：可以，但实现麻烦；权重法把所有列合成一个等式，更好写。
- 单个字母的单词当成前导零：一位数 `0` 是合法的，只有长度大于 1 的才禁止首位为 `0`。
- 字母超过 10 个没有直接返回：数字只有 10 个，必然无解。

**追问。**
- 如何剪枝？：每层记录剩余字母权重的上下界，若 `total` 已不可能回到 `0` 就提前返回。
- 为什么权重法正确？：十进制按位展开后，等式两边相减恰是每个字母的数字乘以它在所有位置上的 `10^位` 之和。

**同模式。** LC 1255 得分最高的单词集合、LC 282 给表达式添加运算符、LC 37 解数独
