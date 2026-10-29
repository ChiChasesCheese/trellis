---
id: tlc-longest-happy-string-2-code
node: a.longest-happy-string
type: qa
step: 2
---
## Q
**LC 1405 最长快乐字符串**｜写出 Python 实现

三个整数 `a`、`b`、`c`（`0..100`，不全为 0）。用最多 `a` 个 `'a'`、`b` 个 `'b'`、`c` 个 `'c'` 构造尽可能长的字符串，要求不含 `aaa`、`bbb`、`ccc`（同一字母不能连续三个）。返回任意一个最长的。

## A
**思路。** 用一个最大堆保存「剩余个数最多的字母」。每轮取出最多的那个：如果结果末尾已经连着两个它，就改放次多的字母（取出、放一个、有剩余就放回），再把最多的放回堆；否则直接放它，有剩余就放回。堆空或没有字母可垫时结束。

```python
def longest_diverse_string(a: int, b: int, c: int) -> str:
    # 最大堆（用负数模拟）：(-剩余个数, 字母)；个数为 0 的字母不入堆
    heap = [(-n, ch) for n, ch in ((a, "a"), (b, "b"), (c, "c")) if n]
    heapq.heapify(heap)
    out: list[str] = []
    while heap:
        n, ch = heapq.heappop(heap)                    # 剩余最多的字母
        if out[-2:] == [ch, ch]:                       # 末尾已经连着两个 ch，不能再放
            if not heap:
                break                                  # 没有别的字母可垫：只能结束
            n2, ch2 = heapq.heappop(heap)              # 垫一个次多的字母
            out.append(ch2)
            if n2 + 1:
                heapq.heappush(heap, (n2 + 1, ch2))
            heapq.heappush(heap, (n, ch))              # 最多的字母原样放回
        else:
            out.append(ch)
            if n + 1:
                heapq.heappush(heap, (n + 1, ch))
    return "".join(out)
```

运行：`a=1, b=1, c=7` → `'ccaccbcc'`，`a=2, b=2, c=1` → `'ababc'`，`a=7, b=1, c=0` → `'aabaa'`，`a=0, b=0, c=1` → `'c'`，`a=0, b=0, c=5（只有一种字母）` → `'cc'`，`a=100, b=100, c=100 的长度` → `300`。

**复杂度。** 时间 `O(N log 3) = O(N)`，`N = a + b + c` 是总字符数：每放一个字符做常数次对大小为 `≤ 3` 的堆的操作；空间 `O(N)`（输出）+ `O(1)`（堆）。

**写法要点。** `heapq` 是最小堆，所以存 `(-个数, 字母)`，弹出的就是剩余最多的；`out[-2:] == [ch, ch]` 用切片一次判断「末尾连着两个 `ch`」，长度不足 2 时切片也安全，不会越界；`(-n, ch)` 元组在个数相同时按字母排序，结果确定；入堆前用 `if n` 过滤零个数；放回时 `n + 1` 非零才推（因为 `n` 是负数，加一是少一个）。
