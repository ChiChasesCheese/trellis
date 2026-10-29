---
id: uth-compose-orm-session-3-core-code
node: compose.orm-session
type: qa
step: 3
---
## Q
**身份映射 + 工作单元的最小实现**｜SQLAlchemy · 2.0.55（简化）

把 Session 写成一个 Python 类：每个操作改哪些结构？flush 按什么顺序写？

## A
**不变量。**

- 身份映射里，同一个 `(类, 主键)` 至多一个对象
- `new` 里的对象还没有主键，不在身份映射里；`flush` 给它主键之后才登记
- `flush` 之前不发任何 SQL；`flush` 之后三个集合全部清空

**顺序。** 先 INSERT（先 `add` 的在前，所以父对象要先 `add`），再 UPDATE，最后 DELETE。SQLAlchemy 的源码注释写着 keep saves before deletes，Hibernate 的动作队列也是先插入、再更新、最后删除。

```python
class Session:
    def __init__(self, db: "Db") -> None:
        self.db = db
        self.identity: dict[tuple[type, int], "Entity"] = {}   # (类, 主键) -> 唯一的对象
        self.new: list["Entity"] = []                          # 待 INSERT，按加入顺序
        self.dirty: set["Entity"] = set()                      # 已加载且被改过，待 UPDATE
        self.deleted: set["Entity"] = set()                    # 待 DELETE

    def get(self, cls: type, pk: int) -> "Entity | None":
        key = (cls, pk)
        if key not in self.identity and (row := self.db.select(cls, pk)):
            self.identity[key] = cls(session=self, **row)      # 第一次见到才建对象
        return self.identity.get(key)                          # 之后永远是同一个对象

    def add(self, obj: "Entity") -> None:
        self.new.append(obj)

    def delete(self, obj: "Entity") -> None:
        self.deleted.add(obj)

    def touch(self, obj: "Entity") -> None:                    # 对象的 __setattr__ 调用它
        if obj not in self.new:                                # 新对象本来就要 INSERT
            self.dirty.add(obj)

    def flush(self) -> None:
        for obj in self.new:                                   # 1. INSERT，拿到主键后登记
            self.identity[(type(obj), self.db.insert(obj))] = obj
        for obj in self.dirty - self.deleted:                  # 2. UPDATE，要删的不必更新
            self.db.update(obj)
        for obj in self.deleted:                               # 3. DELETE
            self.db.delete(obj)
            self.identity.pop((type(obj), obj.id), None)
        self.new, self.dirty, self.deleted = [], set(), set()
```

**坑。** 真实的对象靠属性赋值时的钩子（SQLAlchemy 的属性事件）调用 `touch`；这里假设实体的 `__setattr__` 会调用它。

**对应 LeetCode：** 无直接对应的题
