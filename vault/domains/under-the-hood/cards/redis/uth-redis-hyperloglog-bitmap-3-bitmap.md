---
id: uth-redis-hyperloglog-bitmap-3-bitmap
node: redis.hyperloglog-bitmap
type: qa
step: 3
---
## Q
**用一个字符串怎么做签到统计**｜Redis · Bitmap

`SETBIT` / `BITCOUNT` 底下是什么？一亿用户的签到要多少内存？

## A
**结构。** 位图（bitmap）不是独立类型，就是普通字符串，第 0 位是第一个字节的最高位。

**细节。**

- 一个用户一位：一亿用户约 12.5MB；`BITCOUNT` 统计当天签到人数
- 偏移上限 2³²−1，所以字符串最大 512MB
- `BITCOUNT`：CPU 有 `POPCNT` 指令就一次数 64 位；否则用 `0x55555555`、`0x33333333`、`0x0F0F0F0F` 三步位运算折叠

**为什么。** 一位表示一个状态，空间最小，`BITOP` 还能直接求交并集。

**坑。** 第一次对很大的偏移 `SETBIT`，要一次分配前面全部内存，可能卡住服务器。

**对应 LeetCode：** LC 191 位 1 的个数 · LC 338 比特位计数
