---
slug: amazon-rate-limiter
---
## Q
**多粒度滑动窗口限流**｜Medium

实现 `allow(request, now)`：`rules` 给每个粒度（如 `ip`、`user`）一个上限「`window` 秒内至多 `limit` 次」，所有粒度都没超才放行；被拒的请求不占任何粒度的额度。

## A
**一句话。** 每个 `(粒度, key)` 一个 `deque`，只存放行过的时间戳：先弹掉过期的，所有粒度都 `len < limit` 才统一记下本次时间。

```python
class RateLimiter:
    def __init__(self, rules):  # {粒度: (limit, window)}
        self.rules = rules
        self.logs = defaultdict(deque)

    def allow(self, request, now):
        hit = []
        for name, (limit, window) in self.rules.items():
            if name not in request:
                continue
            log = self.logs[name, request[name]]
            while log and log[0] <= now - window:
                log.popleft()   # 窗口左开右闭
            if len(log) >= limit:
                return False    # 一处超限，哪都不记
            hit.append(log)
        for log in hit:         # 全部通过再统一记录
            log.append(now)
        return True
```

**复杂度。** 时间 `allow` 均摊 `O(粒度数)`，空间 `O(活跃 key × limit)`。

**易错点。**
- 边检查边记录：`ip` 通过先记了一次，`user` 超限被拒，`ip` 的额度白白被占。
- 弹出条件写成 `<`：`limit = 2, window = 10` 时 `t = 0, 1, 10` 第三个应放行，却因为 `0` 还在窗口里被拒。

**追问。**
- 每个 key 存 `limit` 个时间戳太多？：滑动窗口计数器：只存当前桶和上一桶两个整数，估计 `prev × (1 - 已过比例) + cur`，近似但 `O(1)`。
- 多台机器？：Redis sorted set 加 Lua 脚本一次完成弹出、计数和写入；热点 key 本地预取一批额度。

**同模式。** LC 933 最近的请求次数、LC 359 日志速率限制器、LC 362 敲击计数器
