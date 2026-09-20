---
nodes: [problems.social.stack-overflow]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/stack-overflow.md
---
# awesome-low-level-design — Designing Stack Overflow

值得读：开源题库（GPL-3.0），Python 实现在 `solutions/python/stackoverflow/`。它的 `Post`
基类同时是 `Question` 和 `Answer` 的父类，评论只挂在 `Post.comments` 列表上、`Comment` 甚至
不存回指字段——这一点和本题解的方向一致：评论从不需要问"我是问题的评论还是回答的评论"，
它就长在拿到手的那个对象上。

但它的声望实现正是本题解要刻意避免的反面教材。`User.reputation` 是一个普通 `int` 字段，
`update_reputation` 直接 `self.reputation += change`；投票产生的是一次性事件
（`UPVOTE_QUESTION` 等），`ReputationManager` 收到事件就按固定分值加一次，**不知道也不检查
这是不是一次改票**——一个人从反对票改成赞成票，`Post.vote()` 正确地把帖子自己的
`vote_count` 调整了 2 个单位，可通知出去的事件仍是单纯的"赞成"，于是 `ReputationManager`
把先前那次反对造成的扣分原样留在账上，又叠加一次赞成的加分，声望多算了。这正是
"声望是一个可以被写坏的字段"的具体后果：本题解把投票效果做成"净差值"事件（改票的
delta 是新效果减旧效果，而不是新效果本身），并且用重新折叠事件日志的结果去验证增量
缓存，专门堵上这个洞。

`ReputationManager` 里另有一处常量对不上：`DOWNVOTE_REP_PENALTY`（命名暗示"扣投票人"）
却被用在帖子作者身上，`POST_DOWNVOTED_REP_PENALTY`（命名暗示"帖子被踩"）却被用在投票人
身上——两个角色的扣分被调换了。此外它的 `accept_answer` 一旦设置过 `accepted_answer` 就
永远不能再改（`if self.accepted_answer is None`），不支持"改指到另一个回答"；也完全没有
关闭或删除问题的实现。这两处都是本题解第 3 关特意要做对的地方。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/stack-overflow.md)
%% trellis:end %%
