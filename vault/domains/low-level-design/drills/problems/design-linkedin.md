---
nodes: [problems.social.linkedin, oop.relationships]
tags: [problem]
---
# Drill：职业社交（LinkedIn）

个人职业档案——工作经历、教育经历、技能；连接请求与一度人脉；职位发布与申请；招聘方
按技能搜候选人。信息流、私信、账号鉴权都不在这道题里，信息流属于
[[solution-social-network|社交网络（Social Network）]]那道题。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：档案的工作经历、教育经历、技能。先决定这些栏位是结构化的类
  还是自由格式的字典——这个决定不对，技能搜索和经历排序都会建立在没有强制力的假设上。
- 第 2 关（约 20 分钟）：连接请求的发送、接受、忽略、撤回；接受后双方互为一度人脉；
  查两个人之间隔了几度。**先想清楚"连接"和"关注"是不是同一种关系**——这是这道题唯一
  真正的陷阱，想错了后面的度数查询无从谈起。
- 第 3 关（约 15 分钟）：职位发布与申请各自的生命周期（提交、审核中、录用/拒绝/撤回，
  且不能乱跳）；招聘方按技能搜候选人，想清楚这条高频查询该怎么维护数据结构。
- 第 4 关（选做）：加背书或推荐信，要求都建立在"双方已经是一度人脉"之上。评分点是
  "加它有没有碰到连接图那段代码的任何一行"。

**怎么练**：把 `vault/domains/low-level-design/problems/linkedin/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/linkedin -q`。

**评分点**
- 档案的每一栏是结构化的 `dataclass`，不是自由格式的 `dict`，技能能被反向索引安全引用（[[problems-linkedin-profile-structured-not-dict]]）。
- 连接是一个专门的无向图，一条边的写入只有一个入口，不靠"两次写入都执行"的调用约定维持对称（[[problems-linkedin-connection-undirected-graph]]）。
- 连接请求的生命周期是有向的（谁发给谁、谁能接受），但它导致的连接结果是无向的——两者是两个类，分工不同（[[problems-linkedin-request-directed-connection-undirected]]）。
- 度数查询是有界双向 BFS，从两端同时展开、命中即停，成本从 O(b^d) 降到 O(b^(d/2))（[[problems-linkedin-degrees-bidirectional-bfs-cost]]）。
- 按技能搜候选人靠一张维护中的反向索引，不扫描全部档案（[[problems-linkedin-skill-reverse-index]]）。
- 申请状态转移收在一张表里查，不是散落在方法体里的 `if`（[[problems-linkedin-application-transition-table]]）。
- 加背书只需要调用连接图已经公开的只读查询，连接图内部代码一行不动（[[problems-linkedin-endorsement-proves-decoupling]]）。
- 一把锁保护档案、连接图与技能索引，因为复合操作拆锁会开出竞态窗口，GIL 管不住跨语句的复合逻辑（[[problems-linkedin-single-lock-rationale]]）。

**题解**：[[solution-linkedin]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
