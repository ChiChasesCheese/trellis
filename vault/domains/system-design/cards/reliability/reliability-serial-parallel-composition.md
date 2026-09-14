---
id: reliability-serial-parallel-composition
node: reliability.availability
type: cloze
---
Components in **series** multiply availabilities: two 99.9% dependencies give {{c1::0.999 × 0.999 ≈ 99.8%}} — every hard dependency subtracts nines. Components in **parallel** (either can serve) give 1 − (1−A)², so two 99.9% replicas yield {{c2::99.9999%}} — assuming truly independent failure modes.

## zh
**序列**中的组件乘以可用性：两个 99.9% 依赖给 {{c1::0.999 × 0.999 ≈ 99.8%}} ——每个硬依赖减法九。**平行**（任一个可以服务）中的组件给 1 − (1−A)²，所以两个 99.9% 副本产生 {{c2::99.9999%}} ——假设真实独立故障模式。
