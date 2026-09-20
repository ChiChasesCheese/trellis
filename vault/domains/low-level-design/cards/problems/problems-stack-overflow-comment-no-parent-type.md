---
id: problems-stack-overflow-comment-no-parent-type
node: problems.social.stack-overflow
type: qa
step: 1
tags: [grown]
---
## Q
在问答社区（Stack Overflow）设计里，一条评论既可能挂在问题下面也可能挂在某个回答下面，为什么不给 `Comment` 加一个 `parent_type: Literal["question", "answer"]` 字段去区分，而是让 `Question`、`Answer`（以及后来的 `Article`）共享同一个 `Post` 基类？

## A
因为 `parent_type` 字符串和它实际指向的对象之间没有类型系统帮你对齐——传错一个值，运行时才会在某个查找里悄悄出错，而且每加一种可评论的类型（比如后来新增的 `Article`）都要在每一处读写评论的代码里再加一个分支。本设计让 `Question`/`Answer`/`Article` 都继承 `Post`，评论直接组合在具体帖子对象自己身上（`Post.add_comment`）：调用方已经通过 id 拿到了一个具体对象，不管它是哪个子类，调 `add_comment` 都会被多态正确地路由到那个对象自己的评论列表，完全不需要问“这是问题还是回答”。`Comment` 上仍留一个 `post_id` 字段，但它只用来给读者显示，删掉它也不影响任何存取行为。
