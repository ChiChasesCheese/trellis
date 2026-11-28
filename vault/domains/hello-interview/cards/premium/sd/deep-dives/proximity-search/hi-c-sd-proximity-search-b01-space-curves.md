---
id: hi-c-sd-proximity-search-b01-space-curves
node: sd.deep-dives.proximity-search.beyond
type: qa
step: 1
---
## Q
**邻近搜索 · 空间填充曲线：Z 序、Hilbert 与 geohash 的实现**｜拓展 · 加分

geohash 的前缀为什么对应一块区域？它有什么不连续？S2 用的曲线有什么不同？

## A
**模式。** 空间填充曲线：把二维坐标交错成一维键，保持局部性。
```python
B32 = "0123456789bcdefghjkmnpqrstuvwxyz"

def geohash(lat: float, lon: float, n: int) -> str:
    lat_lo, lat_hi, lon_lo, lon_hi = -90.0, 90.0, -180.0, 180.0
    out, bits, ch, even = [], 0, 0, True        # 偶数位切经度，奇数位切纬度，交错成 Z 序
    while len(out) < n:
        lo, hi, v = (lon_lo, lon_hi, lon) if even else (lat_lo, lat_hi, lat)
        mid = (lo + hi) / 2
        bit = 1 if v >= mid else 0               # 落在上半区记 1，下半区记 0
        ch = ch * 2 + bit
        if even: lon_lo, lon_hi = (mid, hi) if bit else (lo, mid)
        else:    lat_lo, lat_hi = (mid, hi) if bit else (lo, mid)
        even = not even
        bits += 1
        if bits == 5:                            # 每 5 比特映射成一个字符
            out.append(B32[ch]); bits = ch = 0
    return "".join(out)

print(geohash(40.7128, -74.0060, 7))             # dr5regw
```
- **为什么前缀是区域：** 每一位都是对某个方向的二分，前 k 位固定了一个矩形；这样的前缀在字符串里是连续的一段，所以前缀扫描就是一次范围查询。
- **不连续（Z 序的跳跃）：** 交错比特的曲线在某些位置会"跳"，地图上相邻的两格在一维键上可能相隔很远，这就是边界陷阱的根源，也是需要 3x3 的原因。
- **Hilbert 曲线：** S2 用的是 Hilbert 曲线，跳跃更少、局部性更好，一个区域能被更少的连续区间覆盖；代价是计算比简单交错比特复杂。
- **何时不用：** 查询经常是任意多边形、要精确几何时，直接用 R 树。
