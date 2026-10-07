# REPORT · cr02 risk API

> 子代理在写 REPORT 前因用量上限中断；本文件由编排者根据仓库实测补写。

## 规模（命令实测）

| 项 | 数字 |
|---|---|
| starter Python 行数（含测试） | 602（`find starter -name '*.py' \| xargs wc -l`） |
| solution Python 行数 | 702 |
| starter 自带测试 | 17 个，全绿 |
| solution 自带测试 | 20 个，全绿 |
| `pr.diff` | 454 行，13 个文件 |
| acceptance | 24 个测试：core 9 · stretch 10 · regression 5（`pytest --collect-only -m <marker>`） |

## 问题分布

13 条：P0 4（CR-01 IDOR · CR-02 `sort` 拼 SQL · CR-03 缓存用 `pickle` · CR-04 缓存 key 不含租户）· P1 5（CR-05 无盐 MD5 + `==` 比较 · CR-06 缓存击穿 · CR-07 分页 `>=` 重复一条 · CR-08 `limit` 无上下限 · CR-09 日志打印 email）· P2 4（CR-10 复制粘贴的认证与魔法下标 · CR-11 错误形状不统一 / 500 泄露异常 · CR-12 缓存无容量与失效 · CR-13 只有 happy-path 测试）。CR-05 的一半在 diff 外（`db.py` 的建表与 `create_api_key`），考察是否看上下文。完整表见 `REVIEW_KEY.md`。

## 验收

编排者 gate（`tools/verify_suites.py`，2026-10-07）：acceptance/solution 24 passed · starter `-m core` 9 failed（0 passed）· starter 自带 17 passed · solution 自带 20 passed → **OK**。

## 每个 P0 的"为什么是 P0"

- **CR-01 IDOR**：任何有效 key 读任何租户的风险分——安全产品里的跨租户数据泄露，利用成本为零。
- **CR-02 SQL 注入**：`sort` 来自 query string，可读任意表；也会让正常但带特殊字符的输入报 500。
- **CR-03 pickle**：缓存一旦被写入恶意值即远程代码执行；修法简单（JSON），不修的理由不存在。
- **CR-04 缓存 key 不含租户**：user_id 在租户间重复 → 把 A 租户的分数返回给 B 租户；静默错误，监控看不出来。
