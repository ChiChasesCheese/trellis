---
id: hl-cx-estimate-treemap
node: foundations.complexity
type: qa
step: 34
---
## Q
估算：一百万个订单各做一次 `TreeMap.put`，要多久？写出估算过程。

## A
- n = 10⁶，每次 O(log n)，log₂ 10⁶ ≈ 20 层。
- 理论 10⁶ × 20 = 2 × 10⁷ 步，按 10⁸ 步/秒 → **0.2 秒**。
- 校对实测：239 ns × 10⁶ = 0.24 秒，吻合。

结论：约 0.2–0.3 秒，可接受。
