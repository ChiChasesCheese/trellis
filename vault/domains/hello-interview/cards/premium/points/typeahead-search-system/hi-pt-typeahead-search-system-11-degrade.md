---
id: hi-pt-typeahead-search-system-11-degrade
node: qb.sd.typeahead-search-system.points
type: qa
step: 11
---
## Q
**搜索联想 · 故障降级**｜追问 · 出自：搜索联想 › 深入 7

联想服务不可用或快照切换失败时，用户体验怎么保证？

## A
**客户端。** 静默不显示建议，不阻塞搜索框，因为搜索本身比联想重要。
**服务端。** 快照切换失败保留旧版本；数据中心故障时流量切到其他区域。

**原则。** 陈旧的建议比没有建议好。
