---
id: foundations-storage-estimate-method
node: foundations.estimation
type: qa
---
## Q
Estimate storage for 100M-DAU Twitter-like service, 2 tweets/user/day, ~1 KB/tweet (skip media), 5-year retention. Walk the math.

## A
- Writes/day: 100M × 2 = **2 × 10⁸ tweets/day**
- Data/day: 2 × 10⁸ × 1 KB = **200 GB/day**
- 5 years ≈ 2,000 days → **~400 TB** raw; ×3 replication → **~1.2 PB**

Keep every input a round power of ten and state units at each step — the method is the signal, not decimal precision.


## Q zh
估算一个 1 亿 DAU 的 Twitter 类服务的存储需求：每用户每天 2 条推文，每条约 1 KB（忽略媒体），保留 5 年。走一遍这个数学过程。

## A zh
- 每天写入量：1 亿 × 2 = **2 × 10⁸ 条推文/天**
- 每天数据量：2 × 10⁸ × 1 KB = **200 GB/天**
- 5 年 ≈ 2,000 天 → 原始数据约 **400 TB**；× 3 副本 → **约 1.2 PB**

让每一个输入都保持在十的整数次幂，并在每一步都注明单位 — 方法本身才是信号，而不是小数精度。
