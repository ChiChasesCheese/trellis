---
id: patterns-selection-cues
node: patterns.selection
type: cloze
step: 1
---
需求短语到模式的反射：「支持对某个步骤的多个/可插拔算法」→ {{c1::strategy}}；「某个对象变化时通知相关方」→ {{c2::observer}}；「以任意组合叠加可选功能」（咖啡加料、IO 流包装）→ {{c3::decorator}}；「撤销/重做，或者把操作排队、记录下来」→ {{c4::command}}；「对象在生命周期里行为不同，某些动作在某些阶段是非法的」→ {{c5::state}}；「统一对待单个对象和一组对象」→ {{c6::composite}}；「请求依次尝试一串可配置的处理器」→ {{c7::chain of responsibility}}。
