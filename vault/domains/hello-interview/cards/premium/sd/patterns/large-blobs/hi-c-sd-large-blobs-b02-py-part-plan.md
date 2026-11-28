---
id: hi-c-sd-large-blobs-b02-py-part-plan
node: sd.patterns.large-blobs.beyond
type: qa
step: 2
---
## Q
**大文件 · Python：分块大小怎么算**｜拓展 · 加分

S3 分段上传的块数和块大小有哪些硬限制，客户端怎么规划与续传？

## A
```python
import math

MIN_PART = 5 * 1024**2     # S3：除最后一块外，每块至少 5 MiB
MAX_PARTS = 10_000         # S3：一个对象最多 10000 块

def plan_parts(size: int, preferred: int = 16 * 1024**2) -> list[tuple[int, int]]:
    # 块大小取三者最大：偏好值、下限、以及不超过 10000 块所需的最小块
    part = max(preferred, MIN_PART, math.ceil(size / MAX_PARTS))
    return [(s, min(s + part, size) - 1) for s in range(0, size, part)]   # 闭区间字节范围

def missing(plan: list[tuple[int, int]], done: set[int]) -> list[int]:
    # done 是 ListParts 返回的已成功块号（从 1 起）；只重传缺的
    return [i + 1 for i in range(len(plan)) if i + 1 not in done]
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<g stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="10" y="26" width="72" height="44"/>
<rect x="82" y="26" width="72" height="44"/>
<rect x="226" y="26" width="72" height="44"/>
</g>
<g stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3">
<rect x="154" y="26" width="72" height="44"/>
<rect x="298" y="26" width="32" height="44"/>
</g>
<g font-size="12" font-family="sans-serif" fill="currentColor">
<text x="10" y="16">plan_parts：每块一个字节范围，末块可以更短</text>
<text x="10" y="100">ListParts 返回 {1, 2, 4} → missing() = [3, 5]</text>
<g text-anchor="middle">
<text x="46" y="45">块 1</text><text x="118" y="45">块 2</text><text x="190" y="45">块 3</text><text x="262" y="45">块 4</text><text x="314" y="45">5</text>
<text x="46" y="62">已传</text><text x="118" y="62">已传</text><text x="190" y="62">缺</text><text x="262" y="62">已传</text><text x="314" y="62">缺</text>
</g>
</g>
</svg>

- **块数上限逼出块大小：** 4TiB 的文件要求每块至少约 420MiB，因为 10000 块是硬上限；块大小固定在 5MiB 的实现传不了大文件。
- **块号是幂等的：** 同一块号重传会覆盖，所以续传重复传一块无害。
- **校验和：** 每块的 ETag 要和块号一起交给完成接口；分段对象的最终 ETag 不是整个文件的 MD5，不要拿它做整体校验。
- **2026 亮点：** 整体校验用全对象 CRC64NVME（新版 SDK 默认随上传发送 CRC，服务端独立计算比对并存入对象元数据），而不是分段 ETag；全对象 CRC 可由各块线性组合，不妨碍并行上传。
