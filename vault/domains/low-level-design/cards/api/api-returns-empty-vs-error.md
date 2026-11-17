---
id: api-returns-empty-vs-error
node: api.returns
type: qa
step: 1
---
## Q
`recommend(user, limit)` 在目录为空、或者用户已经看完所有片子时没有东西可推荐。该返回 `[]`、返回 `None`，还是抛 `NoResults`？为什么？

## A
**“没有结果”是正常答案，返回空容器**

- **空是合法的结果**：调用方的下一行通常是 `for x in result`，`[]` 让循环零次，不需要任何特判；
- **`None` 逼调用方写分支**：忘了判断就是 `TypeError: 'NoneType' object is not iterable`，而且只在没数据的那天爆；
- **异常留给“请求本身有问题”**：用户不存在、`limit` 非法是错误；用户存在但没东西可推荐不是；
- **类型保持一致**：返回列表的函数任何分支都返回列表，每次新建，不要把一个模块级的 `[]` 到处共享；
- **候选不够就少给**：要 10 个只有 3 个，返回 3 个，不补假数据，也不报错。

```python
def recommend(seen: set[int], catalog: list[int], limit: int) -> list[int]:
    return [m for m in catalog if m not in seen][:limit]

print(recommend({1, 2}, [1, 2], 5))        # []
print(recommend({1}, [1, 2, 3], 5))        # [2, 3]，不够也不补
for m in recommend(set(), [], 5):          # 空结果不需要特判
    print(m)
```

**知识点：**返回值设计（Return Values）
