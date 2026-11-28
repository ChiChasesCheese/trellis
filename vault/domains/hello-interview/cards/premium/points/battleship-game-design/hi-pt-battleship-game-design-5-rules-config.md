---
id: hi-pt-battleship-game-design-5-rules-config
node: qb.lld.battleship-game-design.points
type: qa
step: 5
---
## Q
**海战棋 · 规则用配置不用子类**｜追问 · 出自：海战棋 › 深入 4

要加三种玩法变体：船不许相邻、命中后连击、每回合齐射，而且玩法能自由组合。用子类还是用配置？`Rules` 怎么写？

## A
**用配置。** 三个布尔开关组合出 2^3 = 8 种玩法，用子类要写 8 个或多重继承；配置对象一个就够。

**写法。** 不可变数据类，传进 `Game` 后外面改不了，`slots` 去掉每个实例的 `__dict__`。默认值等于前面的规则，旧行为不变（不可变配置对象）。

```python
@dataclass(frozen=True, slots=True)
class Rules:
    touching_allowed: bool = True
    extra_turn_on_hit: bool = False
```
