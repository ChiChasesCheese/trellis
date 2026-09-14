---
id: cc-verification-determinism-rollout-boundary
node: verification.determinism
type: qa
---
## Q
A feature is enabled for `rollout` percent of users. Write the comparison and defend the boundary.

## A
**`bucket < rollout`, with `bucket` in `0..99`.**

- Strict `<` is the only choice that makes `rollout = 0` mean *nobody* and `rollout = 100` mean *everybody*. With `<=`, a 0 % rollout still enables one percent of your users — a real incident, not a test artefact.
- The bucket must be a stable function of `(flag, user)` and of nothing else, so raising 10 % to 20 % keeps the original users enabled and adds to them, instead of reshuffling everyone ([[cc-verification-determinism-stable-hash]]).
- Test the boundary directly: a user whose bucket equals `rollout` must be **off**, and `rollout + 1` must switch them on ([[cc-verification-edge-exact-threshold-triple]]).

## Q zh
某个功能对 `rollout` 百分比的用户开启。写出比较式，并为边界辩护。

## A zh
**`bucket < rollout`，其中 `bucket` 取值 `0..99`。**

- 严格的 `<` 是唯一能让 `rollout = 0` 表示*没有人*、`rollout = 100` 表示*所有人*的选择。用 `<=` 的话，0% 的灰度仍会给百分之一的用户开启 —— 那是真实事故，不是测试瑕疵。
- 桶必须是 `(flag, user)` 的稳定函数、且不依赖其他任何东西，这样从 10% 提到 20% 是在原有用户之上追加，而不是把所有人重新洗牌（[[cc-verification-determinism-stable-hash]]）。
- 直接测边界：桶值恰好等于 `rollout` 的用户必须是**关**，`rollout + 1` 必须把他打开（[[cc-verification-edge-exact-threshold-triple]]）。
