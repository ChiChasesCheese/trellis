---
slug: count-zero-request-servers
---
## Q
**LC 2747 统计没有收到请求的服务器数目**｜Medium

`n` 台服务器，`logs[i] = [id, time]` 是请求记录。对每个查询 `q`，求闭区间 `[q - x, q]` 内没有收到请求的服务器数。

## A
**一句话。** 日志和查询都按时间排序（离线），双指针维护时间窗口，计数表统计窗口内有请求的服务器数 `busy`，答案 `n - busy`。

```python
def count_servers(n, logs, x, queries):
    logs = sorted(logs, key=lambda l: l[1])
    order = sorted(range(len(queries)),
                   key=lambda i: queries[i])
    cnt = [0] * (n + 1)      # 服务器在窗口内的请求数
    busy = left = right = 0
    ans = [0] * len(queries)
    for i in order:
        q = queries[i]
        while right < len(logs) and logs[right][1] <= q:
            s = logs[right][0]
            if cnt[s] == 0:
                busy += 1
            cnt[s] += 1
            right += 1
        while left < right and logs[left][1] < q - x:
            s = logs[left][0]
            cnt[s] -= 1
            if cnt[s] == 0:
                busy -= 1
            left += 1
        ans[i] = n - busy    # 写回原下标
    return ans
```

**复杂度。** 时间 `O(m log m + q log q)`，空间 `O(n + q)`。

**易错点。**
- 左端用 `<= q - x` 出窗口：恰在左端点的请求被丢掉，`x=2, queries=[3,4]` 得 `[2, 2]`，应为 `[0, 1]`。
- 按排序后顺序直接 `append`：忘了写回原下标，`[11,10]` 得 `[1, 2]`，应为 `[2, 1]`。

**追问。**
- 为什么要离线排序？：查询有序后窗口两端只右移，指针总共移动 `O(m)` 次。

**同模式。** LC 1851 包含每个查询的最小区间、LC 1697 检查边长度限制的路径是否存在、LC 2070 每一个查询的最大美丽值、LC 438 找到字符串中所有字母异位词
