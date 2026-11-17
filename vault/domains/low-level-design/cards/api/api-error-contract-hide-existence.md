---
id: api-error-contract-hide-existence
node: api.error-contract
type: qa
step: 4
---
## Q
用户 A 请求用户 B 的片单 `/lists/17`。服务返回 403 还是 404？这个选择为什么属于错误契约，而不是随手挑的？

## A
**别人的资源和不存在的资源，对外是同一个答案**

- **403 会泄露存在**：回 403 等于告诉调用方“17 号存在，只是不归你”；遍历 id 就能摸清别人的数据量；
- **404 对两种情形一致**：不存在、归别人，响应逐字节相同（同一个 `code`，同一个状态码）；
- **一个分支**：内存里像下面这样，两种情形进同一个 `if`；数据库里更好，把 owner 写进 `WHERE`，别人的行根本查不出来，耗时也分不出；
- **写进合同并测试**：一个测试用别人的 id，一个用不存在的 id，断言两个响应相等；
- **例外**：资源本身是公开的（调用方本来就知道它存在），那 403 是诚实的答案。

```python
LISTS = {17: ("bob", ["m1"])}

def get_list(user: str, list_id: int) -> tuple[int, dict]:
    row = LISTS.get(list_id)
    if row is None or row[0] != user:             # 两种情形走同一个分支
        return 404, {"error": "list_not_found"}
    return 200, {"movies": list(row[1])}

print(get_list("amy", 17) == get_list("amy", 99))   # True，外面分不出
print(get_list("bob", 17))
```

<details class="pt"><summary>延伸</summary>

写操作要一起守：删除、改名也先按 owner 过滤，别人对 17 号的 DELETE 同样得到 404，并且不能删掉任何东西。条件更新没命中时，复查也要带 owner，否则“复查发现在”会把别人的行暴露成 409。

</details>

**知识点：**接口的错误契约（Error Contract）
