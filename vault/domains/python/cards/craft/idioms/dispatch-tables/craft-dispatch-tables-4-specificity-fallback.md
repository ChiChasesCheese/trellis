---
id: craft-dispatch-tables-4-specificity-fallback
node: craft.idioms.dispatch-tables
type: qa
step: 4
---
## Q
**分派表 · 按（读者类型，介质）查政策，缺省怎么回退**｜写法

图书馆的借阅规则由读者类型和介质共同决定：默认 14 天，教职工 30 天，所有人的 DVD 3 天。有人写成一串 `if member is STAFF and kind is DVD ...`。用表驱动之后，规则可以怎样组织？当两条规则同时命中谁优先？

## A
**要点。** 表的键用元组，`None` 表示「任意」。查找从最具体到最粗依次试：`(类型, 介质)`、`(类型, None)`、`(None, 介质)`，最后才是默认值，第一个命中的就是答案。新增一种读者或介质只是加一行数据，借还流程不动。

```python
from dataclasses import dataclass, field
from enum import Enum

class Member(Enum): STUDENT = 1; STAFF = 2
class Media(Enum): BOOK = 1; DVD = 2

@dataclass(frozen=True)
class Loan:
    days: int = 14
    max_items: int = 5

@dataclass(frozen=True)
class PolicyTable:
    default: Loan = Loan()
    overrides: dict[tuple[Member | None, Media | None], Loan] = field(default_factory=dict)
    def resolve(self, m: Member, k: Media) -> Loan:
        for key in ((m, k), (m, None), (None, k)):      # 从最具体到最粗
            found = self.overrides.get(key)
            if found is not None:
                return found
        return self.default

t = PolicyTable(overrides={
    (Member.STAFF, None): Loan(days=30),                # 教职工所有介质 30 天
    (None, Media.DVD): Loan(days=3),                    # 所有人的 DVD 3 天
})
print(t.resolve(Member.STUDENT, Media.BOOK).days)
print(t.resolve(Member.STAFF, Media.BOOK).days)
print(t.resolve(Member.STUDENT, Media.DVD).days)
print(t.resolve(Member.STAFF, Media.DVD).days)          # 两条都命中
t2 = PolicyTable(overrides={**t.overrides, (Member.STAFF, Media.DVD): Loan(days=7)})
print(t2.resolve(Member.STAFF, Media.DVD).days)
```

实际输出：

```
14
30
3
30
7
```

**为什么。** 第四行说明两条规则同时命中时，读者类型的规则排在介质规则前面，这是查找顺序里写死的约定，要在文档里说清；最后一行加了一行 `(STAFF, DVD)`，更具体的键立即胜出，没有改任何流程代码。

**代价。** 表不擅长「规则互相依赖」「要解释为什么这样判」。规则一多，同时命中的优先级会变成隐含知识；那时要给规则显式的优先级字段，或者每次返回命中的是哪一条，便于排查。
