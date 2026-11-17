---
id: ai-verification-independent-expected
node: ai.verification
type: qa
step: 2
---
## Q
让智能体补测试时，期望值可以直接取它的实现跑出来的结果吗？为什么？

## A
**期望值从合同手算，不从代码抄**

- **抄输出**：断言和实现是同一个来源，对当前代码恒成立，实现里的错也一起抄进了期望值；
- **共同误读**：实现和测试都出自同一个对合同的理解，理解错了，两边一致地错，测试永远是绿的；
- **手算**：按合同写一张“输入 → 期望”的表，每一行旁边写出算式，别人能复核；
- **和示例同源**：合同里的数字例子本来就是手算的，新增的行用同样的方式写。

```python
def fee(cents: int) -> int:
    return round(cents * 0.029) + 30      # 合同：2.9% 加 30 分，.5 进位

snapshot = {500: fee(500)}                # 期望值取自实现的输出
by_hand = {500: 15 + 30}                  # 500 × 2.9% = 14.5，进位得 15

print(snapshot[500] == fee(500))          # True：永远通过
print(by_hand[500] == fee(500), fee(500)) # False 44：round 是半入偶
```

<details class="pt"><summary>延伸</summary>

Python 的 `round` 对正好 .5 取偶数（`round(14.5)` 是 14），这是文档写明的行为；合同要求“.5 进位”时要用 `Decimal` 的 `ROUND_HALF_UP`。这个错只有手算的那一行抓得到。

</details>

**知识点：**验证输出（Verification）
