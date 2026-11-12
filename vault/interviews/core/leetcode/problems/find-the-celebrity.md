---
slug: find-the-celebrity
---
## Q
**LC 277 搜寻名人**｜Medium

`n` 个人中，名人是所有人都认识、自己谁都不认识的人。只能调用 `knows(a, b)`，找出名人编号，没有返回 `-1`。

## A
**一句话。** 先淘汰出唯一候选：候选人认识 `i` 就换成 `i`；再完整验证候选人，共不超过 `3n` 次提问。

```python
def find_celebrity(n):
    cand = 0
    for i in range(1, n):
        if knows(cand, i):     # cand 认识 i，cand 不是名人
            cand = i
    for i in range(n):         # 验证：人人认识他，他谁也不认识
        if i == cand:
            continue
        if knows(cand, i) or not knows(i, cand):
            return -1
    return cand
```

**复杂度。** 时间 `O(n)`（提问至多 `3n` 次），空间 `O(1)`。

**易错点。**
- 只验证一个方向：`[[1,1,1],[1,1,0],[1,1,1]]` 里 `1` 认识 `0`，得 `1`，应为 `-1`。
- 候选人不验证就返回：淘汰只说明别人不是名人，`[[1,0,1],[1,1,0],[0,1,1]]` 会返回 `2`，应为 `-1`。
- 验证时问 `knows(cand, cand)`：`graph[i][i]=1` 会误判为认识别人。

**追问。**
- 为什么淘汰一轮就够？：每次提问必淘汰一人（认识则 `cand` 出局，不认识则 `i` 出局），`n-1` 次剩一人。
- 怎么省重复提问？：给 `knows` 加缓存，同一对不重复问。

**同模式。** LC 997 找到小镇的法官、LC 169 多数元素、LC 229 多数元素 II
