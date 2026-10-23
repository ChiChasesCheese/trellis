---
id: hl-cache-pointer-chasing-ladder
node: foundations.cpu-cache-locality
type: qa
step: 5
---
## Q
指针追逐（pointer chasing）实验怎么测出真实访问延迟？Apple Silicon 上工作集从 4 KB 增大到 256 MB，每次读取耗时怎么变？

## A
做法：建大小为 W 的 `int[] next`，内容是随机的单圈排列，反复执行 `p = next[p]`。每次读取依赖上一次结果，CPU 无法并行或预取，测得时间就是**真实的单次访问延迟**。

实测（缓存行 128 B）：
- 工作集 ≤ 64 KB：1.26 ns/load（全在 L1）；
- 256 KB：2.20 ns；1 MB：2.84 ns；4 MB：5.56 ns；16 MB：7.19 ns（L2 区间 2–7 ns）；
- 64 MB：**51.35 ns**；256 MB：**78.60 ns**（真正的 DRAM + TLB 缺失）。

L1 到主存延迟差约 60 倍。数字随机器变，阶梯**形状**不变。
