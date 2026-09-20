---
id: problems-cricinfo-ball-outcome-properties
node: problems.games.cricinfo
type: qa
step: 2
tags: [grown]
---
## Q
体育比分系统设计里，wide、no ball、bye、leg bye 这四种额外球，对“算不算合法球”“记不记到击球手个人得分”“记不记到投手失分”这三件事的回答两两不同，为什么把这套规则做成 `BallOutcome` 上的几个只读属性，而不是直接写在重放循环里的一串 `if`？

## A
写在重放循环里，这套判断只在一个地方生效——`Innings.record` 要不要用同一套逻辑校验、测试要不要单独断言这几条规则，都得重新写一遍判断。做成 `BallOutcome` 的只读属性（`is_legal`、`batter_runs`、`team_runs`、`bowler_runs`）之后，重放函数只管调用它们，完全不知道 wide 和 no ball 的区别；规则变了（比如某联赛把 no ball 的判罚改成 2 分）只改 `BallOutcome` 一处，重放逻辑一行不动，任何调用方读到的都是同一套规则，不会出现两处判断不一致的风险。
