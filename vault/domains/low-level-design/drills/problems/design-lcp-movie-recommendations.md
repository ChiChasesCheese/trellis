---
nodes: [lcproject.lcp-movie-recommendations, data.defensive-copy, errors.boundary-validation, data.invariants, api.error-contract]
tags: [problem]
---
# Drill：电影推荐修复（Movie Recommendations）

一个电影推荐服务：给用户从片库里挑出他还没接触过的电影，按他的口味排好队，返回前几部。线上现象是用户明明有评分和观看记录，拿到的却是空的、排错序的，甚至是评过分的片子。
规模是一个服务类加一个固定的 HTTP 适配器；难点是五个小缺陷各自藏在边界上（50 含不含、评 3 分算几、平局的 id 方向），公开测试只会抓到其中一个。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 15 分钟）：先不改代码，把六条规则逐条对照现有服务，写出差异清单（`limit` 的上界、按 `limit` 截断、排除集、权重公式、平局的 id 方向：一共五处）；跑一遍测试，看哪些失败。每处缺陷先写一个会失败的测试。
- 第 2 关（约 20 分钟）：修校验与候选集：`limit` 取 1 到 50 含 50，布尔不算整数；排除集是评过分的并上看过的；评分只走偏好、不走排除，下架的评分仍然贡献。
- 第 3 关（约 20 分钟）：修偏好与排序：权重是 `rating - 3`；排序键是分数降序、热度降序、id 升序；按 `limit` 取前几名；冷启动用户只按热度和 id 排；负分候选保留。
- 第 4 关（选做，约 15 分钟）：隔离与适配器：构造之后改输入、改返回值，服务都不受影响；检查五种 `limit` 文本在适配器里的反应；然后写三个书面回答：怎样区分候选排除与评分；新策略里怎样避免热度压倒个性化；请求期间目录和评分变化时用什么快照或版本。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-movie-recommendations/starter.py` 里的 `RecommendationService` 当作要修的服务（`dispatch` 是固定的适配器），改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-movie-recommendations -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给六条规则和两三个小例子（评过分的电影不出现、打 3 分不加分、同分同热度按 id 升序），要求它只列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一个缺陷、只给它一个失败的测试，改完立刻运行测试。
排除与打分分成两条路径、排序键怎么写、哪里复制这些设计决定自己留着；期望值自己用小例子手算，不接受"把测试改成通过"，也不让它把"公开测试全绿"当作修好的证据。

**评分点**
- 写得出开工前的规则：排除集是并集、`rating - 3`、三级排序键、`limit` 含 50、先 `limit` 后 `user`、进出各复制一次（[[lcp-movie-recommendations-contract-rules]]）。
- 说得清评过分的电影既排除又贡献权重，下架的电影也一样，所以排除与偏好是两个集合、两条路径（[[lcp-movie-recommendations-state-and-invariant]]）。
- 知道热度并入分数时要先统一尺度、给热度设份额上限，并能说出怎样监控它有没有压倒个性化（[[lcp-movie-recommendations-reflection-popularity-blend]]）。
- 知道一次请求只读一个不可变快照、写入方换整份快照，并能说出响应里为什么带版本号（[[lcp-movie-recommendations-reflection-snapshot-version]]）。
- 写得出能抓住缺陷的测试：`limit=50`、候选多于 `limit`、评过分的电影、打 3 分的权重、同分同热度的 id 顺序（[[lcp-movie-recommendations-contract-rules]]、[[lcp-movie-recommendations-state-and-invariant]]）。

**题解**：[[solution-lcp-movie-recommendations]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
