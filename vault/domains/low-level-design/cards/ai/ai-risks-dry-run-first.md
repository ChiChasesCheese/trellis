---
id: ai-risks-dry-run-first
node: ai.risks
type: qa
step: 1
---
## Q
要修复生产库里的脏数据（比如超额预订的场次）。为什么先在副本上演练、读差异、再应用？一个演练该产出什么？

## A
**复制、迁移副本、读差异、丢弃**

- **演练要真做迁移**：在生产的副本上跑同一段迁移，约束建不起来这类失败在这一步就能暴露；只打印“计划”发现不了；
- **读差异**：几行被改、涉及哪些记录、有没有意外的行，数字和你预期的对一遍；
- **本地快照可能只是节选**：快照里没有的行，演练里也不会出现；演练通过只说明迁移能跑；
- **应用由人确认**：脚本里的提示拦不住智能体（它也能传参数），拦得住的是权限和你按下的那一步；
- **应用之后**：只读检查一致性，再运行一次迁移，应当什么都不再改。

```python
import sqlite3

prod = sqlite3.connect(":memory:")
prod.executescript("create table slot(id integer primary key, free int);"
                   "insert into slot values (1, 5), (2, -1), (3, 0);")
rehearsal = sqlite3.connect(":memory:")
prod.backup(rehearsal)                                    # 复制生产
before = rehearsal.execute("select * from slot").fetchall()
rehearsal.execute("update slot set free = 0 where free < 0")
after = rehearsal.execute("select * from slot").fetchall()
print([(b, a) for b, a in zip(before, after) if b != a])  # [((2, -1), (2, 0))]
print(prod.execute("select free from slot where id = 2").fetchone())    # (-1,) 生产没动
```

**知识点：**风险与权限（Risks & Guardrails）
