---
id: bank-rule-engine-eval-order
node: bank.machine-coding.rule-engine
type: qa
step: 2
---
## Q
一个功能开关有「是否启用」「定向规则列表」「兜底分桶」三层。求值的顺序和命中语义该怎么定？顺序写反会怎样？

## A
**停用 → 规则自上而下首中 → 兜底**

- **顺序就是语义**：先看总开关，停用就直接返回默认值，规则一条不看；再按列表顺序找第一条条件全部命中的，命中即返回，后面的不再看；都不中才走兜底；
- **首中即胜**：规则顺序就是优先级，具体的写上面、宽泛的写下面。代码里 `US + pro` 排在 `US` 之前；把两条换位置，`US` 的 pro 用户先撞上宽泛的那条，拿到 `on` 而不是 `beta`；
- **结果自带解释**：`reason` 说明是哪一层回答的，`rule_index` 只在规则命中时出现，排查「这个用户为什么看到 X」靠它；
- **写反的后果**：启用检查放到规则之后，停用的开关仍会给命中规则的用户发放；把「首中返回」改成「收集所有命中」，最后一条会盖掉前面的；
- **兜底层这里简化成固定值**：真实的兜底是放量表（变体到百分比，没写的变体权重为 0，总和恰好 100），按用户哈希分桶，和规则层互不相干。

```python
def evaluate(flag, attrs, hit):                   # hit(rule, attrs)：规则怎么匹配另写
    if not flag["enabled"]:                       # 第一层：停用就不看规则
        return {"value": flag["default"], "reason": "DISABLED"}
    for i, rule in enumerate(flag["rules"]):      # 第二层：自上而下，第一条命中的赢
        if hit(rule, attrs):
            return {"value": rule["serve"], "reason": "RULE_MATCH", "rule_index": i}
    return {"value": flag["fallthrough"], "reason": "FALLTHROUGH"}   # 第三层：兜底

flag = {"enabled": True, "default": "off", "fallthrough": "off", "rules": [
    {"when": {"country": "US", "plan": "pro"}, "serve": "beta"},
    {"when": {"country": "US"}, "serve": "on"}]}
hit = lambda r, a: all(a.get(k) == v for k, v in r["when"].items())   # 只演示等值匹配
for attrs in ({"country": "US", "plan": "pro"}, {"country": "US"}, {"country": "FR"}):
    print(evaluate(flag, attrs, hit))
print(evaluate({**flag, "enabled": False}, {"country": "US"}, hit))
```

<details class="pt"><summary>延伸</summary>

推荐活动的「分级列表」是同一个形状：第一个有结果的级别决定输出。还有一个顺序陷阱：要在整个候选集上匹配、再截断到条数上限；先截断成前几场再匹配，最早的几场都不在客户附近时，哪怕第 20 场就在隔壁也推荐不出来。见 [[solution-lcp-event-campaigns|活动推荐规则修复（Event Campaigns）]]。

</details>

**知识点：**规则引擎（Rule Engine）
