---
id: problems-linkedin-endorsement-proves-decoupling
node: problems.social.linkedin
type: qa
step: 7
tags: [grown]
---
## Q
职业社交设计的第 4 关要求加“背书”（endorsement）功能，且要求只有一度人脉能互相背书，这条加法为什么能证明“连接是无向图”这条决策带来的好处？

## A
因为 `endorse_skill` 只需要调用 `ConnectionGraph.are_connected(endorser_id, subject_id)` 这个已经公开的只读方法去判断“这两人是不是一度人脉”，`ConnectionGraph` 内部一行代码都不用改——它从设计之初就是一个独立的、只回答“连没连接”这类查询的组件，不知道背书、推荐或者任何调用它的具体业务。如果“连接”当初是散落在业务逻辑里的临时判断（比如直接翻某个成员对象的关注列表），加背书这种新功能很可能需要重新实现一遍“判断是否连接”的逻辑，而不是简单地复用一个既有的公开接口。
