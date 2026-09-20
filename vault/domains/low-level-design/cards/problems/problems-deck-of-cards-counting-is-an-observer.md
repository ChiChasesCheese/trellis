---
id: problems-deck-of-cards-counting-is-an-observer
node: problems.games.deck-of-cards
type: qa
step: 6
tags: [grown]
---
## Q
赌场牌鞋（shoe，几副牌摞在一起）要支持算牌（card counting）。为什么不该在牌鞋里加一个 `running_count` 字段顺手加减？事件里该带什么？

## A
三条理由：现实里牌鞋**不知道**有人在算它，模型该反映这一点；算牌体系不止一种（Hi-Lo、KO、Omega II），把其中一种焊进牌鞋等于宣布只支持这一种；用不到算牌的场合还要为这个字段付代价。

正确做法是牌鞋只**广播事件**，算牌器是一个纯粹的观察者（Observer），去掉它牌鞋的行为一模一样。关键在于**事件要自带发生了什么**——发了哪几张、还剩多少张、还剩几副——而不是只发一个「有事发生了」的通知；否则订阅者必须回头读 `shoe.remaining`，那是对主体内部状态的反向依赖，并发时还会读到中间状态。

两个必须答对的细节：**洗牌也是一个事件**，算牌器收到它要把计数归零（「洗完还在用旧计数」是算牌代码最经典的 bug）；**订阅要能取消**，`subscribe` 返回一个 unsubscribe 闭包，监听器表才不会只进不出。
