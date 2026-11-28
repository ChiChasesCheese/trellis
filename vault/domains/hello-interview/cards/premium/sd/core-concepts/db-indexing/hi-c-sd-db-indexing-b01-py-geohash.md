---
id: hi-c-sd-db-indexing-b01-py-geohash
node: sd.core-concepts.db-indexing.beyond
type: qa
step: 1
---
## Q
**数据库索引 · 动手实现 geohash**｜拓展 · 加分
geohash 的编码到底怎么做？为什么交错经纬度二进制位就能保留邻近性？

## A
**模式。** 二分逼近加比特交错。
```python
_B32 = "0123456789bcdefghjkmnpqrstuvwxyz"


def geohash(lat: float, lon: float, precision: int = 6) -> str:
    lat_lo, lat_hi, lon_lo, lon_hi = -90.0, 90.0, -180.0, 180.0
    bits = bit_count = 0
    even, out = True, []              # 偶数位切经度，奇数位切纬度，交错
    while len(out) < precision:
        lo, hi, v = (lon_lo, lon_hi, lon) if even else (lat_lo, lat_hi, lat)
        mid = (lo + hi) / 2
        bit = v >= mid                # 在上半区记 1，下半区记 0，并缩小区间
        bits = bits * 2 + bit
        if even:
            lon_lo, lon_hi = (mid, hi) if bit else (lo, mid)
        else:
            lat_lo, lat_hi = (mid, hi) if bit else (lo, mid)
        even = not even
        bit_count += 1
        if bit_count == 5:            # 每 5 个比特编成一个 base32 字符
            out.append(_B32[bits])
            bits = bit_count = 0
    return "".join(out)


print(geohash(37.7749, -122.4194, 6))   # 9q8yyk，旧金山市中心
```
- **为什么保留邻近：** 每个比特把区域对半切，前 k 个比特相同就表示落在同一个 2^k 分之一的矩形里，所以前缀越长格子越小；前缀相同的点一定相近。
- **反过来不成立：** 近的点前缀不一定相同（跨越格子边界时），这就是要查相邻 8 格的原因。
- **精度换算：** 每个字符 5 比特，多一个字符格子面积缩小到约 1/32。
- **并行思路：** 这种把多维映射到一维有序值的做法称为空间填充曲线（Z 序曲线）；Hilbert 曲线的局部性更好，但计算更复杂（S2、H3 是其他常见方案，分别基于球面曲线和六边形网格）。
