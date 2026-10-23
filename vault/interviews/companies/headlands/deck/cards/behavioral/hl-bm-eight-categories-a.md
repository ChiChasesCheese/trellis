---
id: hl-bm-eight-categories-a
node: behavioral.method
type: qa
step: 6
---
## Q
Headlands 的背景问题分八类。前四类（简历深挖、为什么交易/Headlands/离开、最难的 bug、性能问题）各自真正在探什么？首选哪个故事？

## A
- **简历深挖** → 你说的每个词能不能被追问三层 → 首选 **S1**（结算管线）。
- **为什么交易 / 为什么 Headlands / 为什么离开** → 你是不是真的好奇，而不是追薪水 → **R1**（个人研究平台 Quant-Stroller）。
- **最难的 bug** → 定位的**方法**，是否往下一层走 → **S3**（无报错的 NULL bug）、**S8**（Terraform 7 分钟根因）。
- **性能问题** → 测过吗？是哪一层？ → **S6**（上线前容量推理）、**S5**（窗口化 `ON`）。
