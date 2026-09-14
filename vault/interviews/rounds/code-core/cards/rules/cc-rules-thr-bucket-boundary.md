---
id: cc-rules-thr-bucket-boundary
node: rules.thresholds
type: qa
---
## Q
A percentage rollout puts a user in bucket `h = hash(flag, user) % 100` and enables the feature when the bucket is in the rollout. Write the comparison and check both ends.

## A
**`enabled = h < rollout`.**

- `rollout = 0` → no bucket satisfies `h < 0` → nobody, which is what "0%" must mean.
- `rollout = 100` → every bucket 0–99 satisfies `h < 100` → everybody.
- A user in bucket 54 is **off** at `rollout = 54` and **on** at 55.

`h <= rollout` breaks both ends: 0% would enable bucket 0, and the population would be 101 buckets wide. The general check for any "x% of N" rule: verify that 0 gives none and the maximum gives all before trusting the middle.

## Q zh
百分比灰度把用户放进桶 `h = hash(flag, user) % 100`，当桶落在灰度范围内时开启功能。写出这个比较并检查两端。

## A zh
**`enabled = h < rollout`。**

- `rollout = 0` → 没有桶满足 `h < 0` → 没有人，这正是"0%"必须表达的意思。
- `rollout = 100` → 0–99 全部满足 `h < 100` → 所有人。
- 位于桶 54 的用户在 `rollout = 54` 时**关闭**，在 55 时**开启**。

`h <= rollout` 两端都错：0% 会放行桶 0，而人群宽度会变成 101 个桶。任何"N 中取 x%"规则的通用检查：先确认 0 给出零人、最大值给出全部，再去相信中间值。
