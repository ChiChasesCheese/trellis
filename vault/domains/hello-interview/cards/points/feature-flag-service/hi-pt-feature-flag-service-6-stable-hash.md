---
id: hi-pt-feature-flag-service-6-stable-hash
node: qb.sd.feature-flag-service.points
type: qa
step: 5
---
## Q
**功能开关服务 · 百分比灰度的稳定哈希**｜必会 · 出自：功能开关服务 › 深入 1

百分比灰度怎么给用户分配？随机数、存储每个用户结果、稳定哈希三种方案各有什么问题？稳定哈希怎么算？

## A
**对比。** 随机数使同一用户时开时关，不可用；存储每个用户结果的表太大，规则一改要迁移。
**选用。** 对 `开关key + 盐 + 用户ID` 做哈希（如 SHA-1 取前 4 字节），对 10000 取模得桶号 0 到 9999，桶号小于百分比 × 100 即命中。无状态、可复现、各 SDK 一致。
```python
h = hashlib.sha1(f"{flag_key}.{salt}.{user_id}".encode()).digest()
b = int.from_bytes(h[:4], "big") % 10000
```
