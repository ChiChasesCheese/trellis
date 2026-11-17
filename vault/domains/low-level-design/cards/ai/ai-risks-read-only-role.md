---
id: ai-risks-read-only-role
node: ai.risks
type: qa
step: 2
---
## Q
设计修复之前，要让智能体看生产数据。给它什么权限？为什么不是“让它小心点”？

## A
**能写的权限不给，只读连接先看数据**

- **自觉不是控制**：提示词里的“不要写”、脚本里的确认开关，智能体都可以绕过，一次误操作就是真的写入；
- **权限才是控制**：数据库只读角色，或只读的连接；即使它执行了写语句，数据库也会拒绝；
- **先看数据再设计**：用只读连接查实际的重复、异常行，有了数据，修复才不是猜的；
- **写权限单独给**：应用迁移用另一个连接，由你执行，并且在变更记录写好之后。

```python
import os, sqlite3, tempfile

path = os.path.join(tempfile.mkdtemp(), "app.db")
w = sqlite3.connect(path); w.execute("create table t(x)"); w.commit(); w.close()

ro = sqlite3.connect(f"file:{path}?mode=ro", uri=True)    # 只读连接
print(ro.execute("select count(*) from t").fetchone())    # (0,)
try: ro.execute("insert into t values (1)")
except sqlite3.OperationalError as e: print(e)            # attempt to write a readonly database
```

<details class="pt"><summary>延伸</summary>

生产库用的是别的数据库时同理：建一个只授予 `SELECT` 的角色给读场景用。这条是权限的基本做法，不是某个库的特性。

</details>

**知识点：**风险与权限（Risks & Guardrails）
