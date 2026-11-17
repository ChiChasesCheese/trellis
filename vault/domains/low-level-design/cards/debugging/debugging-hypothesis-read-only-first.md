---
id: debugging-hypothesis-read-only-first
node: debugging.hypothesis
type: qa
step: 4
---
## Q
线上有一批预约状态不对，你要设计修复。在动任何东西之前，应该怎么看生产数据？要把这个问题交给 AI 编程助手时，先给它什么？

## A
**先用只读账号看数据，把假设验证了，再设计修复**

- **查询也是实验**：它不改世界，能验证假设，成本最低；
- **用只读角色或只读连接**：不是靠自己小心，而是让写操作在权限上就做不到；
- **先数一数范围**：多少行受影响、集中在哪些条件下、从什么时间开始；这些数字直接决定修复怎么设计；
- **给助手的是症状、假设、待验证的检查**：不是一句“帮我修”；它拿到的假设和证据越具体，越不会去改对的代码；
- **把已经正确的行为也交代给它**：“这几个函数是对的，别动”，修缺陷时才不会顺手破坏它们。

```python
import os, sqlite3, tempfile

path = os.path.join(tempfile.mkdtemp(), "prod.db")
w = sqlite3.connect(path)
w.execute("CREATE TABLE r(id, status)"); w.execute("INSERT INTO r VALUES(1, 'canceled')")
w.commit(); w.close()

ro = sqlite3.connect(f"file:{path}?mode=ro", uri=True)       # 只读连接
print(ro.execute("SELECT status, COUNT(*) FROM r GROUP BY status").fetchall())
try: ro.execute("UPDATE r SET status='cancelled'")
except sqlite3.OperationalError as e: print("写被拒绝：", e)
```

**知识点：**假设驱动（Hypothesis-Driven）
