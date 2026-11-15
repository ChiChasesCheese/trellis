---
slug: cracking-the-safe
---
## Q
**LC 753 破解保险箱**｜Hard

密码是 `n` 位、每位取 `0..k-1`，保险箱只看最后输入的 `n` 位。求一个最短的输入串，保证其中出现所有可能的密码。

## A
**一句话。** 以 `n-1` 位串为点，每个 `n` 位密码是一条边（点 + 一位数字），每条边恰走一次就是欧拉回路（de Bruijn 序列），长度 `k^n + n - 1`。

```python
def crack_safe(n, k):
    seen, out = set(), []
    def dfs(node):               # node：最后 n-1 位
        for d in map(str, range(k)):
            code = node + d      # 一条边 = 一个密码
            if code not in seen:
                seen.add(code)
                dfs(code[1:])
                out.append(d)    # 后序记录这条边
    start = "0" * (n - 1)
    dfs(start)
    return start + "".join(reversed(out))
```

**复杂度。** 时间 `O(n·k^n)`，空间 `O(n·k^n)`。

**易错点。**
- 把密码当点、做哈密顿路径：那是 NP 难的搜索，换成「密码当边」才是欧拉回路。
- 先序记录数字：遇到提前回到起点的子环时顺序会错，要后序收集再反转。
- 递归深度可达 `k^n = 4096`：超过 CPython 默认的 1000，要调高上限或改显式栈。

**追问。**
- 为什么一定有欧拉回路？：每个点入度、出度都是 `k`，且图强连通。
- 为什么最短是 `k^n + n - 1`？：每多输入一位最多多出一个新密码，前 `n-1` 位凑不出完整密码。

**同模式。** LC 332 重新安排行程、LC 2097 合法重新排列数对
