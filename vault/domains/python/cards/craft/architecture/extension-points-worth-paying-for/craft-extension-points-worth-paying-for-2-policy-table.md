---
id: craft-extension-points-worth-paying-for-2-policy-table
node: craft.architecture.extension-points-worth-paying-for
type: qa
step: 2
---
## Q
**值得付费的扩展点 · 图书馆的借阅规则，为什么写成「查表」而不是 if member.type 分支**｜架构

借阅规则按读者类型（学生、教职工、公众）和介质（书、DVD）不同：能借几天、几本、逾期罚多少。图书馆后来加了一条「教职工借 DVD 可以借 21 天」。写成 `if member.type is STAFF and kind is DVD` 的分支，和写成一张按 (读者类型, 介质) 查询的政策表，成本差在哪？

## A
**要点。** 分支把规则散在借还流程里，每加一条规则就改一次流程，规则之间的优先关系只能靠读代码顺序去猜。政策表把规则变成数据：一个键对应一行政策，查找从最具体到最粗，先命中的就是答案，找不到退回默认。加规则只是加一个键，借还流程不动。

```python
class Member(Enum):
    STUDENT = "student"; STAFF = "staff"
class Media(Enum):
    BOOK = "book"; DVD = "dvd"

@dataclass(frozen=True)
class LoanPolicy:
    loan_days: int = 14
    max_loans: int = 5

@dataclass(frozen=True)
class PolicyTable:
    default: LoanPolicy = LoanPolicy()
    overrides: dict = field(default_factory=dict)

    def resolve(self, m: Member, k: Media) -> LoanPolicy:
        for key in ((m, k), (m, None), (None, k)):       # 从最具体到最粗
            if (found := self.overrides.get(key)) is not None:
                return found
        return self.default

t = PolicyTable(overrides={(None, Media.DVD): LoanPolicy(loan_days=7)})
print("学生借书:", t.resolve(Member.STUDENT, Media.BOOK).loan_days)
print("学生借 DVD:", t.resolve(Member.STUDENT, Media.DVD).loan_days)

# 新规则：教职工借 DVD 可以借 21 天，只加一个键
t.overrides[(Member.STAFF, Media.DVD)] = LoanPolicy(loan_days=21)   # 新规则：只加一个键
print("教职工借 DVD:", t.resolve(Member.STAFF, Media.DVD).loan_days, "| 学生借 DVD 不变:", t.resolve(Member.STUDENT, Media.DVD).loan_days)
```

默认借期 14 天；所有 DVD 7 天；加入教职工借 DVD 21 天之前和之后，实际输出：

```
学生借书: 14
学生借 DVD: 7
教职工借 DVD: 21 | 学生借 DVD 不变: 7
```

**为什么。** 查找顺序（具体优先于笼统）本身就是规则优先级，写在一处，可以单独测试；`None` 表示「不限」，所以新增读者类型或介质也不会破坏已有的键。

**易错。** 表的键如果允许任意组合，查找顺序要明确写进文档并有测试覆盖，否则两条同样具体的规则（读者类型 + 介质 对 读者类型 + 区域）冲突时，结果取决于遍历顺序。
