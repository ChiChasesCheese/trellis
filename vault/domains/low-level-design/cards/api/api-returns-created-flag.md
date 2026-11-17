---
id: api-returns-created-flag
node: api.returns
type: qa
step: 6
---
## Q
`add_movie(list_id, movie_id)` 重复添加同一部电影，应该怎么告诉调用方“这次真加了”还是“本来就在”？为什么 `set.add` 的写法在接口设计上是个反面例子？

## A
**写操作要返回“这次到底发生了什么”**

- **`set.add` 返回 `None`**：调用方想知道元素是否新增，只能先 `in` 再 `add`，两步之间别人可能插进来；
- **返回布尔**：`True` 表示这次新增，`False` 表示本来就在；幂等的操作仍然成功，只是告诉调用方没变；
- **适配层据此选状态码**：新增 201，已存在 200；不是错误，所以不抛异常；
- **更新、创建类操作**：返回改后的对象，调用方不必再读一次，也避免读到别人的后续修改；
- **删除**：返回是否真的删了，或者对不存在的目标明确报 `NotFound`，二选一写进合同。

```python
class Watchlist:
    def __init__(self): self._movies: set[int] = set()
    def add(self, movie_id: int) -> bool:
        if movie_id in self._movies:
            return False
        self._movies.add(movie_id)
        return True

w = Watchlist()
print(w.add(7), w.add(7))                       # True False
print({1}.add(1))                               # None：标准库的 set.add 不告诉你
status = 201 if w.add(8) else 200
```

<details class="pt"><summary>延伸</summary>

并发下“先查再加”两步会被打断；返回值本身要来自同一个原子操作：SQL 用 `INSERT OR IGNORE` 再看 `cursor.rowcount`，内存里用同一把锁包住判断和添加。

</details>

**知识点：**返回值设计（Return Values）
