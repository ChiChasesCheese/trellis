---
id: match-tries-patterns-top-to-bottom-first-wins
node: iteration.pattern-matching
type: qa
source: peps
---
## Q
一个 `match` 语句里写了多个 `case`，Python 是怎么决定执行哪一个分支的？`case _:` 放在中间会有什么问题？

## A
`match` 按从上到下的顺序依次尝试每个 `case` 的模式，一旦第一个匹配成功，就执行该分支的代码，后面所有 `case` 都不再检查——这和 `if/elif/elif/...` 的短路顺序完全一样。通配符模式 `_`（wildcard）永远匹配任何对象（不只是序列），所以只有把它放在最后一个 `case` 才有意义；如果放在前面，后面所有 `case` 永远不会被触发到，Python 会在编译期就阻止这种写法。
