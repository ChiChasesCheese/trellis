---
id: api-paging-keyset-vs-offset
node: api.paging-iteration
type: qa
step: 1
---
## Q
片单有几万部电影，分页接口写成 `LIMIT 20 OFFSET 40`。翻页的过程中有人在前面加了一部电影，调用方会看到什么？“键集分页”（keyset pagination）为什么没有这个问题？

## A
**页界按位置算会漂，按“上一页最后一个键”算不会**

- **偏移分页（offset）**：第 3 页是“跳过前 40 条”；前面插入一条，原来第 40 条变成第 41 条，下一页的第一条是上一页已经给过的，重复了；前面删一条则漏一条；
- **键集分页**：`WHERE id > :last ORDER BY id LIMIT 20`，条件是“大于上一页最后一个 id”，与前面发生了什么无关；
- **严格大于**：用 `>` 而不是 `>=`，上一页最后一条不会再出现；
- **要求有稳定的、唯一的排序键**：按评分排序时，加上 id 作为第二列 `(score, id)`，否则同分的行页界不确定；
- **代价**：不能直接“跳到第 N 页”，只能顺着往后走；对大列表这是可以接受的。

```python
ids = list(range(1, 11))

def offset_page(rows, off, n): return rows[off:off + n]
def keyset_page(rows, last, n): return [r for r in rows if r > last][:n]

p1 = offset_page(ids, 0, 4)                       # [1,2,3,4]
ids.insert(0, 0)                                  # 翻页途中前面插入一条
print(offset_page(ids, 4, 4))                     # [4,5,6,7]：4 重复了
print(keyset_page(ids, p1[-1], 4))                # [5,6,7,8]
```

**知识点：**大结果集接口（Pagination & Iteration）
