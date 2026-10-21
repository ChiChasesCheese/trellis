---
id: amz-dns-resolver-ttl-lazy-and-active-expiry
node: amazon.amz-dns-resolver
type: qa
step: 3
tags: [grown]
---
## Q
在 DNS 解析器设计里，缓存过期为什么要同时做惰性过期和主动过期？

## A
惰性过期：读到时才检查 `expires <= now`，过期就当没有并删除，保证读到的数据永远正确。但从此再也没人查的域名会永久占着内存，所以还要主动过期：一个按过期时间排序的最小堆，后台线程定期弹出到期项删除。惰性保证正确，主动保证内存有界，两者缺一不可。时钟用单调时钟并注入。
```python
def get(self, name):
    entry = self._data.get(name)
    if entry is None:
        return None
    if entry.expires <= self._clock():
        del self._data[name]
        return None
    return entry.record
```
