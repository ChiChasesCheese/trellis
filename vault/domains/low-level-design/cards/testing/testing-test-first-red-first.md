---
id: testing-test-first-red-first
node: testing.test-first
type: qa
step: 1
---
## Q
退货服务收到 bug 报告：「购买后第 30 天的退货被判为过期，合同说第 30 天仍在窗口内」。动手改 `>=` 之前，为什么要先写一个测试并看着它失败？

## A
**先红再改：红证明测试抓得住，绿证明修好了**

- **红**：新测试在旧代码上必须失败，而且失败的原因就是 bug 描述的那个现象；一上来就绿，说明测试没碰到缺陷；
- **绿**：只改一处，让这个测试变绿，别的测试仍绿；
- **测试成为规格**：这条边界之后谁再改回 `>=`，立刻有人知道；没有测试的修复，下次重构时会悄悄回退；
- **断言两侧**：第 30 天不过期、第 31 天过期；只断言一侧，改成「永不过期」也能通过；
- **从现象出发**：测试名直接写现象（`day_30_is_inside_window`），不要写成 `test_fix_1`。

```python
buggy = lambda days: days >= 30      # 旧代码：第 30 天被判过期
fixed = lambda days: days > 30       # 合同：超过 30 天才过期

def check(expired) -> bool:          # 同一个测试，分别跑在两版代码上
    return expired(30) is False and expired(31) is True

print(check(buggy), check(fixed))    # False True：旧代码红，新代码绿
```

<details class="pt"><summary>延伸</summary>

红的那一步也是在验证测试本身：如果改了代码测试仍然红，先怀疑期望值抄错了，而不是急着再改代码。

</details>

**知识点：**先写失败的测试（Test First）
