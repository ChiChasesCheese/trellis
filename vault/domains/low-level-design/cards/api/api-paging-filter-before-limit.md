---
id: api-paging-filter-before-limit
node: api.paging-iteration
type: qa
step: 3
---
## Q
工单列表支持按状态过滤和 `limit`。实现先取 `limit` 条再过滤，调用方会看到什么？过滤、排序、游标、截断的顺序应该是什么？

## A
**先过滤、再排序、再用游标定位、最后截断**

- **先截断再过滤**：取 20 条，过滤掉 15 条，只剩 5 条，调用方以为到末尾了，其实后面还有大量匹配的行；
- **正确顺序**：筛选 → 稳定排序 → `> 游标` → 取 `limit` 条；SQL 里就是 `WHERE` 与 `ORDER BY` 在 `LIMIT` 前面，顺序天然正确；
- **内存里分页最容易写反**：`rows[:limit]` 放在过滤前面，是常见的错；
- **参数边界写进合同**：`limit` 的上下限（1 到 100）、越界是 400 而不是静默夹成 100；游标格式不对也是 400；
- **页与页之间的状态变化**：遍历中新增的行可以出现也可以不出现，但已经返回过的行不能再出现、没被删的行不能漏。

```python
issues = [(1, "open"), (2, "closed"), (3, "closed"), (4, "open"), (5, "open")]

def wrong(status, limit): return [i for i in issues[:limit] if i[1] == status]
def right(status, limit): return [i for i in issues if i[1] == status][:limit]

print(wrong("open", 3))                            # [(1, 'open')]：后面明明还有
print(right("open", 3))                            # [(1, 'open'), (4, 'open'), (5, 'open')]
```

**知识点：**大结果集接口（Pagination & Iteration）
