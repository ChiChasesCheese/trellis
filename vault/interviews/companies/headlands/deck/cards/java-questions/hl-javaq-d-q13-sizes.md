---
id: hl-javaq-d-q13-sizes
node: java-questions.d-memory
type: qa
step: 11
---
## Q
64 位 HotSpot 上这些对象各占多少字节：`new Object()`、`record P2(int,int)`、`record P3(long,long,long)`、`Integer`、`new int[0]`、`new int[10]`、`new long[10]`、`new Integer[10]`？

## A
- `new Object()`：**16**（12 头 + 4 填充）。
- `record P2(int,int)`：**24**（12 + 8 = 20，对齐到 24）。
- `record P3(long,long,long)`：**40**（12 + 24 = 36，对齐到 40）。
- `Integer.valueOf(1000)`：**16**（12 + 4）。
- `new int[0]`：**16**（数组头）。
- `new int[10]`：**56**（16 + 40）。
- `new long[10]`：**96**（16 + 80）。
- `new Integer[10]`：**56**（16 + 10 个 4 字节引用，不含 `Integer` 对象本身）。
- 推论：`ArrayList<Integer>` 100 万元素 ≈ 4 MB 引用数组 + 16 MB `Integer` 对象 ≈ 20 MB（20,000,208 字节），`int[]` 才 4 MB。
