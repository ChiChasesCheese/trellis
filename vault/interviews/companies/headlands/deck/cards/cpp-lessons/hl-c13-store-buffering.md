---
id: hl-c13-store-buffering
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 10
---
## Q
什么是 store-buffering 实验？T1 `x=1; r1=y;`、T2 `y=1; r2=x;`，`relaxed` 和 `seq_cst` 下 `r1==0 && r2==0` 各出现多少轮？

## A
- 顺序一致性下 `r1==0 && r2==0` **不可能**出现；放松后两个线程的 store 都可能还留在**存储缓冲**里，各自读到对方的旧值 0。
- 实测 20 万轮：`memory_order_relaxed` 下 **199774** 轮出现两个 0，`seq_cst` 下 **0** 轮。
- 教训：没有同步的「我先写了所以你应该能看到」是错的；**默认用 `seq_cst`，有测量证据再降级**。
