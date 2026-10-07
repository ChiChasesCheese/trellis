# walkthrough · cr02 risk API（45 分钟）

同 cr01 的形态：先 code review（约 20 分钟讨论 comments），再转到"扩展 + 规模"（`followups.md`）。这个 PR 是**多租户 API**，评审的主问题是"谁能读谁的数据"。

| 分钟 | 做什么 |
|---|---|
| 0-5 | 读 `PR.md`，把"Notes"里每一句当成线索（"any valid key may call the API"） |
| 5-25 | 读 `pr.diff`，边读边写评论（file:line + 优先级） |
| 25-32 | 让 Claude 复核；合并发现，删假阳性 |
| 32-35 | 60 秒口头总结，先 P0 |
| 35-45 | 抽 3-4 个 followups 回答 |

## 1. 读 diff 的顺序（按攻击面）

1. `app.py`：每个路由——谁能调用（认证）、调用的是谁的数据（授权：key 的租户 vs URL 的租户）、每个输入参数从哪来（`sort`、`cursor`、`limit`）。**对每个入口问三件事：谁？谁的？输入是什么？**（CR-01、02、07、08、10、11）
2. `repo.py`：所有 SQL 里哪些位置是 f-string（CR-02、07）。
3. `service.py` + `cache.py`：缓存里存什么、key 怎么拼、怎么反序列化、过期后会怎样（CR-03、04、06、09、12）。
4. `auth.py`，然后**去看 `db.py` 里 key 怎么存**（diff 外，CR-05）。
5. `tests/`：缺什么（CR-13）。

## 2. 给 Claude 的评审提示词

```
Review this diff for correctness under concurrency, failure modes, security and tenant isolation;
cite file:line; rank by blast radius. For every endpoint, state which tenant's data it can return
and what proves the caller is allowed to see it. Check every f-string that reaches SQL, every
deserialiser, and every cache key. Follow calls into db.py even though it is outside the diff.
```

追问：`Which of these would be caught by an integration test that uses two tenants?` 与 `What can someone with write access to the cache do?`

## 3. 怎么复核 AI 的发现

- **常见漏报**：缓存 key 缺租户（AI 常只盯 URL 授权，不看缓存层）；`limit=-1` 在 SQLite 里等于无限；`principal` 取到后没用这类"死变量"线索；diff 外的凭据存储。
- **常见假阳性**：把 `wsgiref` 单线程当 P0（PR 说明是 dev 服务器）；"缺少 CSRF"（只读 GET + header key，无 cookie）；"缺少 HTTPS"（部署层问题，评论里提一句即可）；对 `Cache` 里的 `threading.Lock` 提"可能死锁"。
- **复核方法**：每个安全发现要求一条可复现的请求（"用 acme 的 key 请求 `/tenants/globex/...`"）。写不出请求的发现降级。`acceptance/` 就是这些请求的集合。
- **优先级**：让 AI 按"跨租户泄露/RCE > 其他注入 > 可用性 > 正确性 > 风格"重排；注意 AI 常把 P1 的分页 bug 排到 P0 之前。

## 4. 评论怎么写（英文示例）

**P0（CR-01）**
> `app.py:47` **[P0 · tenant isolation]** `authenticate()` returns a `Principal` that is never used: any valid key can read any tenant's data by changing the tenant in the URL (e.g. an Acme key on `/tenants/globex/users/u1/risk`). Please compare `principal.tenant_id` with the tenant from the path in one shared `authorize()` helper and return 404 on mismatch so we don't reveal which tenants exist. A two-tenant test for each endpoint should be the default negative case.

**P1（CR-06）**
> `service.py:24` **[P1 · stampede]** When a hot key expires, every concurrent request misses and runs both queries. The console polls the same users, so we'll see DB spikes at each TTL boundary, and the spike gets worse when the DB is slow. Suggest a per-key lock with a re-check after acquiring it (and TTL jitter); across pods a short Redis `SET NX` lease does the same.

**nit（CR-10）**
> `app.py:44` **[nit]** The auth block is copy-pasted in both handlers. Not blocking by itself, but this duplication is how the tenant check got missed in both places; one `authorize()` would make the invariant hard to forget.

## 5. 60 秒口头总结模板

> "There are four blockers, and three of them are about tenant isolation. One: any valid API key can read any tenant's data, because we authenticate but never compare the key's tenant to the URL. Two: the cache key doesn't include the tenant, so even after fixing that, one tenant can be served another's cached score. Three: the `sort` parameter is interpolated into SQL in three places. Four: cache values are unpickled, so anyone who can write to the cache gets code execution in the API. Then the secondary issues: how API keys are hashed and compared, no single-flight on hot keys, an off-by-one in pagination, an unbounded limit, and emails in the logs. I'd block the merge on the four, with two-tenant tests, and happy to talk through how this holds up at ten times the traffic."

中文要点：先点明"主线 = 租户隔离" → 四个 P0 各一句 → 次要问题成组带过 → 合并条件 → 引向规模。
