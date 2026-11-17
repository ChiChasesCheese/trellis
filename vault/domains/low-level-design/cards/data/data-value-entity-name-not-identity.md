---
id: data-value-entity-name-not-identity
node: data.value-entity
type: qa
step: 4
---
## Q
片单服务允许两个用户各有一个叫“周末”的片单，同一个用户也可以先删掉“周末”再新建一个。用名字当身份会出什么问题？id 又该怎么发，才不会出现“旧 id 指到新东西”？

## A
**名字是属性，id 才是身份，id 发出去就不再回收**

- **名字会撞、会改**：重名允许，改名不该换身份；用名字当键，改名要同时改所有引用；
- **id 由系统发**：调用方不指定，格式固定（自增整数或 UUID）；
- **id 不复用**：删掉 7 号再新建，新的不能叫 7；否则调用方手里的旧 7 号链接、缓存、日志里的引用会悄悄指到别的东西；
- **SQLite 的细节**：只有 `INTEGER PRIMARY KEY` 时，删掉最大的那行，下一个新行会复用它的 id；加 `AUTOINCREMENT` 才保证不复用；
- **合并也算**：两个账户合并后，被并掉的 id 永远不再发，查它要得到“已并入”的明确答案。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("create table a (id integer primary key, name text)")
db.execute("create table b (id integer primary key autoincrement, name text)")
for t in "ab":
    db.execute(f"insert into {t}(name) values ('x')")
    db.execute(f"delete from {t}")
    print(t, db.execute(f"insert into {t}(name) values ('y')").lastrowid)   # a 1  b 2
```

**知识点：**值对象与实体（Value vs Entity）
