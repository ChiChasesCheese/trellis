---
id: data-value-entity-edit-makes-new
node: data.value-entity
type: qa
step: 3
---
## Q
审核服务里一条评论被编辑，写成 `comment.text = new_text`，旧的文本就丢了，审核记录里引用的评论也跟着变。值对象的“编辑”应该怎么做？

## A
**值对象不改，编辑就是造一个新值**

- **冻结**：`frozen=True`，赋值字段直接抛 `FrozenInstanceError`，误改在写代码时就暴露；
- **编辑 = `dataclasses.replace`**：基于旧值造新值，旧值原样保留，已经引用它的地方不受影响；
- **要审计就追加**：记录的不是“当前状态”，而是一串事件；违规、申诉、撤销都是新增事件，不改旧事件；当前状态由事件算出来；
- **代价**：每次编辑多一个对象；对象小、改动少时可以忽略，改动频繁的热点路径才需要换成可变；
- **哪里仍然可变**：实体（有 id、生命周期）可以可变，但它持有的值对象是冻结的，换整个值而不是改里面。

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Comment:
    id: int
    text: str

v1 = Comment(1, "hello")
v2 = replace(v1, text="hello, edited")
history = [v1, v2]                                 # 旧版本还在，审核记录可以指向 v1
print(v1.text, "->", v2.text, v1 is v2)
```

**知识点：**值对象与实体（Value vs Entity）
