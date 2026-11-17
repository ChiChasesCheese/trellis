---
nodes: [lcproject.lcp-movie-watchlists, structure.storage, api.error-contract, concurrency-depth.compound-actions, errors.boundary-validation]
tags: [problem]
---
# Drill：私人片单修复（Persistent Private Watchlists）

一个 SQLite 上的私人片单服务：每个用户有自己的几张命名片单，每张片单是一组不重复的电影 id；同一个数据库文件上的第二个服务实例要立刻看得到已提交的内容。线上现象是重复添加也报"新建成功"、用户能读到别人的片单、删除一张片单会连带删掉别的片单、移除一部电影会删掉同一张片单里的其他电影。
规模是一个服务类加一个固定的 HTTP 适配器；难点是五个缺陷里公开测试只会抓到一个，其余四个藏在 SQL 的 `WHERE` 条件里。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 15 分钟）：先不改代码，把六条规则逐条对照现有服务，写出差异清单（名字存的是没 `strip` 的原串、所有者条件缺失、重复添加的状态码、移除电影的条件、删除片单的条件：一共五处）；跑一遍测试，看哪些失败。每处缺陷先写一个会失败的测试。
- 第 2 关（约 15 分钟）：修名字与归属：存 `strip` 之后的值；所有读、改、删、加、移都带所有者；别人的和不存在的都是 `list_not_found`；校验先于归属。
- 第 3 关（约 20 分钟）：修成员与删除：已存在返回 200、新增返回 201（由数据库的约束与 `rowcount` 判断，不是先查再插）；移除只删指定的那一部，缺失的电影 404；删除只删请求的那一张，成员级联带走。
- 第 4 关（选做，约 15 分钟）：持久化与并发：每个写操作一个事务、失败回滚；第二个实例读得到、关闭重开还在；八个线程抢同一部电影恰好一个 201；然后写三个书面回答：失败的修改怎样不动已提交的数据；什么约束防止重复成员；大片单怎样分页又不松动归属。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-movie-watchlists/starter.py` 里的 `WatchlistService` 当作要修的服务（`dispatch` 是固定的适配器），改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-movie-watchlists -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给六条规则和两三个小例子（别人读你的片单得 404、同一部电影加两次得 201 再 200、移除一部不影响其他），要求它只列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一个缺陷、只给它一个失败的测试，改完立刻运行测试。
所有者条件写在哪里、重复由谁裁决、事务在哪一层开关，这些设计决定自己留着；期望值自己用"两个用户、各两张片单"的小例子手算，不接受"把测试改成通过"，也不让它把"三个公开测试全绿"当作修好的证据：五个缺陷里它只抓到一个。

**评分点**
- 写得出开工前的规则：名字存 `strip` 之后的值、"不存在"和"别人的"同一个 404、校验先于归属、201 与 200 的区别、先片单后电影、删除只删请求的那一张（[[lcp-movie-watchlists-contract-rules]]）。
- 说得清要存哪些状态、哪条不变量最要紧：两张表，所有者条件进每条语句，联合主键防重复，外键级联带走成员，`AUTOINCREMENT` 保证 id 不复用（[[lcp-movie-watchlists-state-and-invariant]]）。
- 知道失败的修改靠"校验在事务之外、写操作一个事务、异常即回滚"保证不改已提交的数据，并能说出 `BEGIN IMMEDIATE` 为什么能避免 `database is locked`（[[lcp-movie-watchlists-reflection-failed-mutations]]）。
- 知道大片单用键集分页、每一页重新做归属检查、游标不携带权限（[[lcp-movie-watchlists-reflection-pagination]]）。
- 写得出能抓住缺陷的测试：两个用户互读互改、同一部电影加两次、移除时片单里还有别的电影、删除时同一用户还有另一张片单、八个线程抢同一部电影（[[lcp-movie-watchlists-contract-rules]]、[[lcp-movie-watchlists-state-and-invariant]]）。

**题解**：[[solution-lcp-movie-watchlists]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
