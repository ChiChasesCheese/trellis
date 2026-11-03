---
id: craft-entity-vs-value-object-3-title-and-copy
node: craft.architecture.entity-vs-value-object
type: qa
step: 3
---
## Q
**实体 vs 值对象 · 图书馆里「书」其实是两样东西**｜架构

图书馆系统要支持：按书名搜索、借走某一册、有人想借的书全被借光时预约。如果只有一个 `Book` 类，搜索时同一部作品的三本副本会重复出现，预约也说不清是预约哪一本。怎么划分？

## A
**要点。** 拆成书目（Title，一部作品的著录信息，值）和副本（Copy，架上一本具体的书，实体）。搜索挂书目：同一部作品只出现一次；借还挂副本：借出的是这一本，有借阅人和归还时间；预约挂书目：想要的是这部作品，谁先遇到空副本谁拿。三个操作各挂在对的层级上，不需要补丁。

```python
@dataclass(frozen=True, slots=True)
class Title:                      # 值：一部作品的著录
    isbn: str
    name: str

@dataclass(eq=False)
class Copy:                       # 实体：架上一本具体的书
    copy_id: str
    title: Title
    borrower: str | None = None

class Library:
    def __init__(self) -> None:
        self.copies: dict[str, Copy] = {}
        self.holds: dict[Title, list[str]] = {}       # 预约挂在书目上
    def add(self, c: Copy) -> None:
        self.copies[c.copy_id] = c
    def search(self, text: str) -> list[Title]:       # 搜索挂书目：同一种书不重复出现
        return sorted({c.title for c in self.copies.values() if text in c.title.name}, key=lambda t: t.isbn)
    def available(self, t: Title) -> int:
        return sum(1 for c in self.copies.values() if c.title == t and c.borrower is None)
    def checkout(self, copy_id: str, who: str) -> None:   # 借还挂副本
        self.copies[copy_id].borrower = who
    def reserve(self, t: Title, who: str) -> None:        # 预约挂书目：谁先有空副本谁拿
        self.holds.setdefault(t, []).append(who)

lib = Library()
t = Title("978-1", "流畅的 Python")
lib.add(Copy("c1", t)); lib.add(Copy("c2", t))
print("搜索:", [x.name for x in lib.search("Python")], "可借:", lib.available(t))
lib.checkout("c1", "小王")
print("借走 c1 后可借:", lib.available(t))
lib.checkout("c2", "小李")
lib.reserve(t, "小张")
print("全借出后可借:", lib.available(t), "预约队列:", lib.holds[t])
```

两本副本，借出两次后再预约，实际输出：

```
搜索: ['流畅的 Python'] 可借: 2
借走 c1 后可借: 1
全借出后可借: 0 预约队列: ['小张']
```

**为什么。** 图书、DVD、期刊不需要三个子类：差别是字段叫什么（作者还是导演）、按什么政策借，而不是行为不同；期刊每一期是独立书目，名字相同、编号不同。

**信号。** 一个类上同时有「描述这个东西是什么」和「这个东西现在在谁手里」两类字段，就该拆。
