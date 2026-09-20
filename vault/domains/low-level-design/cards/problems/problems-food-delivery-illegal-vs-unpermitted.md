---
id: problems-food-delivery-illegal-vs-unpermitted
node: problems.marketplaces.food-delivery
type: qa
step: 2
tags: [grown]
---
## Q
外卖订单状态机里，「菜还没好就想取餐」和「顾客想把订单标成已送达」应该抛同一个异常吗？

## A
**不应该，必须分成两个。**

```python
allowed = TRANSITIONS[self._state].get(target)
if allowed is None:
    raise IllegalTransitionError(...)   # 这条边根本不存在，谁来都不行
if by not in allowed:
    raise NotPermittedError(...)        # 边存在，但你没资格走
```

前者是**流程错**：动作本身在当前状态下不成立，正确的反应是等（或者提示「请等餐厅出餐」）。后者是**权限错**：动作在当前状态下成立，只是发起者不对，正确的反应是查这个调用是从哪来的——它多半意味着客户端有 bug 或者有人在越权。

给 App 的提示文案、给客服的解释、给监控的告警级别全都不同。合并成一个 `ValueError`，线上排障时就分不清「系统慢」和「有人在越权」。
