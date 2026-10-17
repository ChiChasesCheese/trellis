---
id: amz-round-test-names-state-business-rules
node: amazon.amz-round
type: qa
step: 5
tags: [grown]
---
## Q
Amazon 官方要求「测试名要描述业务与技术需求」。在票价或折扣类的设计里，写哪种测试名才算合格？

## A
测试名读起来应当是一条业务规则，而不是方法名。差：`test_calculate_fare`、`test1`。好：`test_weekend_fare_is_capped_at_daily_limit`、`test_removing_a_station_never_changes_fares_before_it`。测试体也要和名字一致：名字说「封顶」，断言就必须是超过上限后仍等于上限。时间紧时只写 2–3 个这样的测试名并口述断言，比写满十个 `test_x` 得分更高。
