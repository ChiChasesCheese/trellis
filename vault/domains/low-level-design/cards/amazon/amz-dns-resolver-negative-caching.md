---
id: amz-dns-resolver-negative-caching
node: amazon.amz-dns-resolver
type: qa
step: 6
tags: [grown]
---
## Q
在 DNS 解析器设计里，查询不存在的域名（NXDOMAIN）为什么也要缓存？哪些失败不该缓存？

## A
不缓存的话，对不存在域名的重复查询（拼写错误、扫描器）每次都打到上游。负缓存用较短的 TTL（如 30 秒）。缓存值要用哨兵对象区分「查过且不存在」和「没查过」，否则 `None` 有歧义。上游超时、服务器故障不能缓存：否则一次短暂故障会被放大成整个 TTL 长度的故障。
```python
_MISS = object()

def lookup(self, name):
    hit = self._cache.get(name, _MISS)
    if hit is NXDOMAIN:
        raise NameNotFound(name)
    if hit is not _MISS:
        return hit
    try:
        rec = self._resolve_upstream(name)
    except NameNotFound:
        self._cache.put(name, NXDOMAIN, self.neg_ttl)
        raise
    self._cache.put(name, rec, rec.ttl)
    return rec
```
