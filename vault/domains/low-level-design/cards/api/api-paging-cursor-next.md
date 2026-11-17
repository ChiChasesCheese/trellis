---
id: api-paging-cursor-next
node: api.paging-iteration
type: qa
step: 2
---
## Q
分页接口要告诉调用方“还有没有下一页”。常见写法是返回满了 `limit` 条就当有下一页，什么情形下会错？怎么设计游标（cursor）和结束标志？

## A
**多取一条判断有没有下一页，游标只放位置**

- **“满页”不能说明还有下一页**：总数恰好是 `limit` 的整数倍，最后一页也是满的，调用方多请求一次，拿到空页；
- **多取一条**：`LIMIT limit + 1`，取到 `limit + 1` 条就说明还有，把多出的那条丢掉，游标取第 `limit` 条的键；
- **最后一页游标是 `None`**：调用方 `while cursor is not None` 就能停，不用猜；
- **游标只是位置**：里面是排序键，不带授权、不带查询条件；每一页重新检查所有者和筛选，客户端篡改游标最多是看到自己有权看的另一段；
- **对调用方不透明**：编码成字符串（如 base64 的 JSON），合同写“不要解析”，以后换成别的实现不破坏调用方。

```python
def page(rows: list[int], cursor: int | None, limit: int):
    start = [r for r in rows if cursor is None or r > cursor]
    got = start[:limit + 1]                        # 多取一条
    has_more = len(got) > limit
    items = got[:limit]
    return items, (items[-1] if has_more else None)

print(page([1, 2, 3, 4], None, 2))                 # ([1, 2], 2)
print(page([1, 2, 3, 4], 2, 2))                    # ([3, 4], None)：满页，但已经是最后一页
```

**知识点：**大结果集接口（Pagination & Iteration）
