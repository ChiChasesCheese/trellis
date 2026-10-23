---
id: hl-cq-q38-branch-prediction
node: cpp-questions.i-low-latency
type: qa
step: 12
---
## Q
面试题：什么是分支预测？在代码里怎么体现？
What is branch prediction? How does it show up in code?

## A
- CPU 流水线要提前取指，遇到分支就**猜**走哪边；猜对几乎免费，猜错要清空流水线，代价约**十几到二十个周期**。
- 分支可预测（几乎总是同一方向，或有规律的模式）时成本接近 0；**随机、数据相关的 50/50 分支**才是问题。
- 对策：让数据有序（分支变得可预测）；改写成**无分支**（条件移动 / 算术）；把罕见路径移出热路径。
- 验证：Linux 上用 `perf stat -e branches,branch-misses`，不要猜。
