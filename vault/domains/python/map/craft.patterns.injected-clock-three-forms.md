%% trellis:begin %%
# 注入时钟的三种形态：Clock 参数 / 时间戳参数 / tick 步进
*编码功力（Coding Craft） / 跨题模式（Patterns）*

逻辑里永远不读系统时间：要么构造时注入 clock，要么每个方法收 timestamp，要么由测试推进离散 tick。

**Requires:** [[domains/python/map/engineering.testing|测试：pytest 夹具与参数化、`unittest.mock`、注入时钟与依赖]], [[domains/python/map/engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]]

## Cards (5)
1. [[craft-injected-clock-three-forms-1-why-inject]]
2. [[craft-injected-clock-three-forms-2-three-forms]]
3. [[craft-injected-clock-three-forms-3-monotonic-contract]]
4. [[craft-injected-clock-three-forms-4-separate-core-from-thread]]
5. [[craft-injected-clock-three-forms-5-scales-event-time]]
%% trellis:end %%

## Notes
