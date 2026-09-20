---
id: problems-linkedin-request-directed-connection-undirected
node: problems.social.linkedin
type: qa
step: 3
tags: [grown]
---
## Q
职业社交设计里，连接请求（`ConnectionRequest`）明明记录了“谁发给谁”这种有方向的信息，这和“连接是无向图”这条决策矛盾吗？

## A
不矛盾，因为它们是两个不同的对象，各管各的：`ConnectionRequest` 是一个过程性对象，描述的是“一次请求发生的过程”——谁发起、谁有权接受，这件事本身确实有方向，接受权只在接收方手上，发起方不能自己接受自己发出的请求。而 `ConnectionGraph` 里的边描述的是请求被接受之后留下的**结果状态**——“两人是一度人脉”这件事本身没有方向。把“过程有方向”和“结果无方向”这两条不同的不变量分别交给两个类去守，比塞进同一个类、靠一个 `directed: bool` 参数切换更清楚，也不会出现该无向的地方意外留了个方向。
