---
slug: longest-happy-string
---
## Q
**LC 1405 最长快乐字符串**｜Medium

用最多 `a` 个 `a`、`b` 个 `b`、`c` 个 `c` 拼出最长的、不含 `aaa`、`bbb`、`ccc` 的字符串。

## A
**一句话。** 贪心加最大堆：每次放剩余最多的字母，若它已连放两个，就先垫一个次多的。

```python
def longest_diverse_string(a, b, c):
    cnt = ((a, "a"), (b, "b"), (c, "c"))
    heap = [(-n, ch) for n, ch in cnt if n]  # 负数模拟大根堆
    heapq.heapify(heap)          # 0 个的不入堆
    out = []
    while heap:
        n, ch = heapq.heappop(heap)
        if out[-2:] == [ch, ch]: # 末尾已连两个，不能再放
            if not heap:
                break            # 没有别的可垫，结束
            n2, ch2 = heapq.heappop(heap)
            out.append(ch2)      # 垫一个次多的
            if n2 + 1:
                heapq.heappush(heap, (n2 + 1, ch2))
            heapq.heappush(heap, (n, ch))   # 最多的放回
        else:
            out.append(ch)
            if n + 1:
                heapq.heappush(heap, (n + 1, ch))
    return "".join(out)
```

**复杂度。** 时间 `O(N)`，空间 `O(N)`（输出）。

**易错点。**
- 不限制连续个数：`a=1,b=1,c=7` 得 `ccccccabc`，含 `ccc`。
- 碰到上限就结束：上限只表示这步不能放它，`1,1,7` 只得 `cc`，应有 8 个字符。
- 垫完忘了把最多的放回堆：`1,1,7` 只得 `ccab`。

**追问。**
- 推广到 `k` 种字母、连续上限 `r`？：同一思路，末尾已连 `r` 个时改取次多的，堆操作 `O(log k)`。
- 相邻必须不同、且要用完（LC 767）？：每步取最多的但不能是刚放过的，最多的超过 `⌈N/2⌉` 则无解。

**同模式。** LC 767 重构字符串、LC 984 不含 AAA 或 BBB 的字符串、LC 621 任务调度器、LC 1054 距离相等的条形码
