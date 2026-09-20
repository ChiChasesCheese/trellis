---
id: problems-stack-overflow-article-proves-extension
node: problems.social.stack-overflow
type: qa
step: 8
tags: [grown]
---
## Q
问答社区设计的第 4 关要求加一种独立的发帖类型“文章”（`Article`），且不隶属任何问题，这条加法为什么能证明“评论用多态而不用 parent_type、声望规则用查表而不用分支”这两个决策是对的？

## A
因为 `Article` 只需要继承 `Post`（自动获得评论、编辑历史）并在 `ReputationRules.vote_delta` 表里加两行 `(ARTICLE, UP/DOWN)` 的数值，`ReputationLedger.cast_vote`、`retract_vote` 和 `Post.add_comment` 里没有一行代码需要修改——它们从一开始就只依赖 `Post.kind` 和多态方法，而不是某个针对具体类型的分支或字符串判断。如果之前用的是 `parent_type` 字符串或按类型分支的声望计算，加一种帖子类型就必须回头改这些“核心”代码；本设计只需要加数据。
