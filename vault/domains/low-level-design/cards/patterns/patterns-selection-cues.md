---
id: patterns-selection-cues
node: patterns.selection
type: cloze
---
Requirement phrase → pattern reflex: "support multiple/pluggable algorithms for X" → {{c1::strategy}}; "notify interested parties when X changes" → {{c2::observer}}; "add optional features in any combination" (coffee add-ons, stream wrappers) → {{c3::decorator}}; "undo/redo or queue operations" → {{c4::command}}; "object behaves differently through its lifecycle, some actions illegal in some phases" → {{c5::state}}; "treat single items and groups uniformly" → {{c6::composite}}; "request tries a configurable sequence of handlers" → {{c7::chain of responsibility}}.

## zh
需求短语 → pattern 反射：「支持对 X 的多个/可插拔算法」→ {{c1::strategy}}；「当 X 改变时通知相关方」→ {{c2::observer}}；「以任何组合添加可选功能」（咖啡附加品、流包装器）→ {{c3::decorator}}；「撤销/重做或排队操作」→ {{c4::command}}；「对象在其生命周期中行为不同，某些动作在某些阶段非法」→ {{c5::state}}；「统一对待单项和组」→ {{c6::composite}}；「请求尝试可配置的处理程序序列」→ {{c7::chain of responsibility}}。
