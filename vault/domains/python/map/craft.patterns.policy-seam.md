%% trellis:begin %%
# 策略接缝：把会变的规则做成注入的纯函数/对象
*编码功力（Coding Craft） / 跨题模式（Patterns）*

核心流程固定，变化点（超售、涨价、匹配、淘汰、找零、叠加）在构造时注入；默认值是策略的下界。

**Requires:** [[domains/python/map/functions.first-class|一等函数：作为对象传递、高阶函数与 lambda]], [[domains/python/map/classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]]

## Cards (5)
1. [[craft-policy-seam-1-inject-what-changes]]
2. [[craft-policy-seam-2-validate-the-policy-output]]
3. [[craft-policy-seam-3-callable-or-protocol-or-enum]]
4. [[craft-policy-seam-4-data-or-policy]]
5. [[craft-policy-seam-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
