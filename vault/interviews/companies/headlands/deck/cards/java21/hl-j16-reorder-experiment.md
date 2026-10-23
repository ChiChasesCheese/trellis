---
id: hl-j16-reorder-experiment
node: java21.j16-concurrency-primitives
type: qa
step: 5
---
## Q
重排序实验：线程 1 `x = 1; r1 = y;`，线程 2 `y = 1; r2 = x;`，跑 100 万次，普通字段与 `volatile` 下 `(r1, r2) = (0, 0)` 各出现多少次？

## A
按逐句顺序执行的直觉，`r1`、`r2` 不可能同时为 0。

- 普通字段：100 万次中 `(0,0)` 出现 **977579 次**（另一次 990150 次），几乎每次；
- `volatile`：**0 次**。

原因是写缓冲让「写后读」被重排（StoreLoad）。arm64 内存模型比 x86 弱，所以更夸张，x86 上同样能复现，概率低些。`volatile` 修复可见性，也禁止了这种 StoreLoad 重排。
