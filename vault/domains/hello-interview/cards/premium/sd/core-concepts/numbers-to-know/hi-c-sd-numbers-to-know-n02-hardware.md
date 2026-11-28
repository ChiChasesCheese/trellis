---
id: hi-c-sd-numbers-to-know-n02-hardware
node: sd.core-concepts.numbers-to-know.notes
type: qa
step: 2
---
## Q
**必知数字 · 现代硬件的上限**｜摘要 · 必会
一台现代云服务器的内存、存储、网络大约是什么量级？这对架构意味着什么？

## A
- **内存与 CPU：** AWS M6i.32xlarge 有 512 GiB 内存、128 vCPU；内存优化型 X1e.32xlarge 有 4 TB 内存，U-24tb1.metal 可达 24 TB。很多以前必须分布式的应用现在一台机器就能装下。
- **存储：** i3en.24xlarge 带 60 TB 本地 SSD；D3en.12xlarge 带 336 TB 机械盘；S3 这类对象存储实际上无限，PB 级是常态。存储不再是首要约束。
- **网络：** 数据中心内标准实例 25 Gbps，高性能实例 50-100 Gbps 以上。延迟可预测：同一可用区（AZ）内低于 1 毫秒，同一区域内跨可用区 1-2 毫秒，跨区域 50-150 毫秒。
- **含义：** 教科书里"数据库超过 100 GB 就拆""别把大对象放内存"是过时的约束，这是一次阶跃式的变化。
