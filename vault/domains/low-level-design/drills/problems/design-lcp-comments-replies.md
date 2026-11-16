---
nodes: [lcproject.lcp-comments-replies, structure.storage, data.defensive-copy, concurrency-depth.compound-actions, errors.boundary-validation]
tags: [problem]
---
# Drill：评论与回复（Comments & Replies）

一个讨论平台已经有帖子，现在要在帖子下加评论、在评论下加回复，只有这两层。服务放在内存里，被很多请求线程同时调用，返回给调用方的是普通字典与列表。
规模是一个服务类加一个帖子仓库；难点不在存数据，而在合同的细节（检查顺序、两条 ID 序列、失败不烧号）、返回快照，以及锁到底要罩住哪一段。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 12 分钟）：评论与读取。校验两个文本（必须是字符串、去空白后非空，存与返回原值），查帖子，存评论；`get_comments` 按提交顺序返回，没有评论的帖子返回 `[]`，不存在的帖子抛 `NotFoundError`。先把合同里的三个返回形状写成断言。
- 第 2 关（约 12 分钟）：回复与资源关系。检查顺序是文本、帖子、评论；评论不存在或属于另一个帖子都是 `NotFoundError`；回复 ID 与评论 ID 是两条独立的序列。数据结构要保证加回复不扫描全站。
- 第 3 关（约 12 分钟）：ID、顺序与快照。失败的调用不消耗 ID；顺序来自提交而不是 `created_at`（把假时钟拨回过去验证）；对返回值的任何修改都伤不到服务内部，旧快照不随新数据变长。
- 第 4 关（选做，约 9 分钟）：并发与短文。十几个线程同时加评论，ID 恰好是 1 到 N；与写入同时进行的读取，每次看到的都是某一时刻的整串（评论 ID 是连续前缀）。再写三个书面回答：锁为什么要罩住整段读—改—写、全局锁与每帖一把锁怎么取舍；为什么要返回快照；多实例部署时 ID 与快照怎么变。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-comments-replies/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-comments-replies -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给十三条规则和几个数字例子（先评论后回复再读取、用别的帖子回复要 `NotFoundError`、失败后下一个 ID 不跳号），要求它先复述规则里最容易漏的几条，再只实现 `add_comment` 和 `get_comments`；
你核对后，一次只给它一个失败的测试，改完立刻运行测试。数据结构、锁的范围、ID 在哪一步分配、快照怎么拷贝这些设计决定自己留着；并发测试自己写（屏障加不变量），不接受"把测试改成通过"，也不接受只靠 `sleep` 的并发测试。

**评分点**
- 写得出开工前的合同：检查顺序、文本只在判空时去空白、"找不到"只有一种、两条独立的 ID 序列、顺序就是提交顺序、返回快照（[[lcp-comments-replies-contract-rules]]）。
- 说得清要存哪些状态、为什么每个帖子一个 `Thread`、字典的插入顺序等于提交顺序等于 ID 升序这条不变量（[[lcp-comments-replies-state-and-invariant]]）。
- 知道锁要罩住"读时钟、分配 ID、追加"这一整段，ID 原子不等于顺序一致，全局锁与每帖一把锁怎么取舍（[[lcp-comments-replies-reflection-lock-scope]]）。
- 知道为什么返回快照、快照为什么要在锁里生成、多实例时快照与 ID 怎么变（[[lcp-comments-replies-reflection-snapshot-reads]]）。
- 写得出能抓住缺陷的测试：失败后 ID 不跳号、时钟回拨后顺序不变、修改返回值伤不到内部、屏障下的并发读写（[[lcp-comments-replies-contract-rules]]、[[lcp-comments-replies-reflection-snapshot-reads]]）。

**题解**：[[solution-lcp-comments-replies]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
