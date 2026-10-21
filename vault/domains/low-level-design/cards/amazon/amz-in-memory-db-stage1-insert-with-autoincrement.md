---
id: amz-in-memory-db-stage1-insert-with-autoincrement
node: amazon.amz-in-memory-db
type: qa
step: 3
tags: [grown]
---
## Q
在内存数据库里，带自增主键的插入怎么写，才能做到「删除后行号不回退」？

## A
行存在 `{主键: 行}` 字典里，行号来自一个只增不减的计数器 `next_id`，而不是「当前行数 + 1」：

```python
def insert(self, values):
    row = {c: values.get(c) for c in self.columns}
    if row[self.pk] is None and self.columns[self.pk] is int:
        row[self.pk] = self.next_id
    row = {c: self.check(c, v) for c, v in row.items()}
    pk = row[self.pk]
    if pk in self.rows:
        raise ConstraintError(f"主键 {pk!r} 重复")
    self.rows[pk] = row
    self.next_id = max(self.next_id, pk + 1)
    return pk
```
先插入得 1、2、3，删掉 3，再插入得 4。
