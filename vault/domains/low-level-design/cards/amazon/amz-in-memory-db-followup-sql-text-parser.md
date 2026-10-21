---
id: amz-in-memory-db-followup-sql-text-parser
node: amazon.amz-in-memory-db
type: qa
step: 6
tags: [grown]
---
## Q
在内存数据库里，面试官要求支持 SQL 文本，要改哪里、不改哪里？AND 和 OR 的优先级怎么实现？

## A
只新增分词器和 `Parser`，把文本翻译成对 `Database` 的调用，`Table`、谓词、`select` 都不动。

优先级靠方法的调用层次：`OR` 在最外层，调用 `AND`，再调用 `NOT`，最里是比较，所以 `a = 1 OR a = 2 AND b = 'y'` 解析成 `a = 1 OR (a = 2 AND b = 'y')`。

```python
def expr(self):
    parts = [self.and_expr()]
    while self.accept("OR"):
        parts.append(self.and_expr())
    return parts[0] if len(parts) == 1 else Or(tuple(parts))

def not_expr(self):
    return Not(self.not_expr()) if self.accept("NOT") else self.atom()
```
