---
slug: string-without-aaa-or-bbb
---
## Q
**LC 984 不含 AAA 或 BBB 的字符串**｜Medium

给 `a`、`b`，构造一个含恰好 `a` 个 `'a'`、`b` 个 `'b'` 的字符串，且不含子串 `"aaa"` 和 `"bbb"`（保证有解）。

## A
**一句话。** 贪心：每步放剩余更多的字母，但若末尾已经连着两个相同字母，就必须放另一个。

```python
def str_without_3a3b(a, b):
    ans = []
    while a or b:
        if len(ans) >= 2 and ans[-1] == ans[-2]:
            put_a = ans[-1] == "b"      # 已连两个：必须换字母
        else:
            put_a = a >= b              # 否则放剩得多的
        if put_a:
            ans.append("a")
            a -= 1
        else:
            ans.append("b")
            b -= 1
    return "".join(ans)
```

**复杂度。** 时间 `O(a + b)`，空间 `O(a + b)`。

**易错点。**
- 一直放多的字母：会出现 `aaa`，连着两个后必须强制换字母。
- 两者相等时随便放：应固定一个，且让 `a >= b` 时放 `a`，否则放 `b`，行为才稳定。

**追问。**
- 为什么放多的是对的？：少的字母要用来隔开多的，多的消耗得越快，隔开的位置越够。
- 有解的条件是什么？：`max(a, b) <= 2 · (min(a, b) + 1)`。

**同模式。** LC 1405 最长快乐字符串、LC 767 重构字符串、LC 621 任务调度器
