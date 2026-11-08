---
id: hi-pt-tt-billing-tax-engine-4-publish-append
node: tt.lld.tt-billing-tax-engine.points
type: qa
step: 4
---
## Q
**计费与计税引擎 · 版本只追加**｜必会 · 出自：计费与计税引擎 › 整体设计

计费引擎发布新规则版本时，为什么要求生效时间严格大于上一个版本？想修正历史定价怎么办？

## A
**要点。** 这保证 starts 永远升序，二分才成立。
**修正历史。** 不改旧版本，而是发布新版本，并对受影响交易写调整行。
**并发。** 发布时构造新列表再替换引用，读路径拿不可变元组，不需要锁。
