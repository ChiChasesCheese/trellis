---
id: performance-cc-n-plus-one
node: performance.complexity-constants
type: qa
step: 6
---
## Q
接口先查出 1000 个 id，再对每个 id 单独执行一次 `SELECT ... WHERE id = ?`。代码里没有一处算法上的问题，为什么它仍然是瓶颈？该怎么改？

## A
**真正的瓶颈常在 I/O 次数，不在循环里的计算**

- **N+1 查询**：1 次拿 id、再 N 次逐个查；每次查询都有固定开销（解析、调度、网络往返）；
- **一次批量取回**：`WHERE id IN (...)`，固定开销只付一次；
- **本机数据库没有网络往返，差距仍然是 10 倍**：生产里每次查询再多一次往返，差距更大；
- **IN 的参数个数有上限**：SQLite 默认最多 32766 个参数（3.32 起），其他数据库各有限制；超过就分批，每批几百到几千个；
- **同样的道理适用于所有 I/O**：文件、HTTP 请求、RPC，凡是“循环里发一次请求”都要想一想能不能合并成一次。

实测（3.11，本机，SQLite 文件数据库，10 万行，随机取 1000 个 id）：逐个查询 2.70 ms，一次 `IN` 0.27 ms。

```python
import sqlite3

c = sqlite3.connect(":memory:")
c.execute("create table m(id integer primary key, t text)")
c.executemany("insert into m values(?, ?)", [(i, f"t{i}") for i in range(100)])
ids = [3, 7, 42]

one_by_one = [c.execute("select t from m where id=?", (i,)).fetchone()[0] for i in ids]

marks = ",".join("?" * len(ids))
batched = dict(c.execute(f"select id, t from m where id in ({marks})", ids))
print(one_by_one, [batched[i] for i in ids])     # ['t3', 't7', 't42'] 两次结果一致
```

<details class="pt"><summary>延伸</summary>

批量取回的结果顺序不保证和传入的 id 一致，需要按 id 重新对齐，如上面最后一行；缺失的 id 也要决定是报错还是跳过。

</details>

**知识点：**复杂度与常数（Complexity vs Constants）
