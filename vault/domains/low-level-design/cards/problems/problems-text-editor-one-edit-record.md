---
id: problems-text-editor-one-edit-record
node: problems.components.text-editor
type: qa
step: 3
tags: [grown]
---
## Q
文本编辑器的撤销要用命令模式（Command）。很多实现会写 `InsertCommand`／`DeleteCommand`／`ReplaceCommand`／`CompositeCommand` 四个类加一个抽象基类。在 Python 里有没有更好的形状？

## A
有：一个冻结 dataclass 就够了，因为这三种操作本来是同一种——一次 splice。插入是把 `""` 换成新文本，删除是把旧文本换成 `""`，替换是两边都非空。

```python
@dataclass(frozen=True, slots=True)
class Edit:
    position: int
    removed: str
    inserted: str
    cursor_before: int
    cursor_after: int

    def invert(self) -> "Edit":
        return Edit(self.position, self.inserted, self.removed,
                    self.cursor_after, self.cursor_before)
```

逆操作退化成一次字段对调：没有分支、没有多态、没有"这个子类的 undo 写对了吗"。`CompositeCommand` 也不必要——一个撤销单元就是一个 `tuple[Edit, ...]`。真正需要命令类的场合是每条命令执行**不同的业务逻辑**（转账、发邮件），那时多态才有内容可承载。
