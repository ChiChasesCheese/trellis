---
slug: split-array-into-fibonacci-sequence
---
## Q
**LC 842 将数组拆分成斐波那契序列**｜Medium

数字字符串 `num`，拆成至少 3 个非负整数，每个不含前导零（`0` 本身可以）、都不超过 `2^31 - 1`，且 `f[i] + f[i+1] = f[i+2]`。返回任意一种拆法，没有返回 `[]`。

## A
**一句话。** 回溯枚举每一段的长度；前两段确定后后面的值被唯一确定，不符就剪枝，超过和就停止加长。

```python
def split_into_fibonacci(num):
    ans = []
    def dfs(i):
        if i == len(num):
            return len(ans) >= 3
        for j in range(i + 1, len(num) + 1):
            if num[i] == "0" and j > i + 1:
                break                  # 前导零：只能单独一个 0
            x = int(num[i:j])
            if x >= 2 ** 31:
                break
            if len(ans) >= 2:
                s = ans[-1] + ans[-2]
                if x > s:
                    break              # 再加长只会更大
                if x < s:
                    continue
            ans.append(x)
            if dfs(j):
                return True
            ans.pop()
        return False
    return ans if dfs(0) else []
```

**复杂度。** 时间 `O(n²)`（前两段枚举后后续唯一），空间 `O(n)`。

**易错点。**
- 前导零判断漏掉：`"01"` 不是合法的数，`"0"` 才是。
- 不限制 `2^31 - 1`：数字过长时 `int` 很大，既慢又不合法。
- 超过和之后仍继续加长：只会更大，应 `break`。

**追问。**
- 为什么复杂度近似平方？：前两段长度确定，后面每段长度由和唯一决定，不再分叉。

**同模式。** LC 306 累加数、LC 93 复原 IP 地址、LC 131 分割回文串
