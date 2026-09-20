---
nodes: [problems.social.stack-overflow, oop.relationships]
tags: [problem]
---
# Drill：问答社区（Stack Overflow）

一个问答社区：用户提问、回答、互相评论；给问题和回答投票，声望按票数与采纳涨跌；问题能
打标签、能被搜索。用户账号、鉴权、真实的全文搜索都不在这道题里。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：提问、回答、给问题或回答加评论。先决定"评论挂在问题下面还是
  回答下面"用什么字段区分——这个决定不对，后面每一步都会拧巴。再加标签和按标签检索。
- 第 2 关（约 20 分钟）：投票与声望。一个人对同一个帖子只能有一票，能改能撤；声望的
  增减按帖子类型和投票方向从一张表里查。降票、评论、编辑各自需要声望门槛。想清楚"声望
  存在哪里"——这一关最容易留下一个日后会漂移的坑。
- 第 3 关（约 15 分钟）：只有提问者能采纳一个回答，同一时刻只有一个，但可以改指到另一个
  回答；关闭问题和删除问题分别对它名下的回答做什么，两者不是同一件事；给帖子加编辑历史。
- 第 4 关（选做）：加一种新的、不隶属任何问题的独立发帖类型（文章），或者加悬赏
  （bounty）。评分点是"加它有没有碰到投票那段代码的任何一行"。

**怎么练**：把 `vault/domains/low-level-design/problems/stack-overflow/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/stack-overflow -q`。

**评分点**
- 评论用 `Post` 多态基类 + 组合，评论天生长在具体帖子对象自己身上，没有 `parent_type` 字符串（[[problems-stack-overflow-comment-no-parent-type]]）。
- 声望是对一份不可变事件日志的折叠，不是一个可以被直接 `+=` 的字段；增量缓存必须和独立重算的结果永远相等（[[problems-stack-overflow-reputation-event-fold]]）。
- 改票落的是"新效果减旧效果"的净差值，不是把新效果原样叠加在旧效果之上（[[problems-stack-overflow-vote-change-net-delta]]）。
- 评论、降票、编辑三项权限门槛收在一张表里查，不为一次数值比较建策略类接口（[[problems-stack-overflow-privilege-table]]）。
- 按标签查问题维护的是一个倒排索引（标签到问题 id 集合），不是每次查询扫全表（[[problems-stack-overflow-tag-reverse-index]]）。
- 一把锁保护索引与账本，因为"检查权限再落账"这类复合操作拆锁会开出竞态窗口，GIL 管不住跨语句的复合逻辑（[[problems-stack-overflow-single-lock-rationale]]）。
- 采纳的"移动"是账本上的一次操作，不是"取消再采纳"两次调用，否则提问者的固定奖励会被多算一次（[[problems-stack-overflow-accept-move-atomic]]）。
- 加一种新的发帖类型只需要一个新子类和政策表里几行数据，投票与评论的代码一行不动（[[problems-stack-overflow-article-proves-extension]]）。

**题解**：[[solution-stack-overflow]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
