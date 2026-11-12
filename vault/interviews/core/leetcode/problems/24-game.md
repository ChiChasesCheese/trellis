---
slug: 24-game
---
## Q
**LC 679 24 点游戏**｜Hard

给 `4` 张 `1~9` 的牌，用 `+ - * /` 和括号（实数除法，不可拼接数字、不可一元负号）能否算出 `24`。

## A
**一句话。** 回溯：每次任选两个数用四种运算合并成一个，剩一个数时判断是否为 `24`，用 `Fraction` 避免浮点误差。

```python
def judge_point24(cards):
    def solve(nums):
        if len(nums) == 1:
            return nums[0] == 24
        for i, j in combinations(range(len(nums)), 2):
            a, b = nums[i], nums[j]
            rest = [x for k, x in enumerate(nums)
                    if k != i and k != j]
            res = {a + b, a * b, a - b, b - a}  # 减、除要试两个方向
            if b:
                res.add(a / b)
            if a:
                res.add(b / a)
            if any(solve(rest + [r]) for r in res):
                return True
        return False

    return solve([Fraction(c) for c in cards])
```

**复杂度。** 时间 `O(1)`（叶子数固定上界），空间 `O(1)`。

**易错点。**
- 浮点直接比 `== 24`：`[3,3,8,8]` 的 `8/(3-8/3)` 得 `23.99999999999999`，误判 `False`。
- 除数为 `0` 不跳过：抛 `ZeroDivisionError`。
- 漏掉 `b - a`、`b / a`：只试一个方向会漏解。

**追问。**
- 要输出表达式？：每个数同时带字符串，合并时拼 `"(" + sa + "+" + sb + ")"`。
- 推广到 `n` 张牌？：同一递归，叶子阶乘级，用排序后的元组做 `memo` 去重。

**同模式。** LC 282 给表达式添加运算符、LC 241 为运算表达式设计优先级、LC 22 括号生成、LC 494 目标和
