---
id: problems-library-policy-table-not-inheritance
node: problems.booking.library
type: qa
step: 7
tags: [grown]
---
## Q
图书馆管理（Library Management）要让借阅上限、借期、续借次数、罚金费率、留架天数随读者类型（学生／教师／公众）和介质（图书／DVD／期刊）变化。用 `Member` 的继承树、`if` 分支，还是别的？

## A
用一张按 `(读者类型, 介质)` 查、允许退化的**政策表**：

```python
def resolve(self, member_type: MemberType, kind: MediaKind) -> LoanPolicy:
    for key in ((member_type, kind), (member_type, None), (None, kind)):
        found = self.overrides.get(key)
        if found is not None:
            return found
    return self.default
```

- **继承树的代价**：读者类型是会变的（学生毕业成校友），而 Python 里给对象换类是件脏事；更本质的是，类型只是一个**属性**，不是他的种类——用继承表达属性是最典型的误用。
- **`if` 分支的代价**：维度一多就是笛卡尔积，而且分支会散落在借、还、续借、分配四个地方，改一处漏三处。

表的收益是可验证的：加「教师借 DVD 可以借 7 天」＝加一个键；加一种介质＝枚举加一个成员；加第三个维度＝键变三元组、`resolve` 多循环一档。**流程代码一行不动。**

它不需要模式的名字：策略里没有算法只有一组数字时，就让它只是数据。
