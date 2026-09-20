---
id: problems-cricinfo-format-is-one-number
node: problems.games.cricinfo
type: qa
step: 8
tags: [grown]
---
## Q
体育比分系统设计里，从 T20 换成 ODI、再到不限 over 数的 Test 赛制，分别要改动几处代码，这说明了这个设计的什么性质？

## A
只需要在 `MatchFormat` 枚举和 `OVERS_PER_INNINGS` 这张映射表里加一行——`Match.start_innings` 不用改一个字符，`Innings`、`derive_innings_state`、改判逻辑全部不知道自己所属的赛制限定几个 over。两局制的 Test 也不是新代码，只是多调用几次 `start_innings`。这说明赛制差异被完全限制在“一局限定几个 over”这一个数字里，其余全部规则（记分、额外球、轮转、改判）与赛制无关，是“加需求不碰老代码”这条验收标准的一个直接证据。
