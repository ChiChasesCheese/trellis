---
id: api-hard-to-misuse-scope-in-query
node: api.hard-to-misuse
type: qa
step: 4
---
## Q
仓储接口提供 `get(item_id)`，每个调用点自己再检查 `item.owner == user`。第 12 个调用点忘了检查，会怎样？接口怎么设计才让“忘了检查”这件事不可能发生？

## A
**把授权条件做进接口的参数，不要靠每个调用点记得**

- **“先取再检查”靠自觉**：N 个调用点里只要有一个漏掉，别人的数据就能被读、改、删；
- **owner 变成必填参数**：`get(owner, item_id)`，没有不带 owner 的版本，漏写就是 `TypeError`；
- **查询里带条件**：`WHERE id = ? AND owner = ?`，别人的行根本查不出来，不存在与别人的是同一种结果；
- **写操作同理**：更新、删除都带 owner；条件更新没命中，复查也带 owner；
- **没有后门**：把无作用域的 `get_unscoped` 放在一个单独的、名字吓人的内部类里，只给迁移脚本用。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("create table item(id integer primary key, owner text, name text);"
                 "insert into item values (1, 'ann', 'saw');")

def get(owner: str, item_id: int):
    return db.execute("select name from item where id = ? and owner = ?", (item_id, owner)).fetchone()

print(get("ann", 1), get("bob", 1))           # ('saw',) None：bob 的结果和“不存在”一样
try: get(1)
except TypeError as e: print("must name an owner")
```

**知识点：**难以用错的接口（Hard to Misuse）
