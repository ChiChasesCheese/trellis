---
id: hi-c-sd-sharding-b02-py-hash
node: sd.core-concepts.sharding.beyond
type: qa
step: 2
---
## Q
**分片 · Python 里别用内置 hash 做分片路由**｜拓展 · 加分
在 Python 里写 `hash(user_id) % n` 做路由，哪里会出问题？该怎么写？

## A
**模式。** 稳定哈希：路由用跨进程、跨语言都一致的哈希函数。
```python
import hashlib


def shard_of(key: str, n_shards: int) -> int:
    # 内置 hash(str) 每个进程随机加盐（PYTHONHASHSEED），
    # 两台机器、或同一台重启后，对同一个键会算出不同分片。
    digest = hashlib.md5(key.encode()).digest()   # 不是为了安全，只要稳定
    return int.from_bytes(digest[:8], "big") % n_shards


assert shard_of("user:42", 64) == shard_of("user:42", 64)
```
- **问题本质：** 字符串和字节串的 `hash()` 为了防哈希碰撞攻击而随机加盐，仅保证进程内一致。拿它路由，各服务实例的分片判断就互相矛盾，数据写进 A 却到 B 去读。
- **整数的 `hash(42)` 是 42：** 开发时碰巧正常，换成字符串键才暴露，这类 bug 在测试环境不易重现。
- **选择：** 要稳定、均匀、快，不要求密码学安全。常见选择是 MurmurHash、xxHash（需第三方库）；标准库里 `hashlib` 的 MD5/SHA-1 更慢但稳定且随处可用。取模前取足够多的位，避免低位偏斜。
- **何时不用：** 单进程内的字典、集合，内置 `hash` 正合适。
