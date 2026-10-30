---
id: tlc-longest-duplicate-substring-2-code
node: p4.longest-duplicate-substring
type: qa
step: 2
---
## Q
**LC 1044 最长重复子串**｜写出 Python 实现

小写字母字符串 `s`（长度 `2` 到 `3 * 10^4`）。重复子串是在 `s` 中出现至少两次的连续子串，两次出现可以重叠。返回任意一个最长的重复子串，没有则返回 `""`。要求 `O(n log n)`。

## A
**思路。** 外层二分长度 `L`：`find(L)` 用滚动哈希扫描所有长度 `L` 的窗口，哈希表记录每个哈希值出现过的起点；遇到相同哈希且真实子串也相同，就返回当前起点。有解则尝试更长（`lo = mid + 1`），无解则变短。

```python
import random


def longest_dup_substring(s: str) -> str:
    n = len(s)
    nums = [ord(c) - 96 for c in s]        # 'a'..'z' -> 1..26
    mod = (1 << 61) - 1
    base = random.randrange(1 << 20, mod)  # 随机底数：防止被构造数据卡哈希

    def find(length: int) -> int:          # 返回某个长度为 length 的重复子串的起点，没有则 -1
        top = pow(base, length, mod)       # base^length，用来滚掉最左边的字符
        h = 0
        for x in nums[:length]:
            h = (h * base + x) % mod
        seen = {h: [0]}                    # 哈希 -> 起点列表（链式，应对碰撞）
        for i in range(1, n - length + 1):
            h = (h * base - nums[i - 1] * top + nums[i + length - 1]) % mod
            for j in seen.get(h, ()):
                if s[j:j + length] == s[i:i + length]:     # 哈希相同再逐字比对，杜绝假阳性
                    return i
            seen.setdefault(h, []).append(i)
        return -1

    lo, hi, start = 1, n - 1, -1           # 答案长度在 [0, n-1]；"有长度 L 的重复" 对 L 单调
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if (idx := find(mid)) != -1:
            start, best, lo = idx, mid, mid + 1
        else:
            hi = mid - 1
    return s[start:start + best] if best else ""
```

运行：`"banana"` → `'ana'`，`"abcd"` → `''`，`"aa"` → `'a'`，`"aaa"` → `'aa'`；`"a" * 30000` → 长度 `29999` 的子串。

**复杂度。** 时间 `O(n log n)`（期望）：二分约 `15` 轮，每轮扫描 `O(n)`，哈希命中时才做 `O(L)` 的比对；空间 `O(n)`：`nums` 与哈希表。

**写法要点。** `pow(base, length, mod)` 是三参数快速幂，`O(log L)`；哈希表值用列表，同一个哈希挂多个起点，碰撞时不会漏掉真正相同的那个；海象运算符 `(idx := find(mid)) != -1` 把调用和判断合成一步，并保留结果供下一行使用；`seen.get(h, ())` 对不存在的键返回空元组，循环自然为空，比先判断 `in` 更简洁。
