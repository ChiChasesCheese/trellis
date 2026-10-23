---
id: hl-cx-qa-nlogn-vs-n2
node: foundations.complexity
type: qa
step: 43
---
## Q
追问：n 是 10⁶，选 O(n log n) 还是 O(n²)？

## A
推荐答法：「n² 是 10¹² 次，按 10⁸ 次/秒要三个小时，不行；n log n 约 2 × 10⁷，百毫秒量级，可以。」

先把 n 代入算出具体步数，再除以每秒步数，用数字说话，而不是只说「n log n 更快」。
