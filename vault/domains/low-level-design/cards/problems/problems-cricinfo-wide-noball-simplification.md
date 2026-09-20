---
id: problems-cricinfo-wide-noball-simplification
node: problems.games.cricinfo
type: qa
step: 3
tags: [grown]
---
## Q
体育比分系统设计里，wide 和 no ball 都不算合法球，但为什么只有 wide 完全不计入击球手的个人得分，no ball 打出去的分却要正常记给击球手？

## A
两种非法球在这一点上遵守的是不同的真实规则：wide 是投手投得离身太远、击球手根本没有机会正当击球，所以全程不可能有击球手个人得分；no ball 通常是投手脚步犯规，球本身仍然可以被正常击打，击球手打出去的分要照算个人得分，球队只是额外再得 1 分判罚。`BallOutcome` 把“打到球棒上的跑动”（`bat_runs`）和“跟球棒无关的额外跑动”（`extra_runs`）分成两个字段，并在构造时校验哪种额外球允许哪种字段非零——给一次 wide 塞击球手跑动、或者给一次 bye 塞额外跑动，会在构造 `BallOutcome` 时就抛 `InvalidDeliveryError`，而不是悄悄算出一个错误的总分。
