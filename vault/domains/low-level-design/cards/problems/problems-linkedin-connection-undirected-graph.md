---
id: problems-linkedin-connection-undirected-graph
node: problems.social.linkedin
type: qa
step: 2
tags: [grown]
---
## Q
职业社交设计里，“连接”（一度人脉）为什么要建成一个专门的无向图 `ConnectionGraph`，而不是像很多题解那样，给每个成员一份 `following: set[str]`、接受请求时双方各自往对方的集合里加一个 id？

## A
两份独立集合能做到“双方都看到对方”，但完全靠“两次写入都执行”这个调用约定去维持对称性，没有任何东西强制它——一次写入失败、或者有代码路径绕过接受请求直接改了底层集合，就会出现 A 认为已连接、B 不这么认为的不一致状态，而这种不一致正是“关注”被允许存在、“连接”不应该存在的地方。专门的 `ConnectionGraph.connect(a, b)` 把两个方向的写入钉在同一个方法里，调用方只需要调用一次，物理上不可能只执行一半；对称性由图结构本身保证，不再依赖调用者自觉。
