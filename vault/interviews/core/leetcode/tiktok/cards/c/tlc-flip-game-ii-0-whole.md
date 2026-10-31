---
id: tlc-flip-game-ii-0-whole
node: c.flip-game-ii
type: qa
---
## Q
**LC 294 翻转游戏 II**｜Medium · LC TikTok 全时段热度 25/100

你和朋友轮流把字符串 `currentState`（只含 `'+'` 和 `'-'`）中**连续**的两个 `"++"` 翻转成 `"--"`，无法进行有效翻转的一方输，双方都采取最优策略。判断起始玩家是否存在必胜策略。`1 <= currentState.length <= 60`，`currentState[i]` 是 `'+'` 或 `'-'`，不会有超过 20 个连续的 `'+'`。例：`"++++"` → `true`（先手翻转中间的 `++` 得到 `+--+`，后手无路可走）；`"+"` → `false`。进阶：推导你算法的时间复杂度。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 极小化极大的博弈搜索：当前局面「必胜」当且仅当存在一步翻转，使对手面对的新局面「必败」；用局面字符串做记忆化。

**识别。** 「两人轮流、双方最优、无法行动者输」的有限博弈：递归定义胜负，再用记忆化去掉重复局面；长度 60、每段 `+` 至多 20，搜索空间可控。

**推导。** 暴力：递归枚举所有走法，不记忆化最坏约 `O(n!!)`（每步至多 `n` 个位置，最多走 `n/2` 步）。浪费：不同的走法顺序会到达同一个局面。洞察：局面只由当前字符串决定，`@cache` 记下每个局面的胜负；局面数等于每段 `+` 里放置互不相交的 `"--"` 的方案数的乘积（斐波那契级增长）。

```python
from functools import cache


def can_win(currentState: str) -> bool:
    @cache
    def win(state: str) -> bool:                 # 轮到的玩家面对 state 时，是否有必胜策略
        for i in range(len(state) - 1):
            if state[i : i + 2] == "++":
                # 翻转这一对后，如果对手面对的新局面必败，我就赢了
                if not win(state[:i] + "--" + state[i + 2 :]):
                    return True
        return False                             # 没有可走的步，或每一步都让对手必胜

    return win(currentState)
```

运行：`"++++"` → `True`；`"+"` → `False`；`"++"` → `True`；`"+++"` → `True`；`"--"` → `False`；单段 `"+" * 20`（允许的最长连续段）→ `True`，记忆化只涉及几千个局面。

**复杂度。** 时间 = 局面数 × 每局面 `O(n)`（枚举位置并拼接字符串）；局面数上界是各段 `+` 内放置不相交 `"--"` 的方案数之积，每段是斐波那契增长，远小于 `2^n`；空间 = 局面数 × `O(n)`。

**拓展优化。**
- 多段 `+` 之间用 `-` 隔开时，整串记忆化的局面数是各段方案数的乘积，会很大；把各段当作独立子游戏时用下面的 SG 值，只需 `O(n^2)`。
- 进阶的更优解：连续的 `+` 段彼此独立，是组合博弈（Sprague–Grundy 定理）：长度 `L` 的段翻转一对后分成长度 `i` 和 `L-2-i` 的两段，SG 值是这些异或值的 mex；多段 SG 值异或，非 0 则先手必胜。时间 `O(n^2)`：

```python
def can_win_grundy(currentState: str) -> bool:
    segments = [len(seg) for seg in currentState.split("-") if len(seg) >= 2]   # 连续 '+' 的段长，彼此独立
    top = max(segments, default=0)
    grundy = [0] * (top + 1)                     # grundy[L]：长度 L 的 '+' 段的 SG 值
    for length in range(2, top + 1):
        reachable = {grundy[i] ^ grundy[length - 2 - i] for i in range(length - 1)}   # 翻转后分成左右两段
        grundy[length] = next(g for g in range(len(reachable) + 1) if g not in reachable)   # mex
    xor = 0
    for length in segments:
        xor ^= grundy[length]                    # 多个独立子游戏：SG 值异或，非 0 先手必胜
    return xor != 0
```

**易错点。**
- 把「对手必败」写成「对手必胜」：`win` 的含义是轮到的玩家能否赢，翻转后轮到对手，要取 `not win(新局面)`。
- 不记忆化：同一局面被不同走法顺序反复到达，`"+" * 20` 一类的串搜索量爆炸。
- 用字符列表拼接且没有复制：在原列表上修改后忘记恢复，递归之间互相污染；用字符串切片拼出新串最不容易错。

**追问。**
- 返回先手的第一步：在 `win` 里记录使对手必败的位置。
- 翻转规则改成连续三个 `"+++"`（或可变长度）：状态不变，枚举规则变；SG 版本里的拆分也相应变化。

**同模式。** LC 293 翻转游戏、LC 292 Nim 游戏、LC 464 我能赢吗、LC 486 预测赢家、LC 877 石子游戏。
