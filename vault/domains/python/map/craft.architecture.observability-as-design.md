%% trellis:begin %%
# 可观测性是设计的一部分：丢弃必须计数，状态变化必须留痕
*编码功力（Coding Craft） / 架构理解（Architecture）*

任何会丢、会拒、会重试、会降级的地方都要有计数或事件，否则线上只能靠猜。

**Requires:** [[domains/python/map/engineering.logging-config|日志与配置：logging 层级、处理器与格式、结构化日志、环境变量配置]], [[domains/python/map/engineering.testing|测试：pytest 夹具与参数化、`unittest.mock`、注入时钟与依赖]]

## Cards (4)
1. [[craft-observability-as-design-1-every-drop-gets-a-counter]]
2. [[craft-observability-as-design-2-record-the-change-when-it-happens]]
3. [[craft-observability-as-design-3-metrics-are-frozen-snapshots]]
4. [[craft-observability-as-design-4-three-places-from-lld-to-slo]]
%% trellis:end %%

## Notes
