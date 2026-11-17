---
id: debugging-reproduce-failing-test
node: debugging.reproduce
type: qa
step: 1
---
## Q
用户反馈“从片单里移除一部电影，整个片单的其他电影都没了”。别急着读代码，第一步该做什么？写好的测试怎么确认它抓的是这个缺陷，而不是随便红了？

## A
**先把症状写成一个会失败的测试，并确认它红得有理由**

- **复现是最小的、自动的**：几行建好数据、调一次函数、断言一个结果；不用手点页面、不靠记忆；
- **只描述症状，不预设原因**：断言“其他电影还在”，不写“条件应该是 `=`”；
- **在原代码上跑一遍，看红的信息**：失败信息要正好是用户说的现象（别的电影不见了）；如果红在别处（建表出错、拼写错），它证明不了任何事；
- **修好以后同一个测试变绿**：这才是“修了这个缺陷”的证据；一开始就是绿的测试，什么也没证明；
- **保留它**：它成为回归测试，下次有人改这段代码会被它拦住。

```python
import sqlite3

def remove(db, pid, mid):                       # 起始代码
    db.execute("DELETE FROM m WHERE pid=? AND mid<>?", (pid, mid))

def test_remove_keeps_the_others():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE m(pid, mid)")
    db.executemany("INSERT INTO m VALUES(?,?)", [(1, "a"), (1, "b"), (2, "a")])
    remove(db, 1, "a")
    left = sorted(db.execute("SELECT * FROM m"))
    assert left == [(1, "b"), (2, "a")], f"剩下 {left}"

try: test_remove_keeps_the_others()
except AssertionError as e: print("红：", e)    # 红： 剩下 [(1, 'a'), (2, 'a')]
```

红的信息告诉你：被删掉的是 `b`，留下的反而是要删的 `a`，条件写反了。

**知识点：**稳定复现（Reproduce）
