---
id: reliability-burn-rate-alerting
node: reliability.slo
type: qa
---
## Q
Why alert on error-budget burn rate instead of a raw error-rate threshold, and how do multi-window burn alerts work?

## A
A fixed threshold either pages on blips (too sensitive) or sleeps through slow leaks (too dull). **Burn rate** = how many times faster than sustainable you are consuming the budget, which directly maps to "time until SLO is blown."

Standard practice: pair a **fast window** (e.g. 14.4x burn over 1h — 2% of a 30-day budget gone — page now) with a **slow window** (e.g. ~1–2x over days — ticket, not page). Both windows must fire, filtering transient spikes.

## Q zh
为什么要在 error-budget burn rate 上告警而不是原始错误率阈值，多窗口 burn 告警是如何工作的？

## A zh
固定阈值要么对抖动反应过敏（太敏感），要么对缓慢泄露睡大觉（太迟钝）。**Burn rate** = 你消耗预算的速度快于可持续速度多少倍，直接映射到"直到 SLO 被打破还有多少时间"。

标准做法：配对一个**快窗口**（例如 14.4x burn 在 1h——30 天预算的 2%——现在告警）与一个**慢窗口**（例如 ~1–2x 在数天——工单，不告警）。两个窗口都必须触发，过滤瞬间峰值。
