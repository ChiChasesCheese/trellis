---
id: amz-dns-resolver-upstream-health-and-failover
node: amazon.amz-dns-resolver
type: qa
step: 4
tags: [grown]
---
## Q
在 DNS 解析器设计里，上游超时后怎样自动切换到备用上游，又不会每次请求都先去试已经挂掉的那个？

## A
每个上游记连续失败次数：失败 3 次就标为不健康，冷却 30 秒内直接跳过；冷却结束后放一个请求过去试探（半开，half-open），成功就恢复，失败就继续冷却。`resolve` 按顺序遍历健康上游，全部失败时可以返回已过期的缓存（serve stale）而不是报错。
```python
def resolve(self, name):
    for up in self._upstreams:
        if not up.healthy(self._clock()):
            continue
        try:
            rec = up.resolve(name)
            up.ok()
            return rec
        except TimeoutError:
            up.fail(self._clock())
    raise ResolveError(name)
```
