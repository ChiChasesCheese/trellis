# REVIEW_KEY · cr02 risk API

> 优先级口径：**影响面 × 可能性 × 可发现性**。行号对应 `starter/`。`diff 内` / `diff 外` 同 cr01。
> 这个 PR 的主线是**多租户隔离**：四个 P0 里有两个是跨租户读数据，一个是读出任意列/注入，一个是缓存被投毒即 RCE。

## 问题表（13 条：P0 4 · P1 5 · P2 4）

| ID | 位置 | 级 | 一句话问题 | 为什么是这个级别 | 修法 | 验收测试 |
|---|---|---|---|---|---|---|
| CR-01 | `app.py:47-51`、`app.py:58-61`（`principal` 取到后从未使用） | P0 | IDOR：只校验 key 有效，不校验 key 所属租户 == URL 里的租户 | 影响面：任意一把有效 key 能读**所有租户**的用户风险评分和用户列表——这是产品最敏感的数据；可能性：改 URL 即可，零技巧；可发现性：功能测试全绿（PR 说明里还写成"设计"）。四项里最重 | `principal.tenant_id != tenant` → 404（不暴露租户是否存在）；把授权收敛到一个 `authorize()` | `test_cr01_key_of_one_tenant_cannot_read_another_tenants_user`、`test_cr01_key_of_one_tenant_cannot_list_another_tenants_users` |
| CR-02 | `repo.py:26,30,32` | P0 | `sort` 参数拼进 `SELECT` 列、`WHERE` 与 `ORDER BY` | 影响面：整库可被读（子查询做布尔盲注）、`sort=email` 即可按 PII 排序做推断；可能性：公开端点，key 持有者即可；可发现性：评审一眼可见，功能测试不会发现。注意 f-string 出现在三处，不只 `ORDER BY` | 白名单字典 `{"user_id","name","risk_score"}` → 列名；不认识的返回 400；游标里的值始终走绑定参数 | `test_cr02_sort_is_validated_against_a_whitelist`（5 个载荷） |
| CR-03 | `service.py:5,28,43` | P0 | 缓存值用 `pickle` 序列化/反序列化 | 影响面：任何能写缓存的一方（Redis 被入侵、SSRF 到 Redis、共享 Redis 的另一个服务）都得到 API 进程的代码执行；可能性：低到中，但后果是整机沦陷；PR 理由"以后可以放更丰富的对象"恰恰是风险 | 用 `json`；读到坏数据当作 miss 并删除 | `test_cr03_poisoned_cache_entry_is_never_unpickled` |
| CR-04 | `service.py:25` | P0 | 缓存 key `risk:{user_id}` 不含租户；user_id 在租户间会重复 | 影响面：租户 B 读到租户 A 同 id 用户的评分与姓名，**即使 CR-01 修好了**也泄露；可能性：user id 是自增/邮箱前缀时必然撞；可发现性极低（单租户测试看不到）。这也是缓存层的隔离问题，所以和 CR-01 并列 P0 | key = `risk:{tenant}:{user}`；payload 里带 tenant 并在读出时校验 | `test_cr04_cached_score_of_one_tenant_is_not_served_to_another` |
| CR-05 | `auth.py:26`（diff 内）、`db.py:30,55`（diff 外） | P1 | key 摘要是**无盐 MD5**（建表与 `create_api_key` 在既有代码里），校验用 `==` | 影响面：库泄露后 MD5 可被撞库/彩虹表（若 key 由人起名）；`==` 的时序差理论上可逐字节猜，网络抖动下实际难利用。可能性低，所以不进 P0；但"凭据怎么存"是评审必问 | 长随机 secret + SHA-256（或带 pepper 的 HMAC）存储；`hmac.compare_digest`；key 不存在时也做一次比较，抹平时序 | `test_cr05_api_key_secret_is_not_stored_in_plaintext_or_md5`、`test_cr05_api_key_digest_is_compared_in_constant_time` |
| CR-06 | `service.py:24-44` | P1 | 缓存击穿：热点 key 过期的一刻，所有并发请求同时回源（无 single-flight） | 控制台轮询同一批用户，过期瞬间 N 个请求各打 2 条 SQL；放大成 DB 连接/CPU 尖刺，**并且在 DB 慢时自我加剧**（越慢堆得越多）。平时看不出来，所以是 P1 而非 P2 | 按 key 的锁（本题用 64 个分段锁）+ 拿到锁后二次检查缓存；跨进程用 Redis `SET NX` 租约；TTL 加抖动；过期后先返回旧值再异步刷新 | `test_cr06_concurrent_cold_requests_hit_the_database_once` |
| CR-07 | `repo.py:30` | P1 | 分页用 `>=`，下一页第一条重复上一页最后一条；`limit` 满页即给 cursor（最后多一次空页） | 导出/遍历得到重复行，按"数量"校验的下游会错；不丢数据所以 P1。注意这里错在**比较符**，而游标取值本身（最后一行）是对的 | `>` ；多取一行判断是否还有下一页 | `test_cr07_cursor_pagination_has_no_duplicates_or_gaps`、`test_cr07_pagination_by_a_non_unique_sort_key_is_stable` |
| CR-08 | `app.py:63` | P1 | `limit` 无上限、无下限：`limit=100000` 拉全表；`limit=-1` 在 SQLite 里等于**不限制**；`limit=abc` 抛 `ValueError` 变成 500 | 一个请求就能拖垮进程内存/DB；且 CR-01 修复前可跨租户拉全表。可能性高（SDK 误用都会触发） | 校验 1..`max_limit`，非法返回 400 | `test_cr08_limit_is_bounded` |
| CR-09 | `service.py:44` | P1 | 日志里打印用户 email | PII 进入日志系统，保留期/访问面都比业务库宽，合规（GDPR/SOC 2）问题；一旦写入难以清除 | 只记 tenant、user id、score | `test_cr09_email_is_not_logged` |
| CR-10 | `app.py:44-66` | P2 | 两个 handler 复制粘贴同一段认证；`route` 里的 `m`、`r[3]` 等魔法下标和无意义命名；无类型注解（`create_app` 返回值） | 不是故障，但重复的认证块正是 CR-01 漏改的温床：授权逻辑应只有一处 | 抽 `authorize()`；`ApiError` 异常 + 统一出口；命名行 | solution 的结构（见 `solution/riskapi/app.py`） |
| CR-11 | `app.py:42,49,52,69,76` | P2 | 错误形状不统一（`{"error": "..."}` / `{"message": ...}`），500 把 `str(exc)` 返回给客户端 | 客户端无法统一解析；`str(exc)` 会泄露 SQL/表名/路径，等于给 CR-02 的注入提供回显 | 统一 `{"error": {"code", "message"}}`；500 只回通用文案，细节进日志 | `test_cr11_errors_share_one_shape`、`test_cr11_unexpected_errors_do_not_leak_internals` |
| CR-12 | `cache.py:21-37` | P2 | 缓存无容量上限，过期条目只在被读到时才删；分数夜间更新后无失效，最长陈旧 5 分钟 | 内存随"被访问过的 key 数"线性增长；长期运行才暴露。陈旧窗口要与产品对齐 | `max_entries`，先清过期再淘汰最旧；评分作业更新后 `delete` 对应 key（事件驱动） | `test_cr12_cache_has_a_size_bound` |
| CR-13 | `tests/` | P2 | 17 个测试只有 happy path：没有"别的租户的 key"、没有恶意 `sort`、没有坏缓存、没有分页翻到底 | 正是这些缺失让 CR-01 到 CR-04、CR-07 全部绿灯通过；评审时应该要求先补测试再合并 | 按 `acceptance/` 的思路补负面用例；用"别的租户"作为每个端点的默认负面测试 | solution 自带 `tests/test_app.py` 新增 3 个 |

## 评审中的判断

- **P0 的共同点**：都是"代码行为正确、功能测试全绿，但边界被破坏"。评审要问的是"谁能调用、谁能写入、谁的数据"。
- **diff 外**：CR-05 的存储半边（`db.py`）。能说出"我去看了 key 是怎么存的"是加分项。
- **红鲱鱼**：`wsgiref` 单线程服务器（README/PR 写明是开发用）、`scoring.py` 里的阈值 70/30、`models.py` 里没被用到的 `UserRow` ——不是本 PR 引入，也不是问题。
- **PR 描述里的线索**：`any valid key may call the API`（CR-01）、`pickle ... richer objects`（CR-03）、`log each lookup with the user`（CR-09）、`any column you want`（CR-02）、`whenever the page is full`（CR-07）。
