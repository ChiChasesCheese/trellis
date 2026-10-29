---
id: uth-redis-streams-geo-3-geo
node: redis.streams-geo
type: qa
step: 3
---
## Q
**GEO 附近的人怎么查**｜Redis · 8.10

`GEOADD` / `GEOSEARCH` 没有单独的结构，底下是什么？

## A
**背景。** “附近的人”是二维问题：要找某个点周围一定半径内的所有点。而有序集合（ZSET）只会按一个数排序、取一段区间。办法：把二维的经纬度压成一个数（geohash），让地理上靠近的点，数也靠近。

**结构。** 就是 ZSET：经纬度编码成 52 位 geohash 整数，当作分数，成员名是地点。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">经纬度的二进制位交错拼成 52 位整数</text>
<rect x="10" y="26" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="33" y="47.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<rect x="60" y="26" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="83" y="47.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<rect x="110" y="26" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="133" y="47.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<rect x="10" y="66" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="33" y="87.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<rect x="60" y="66" width="46" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="83" y="87.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">中心</text>
<rect x="110" y="66" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="133" y="87.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<rect x="10" y="106" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="33" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<rect x="60" y="106" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="83" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<rect x="110" y="106" width="46" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="133" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">邻</text>
<text x="180" y="50" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">中心格子 + 8 个邻居</text>
<text x="180" y="68" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">= 9 个分数区间</text>
<text x="180" y="90" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个区间做范围查找,</text>
<text x="180" y="106" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再用真实距离过滤</text>
<text x="8" y="160" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">底下就是 ZSET: 分数 = geohash, 成员 = 地点名</text>
<text x="8" y="178" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">纬度限制在 ±85.05112878</text>
<text x="8" y="196" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">地理上相邻的两点 geohash 可能差很远, 所以要查邻居格</text>
</svg>
```

**细节。**

- geohash 把经度、纬度的二进制位交错拼接，附近的点分数大多相近；纬度限制在 ±85.05112878
- 查询按半径选精度，取中心格子加 8 个邻居格子，共 9 个分数区间
- 对每个区间做范围查找，再用真实距离过滤

**为什么。** 复用 ZSET 的范围查询；二维问题变成一维区间。

**坑。** 地理上相邻的两点 geohash 可能差很远，所以要查邻居格子。

**对应 LeetCode：** 无直接对应的题（空间索引）
