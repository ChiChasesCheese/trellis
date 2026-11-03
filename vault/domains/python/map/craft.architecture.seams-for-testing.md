%% trellis:begin %%
# 测试接缝：时钟、文件系统、sleep、可观测计数器
*编码功力（Coding Craft） / 架构理解（Architecture）*

设计时就把「可替换的外部依赖」和「可断言的内部状态」留成接缝，让测试不需要 sleep、不需要猜、不需要私有属性。

**Requires:** [[domains/python/map/engineering.testing|测试：pytest 夹具与参数化、`unittest.mock`、注入时钟与依赖]], [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]]

## Cards (5)
1. [[craft-seams-for-testing-1-observable-instead-of-sleep]]
2. [[craft-seams-for-testing-2-drive-the-scheduler-with-now]]
3. [[craft-seams-for-testing-3-count-the-work]]
4. [[craft-seams-for-testing-4-inject-not-patch]]
5. [[craft-seams-for-testing-5-observability-at-scale]]
%% trellis:end %%

## Notes
