---
id: hi-pt-battleship-game-design-2-reverse-index
node: qb.lld.battleship-game-design.points
type: qa
step: 2
---
## Q
**海战棋 · 反查表与派生沉没**｜必会 · 出自：海战棋 › 深入 2

开火时要找出被打的是哪艘船，以及这炮是否打沉了它。数据怎么放，才既快又不会失同步？

## A
**反查表。** 每个 `_Side` 有 `at: dict[Cell, _Ship]`，格子到船的映射，开火是一次字典查询。扫描全部船的全部格子是 O(舰队格数)，每炮都付一遍。

**派生状态。** 船自己记 `hits`，`sunk` 现算，不另存布尔：另存就要在每次命中时同步，漏一处就出现"打满了却没沉"。

```python
@property
def sunk(self) -> bool:
    return len(self.hits) == len(self.cells)
```
