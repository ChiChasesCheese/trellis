---
slug: minimum-health-to-beat-game
---
## Q
**LC 2214 通关游戏所需的最低生命值**｜Medium

按顺序过 `n` 关，第 `i` 关扣 `damage[i]`，全程生命值要大于 `0`；护甲可在某一关抵消至多 `armor` 点伤害，用一次。求最低初始生命值。

## A
**一句话。** 不用护甲需要 `sum + 1`；护甲抵消 `min(armor, 该关伤害)`，用在伤害最大的那关抵消最多。

```python
def minimum_health(damage, armor):
    saved = min(armor, max(damage))   # 护甲用在最痛的一关
    return sum(damage) - saved + 1    # 最后至少剩 1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 忘了 `+1`：生命值要始终大于 `0`，扣完总伤害后还得剩 `1`。
- 直接减 `armor`：伤害比护甲小时只能抵消伤害本身。

**追问。**
- 为什么用在伤害最大的一关？：抵消量 `min(armor, d)` 随 `d` 不减，放在最大的 `d` 上抵消最多。
- 护甲能用 `m` 次？：选伤害最大的 `m` 关，每关抵消 `min(armor, d)`。

**同模式。** LC 1413 逐步求和得到正数的最小值、LC 134 加油站
