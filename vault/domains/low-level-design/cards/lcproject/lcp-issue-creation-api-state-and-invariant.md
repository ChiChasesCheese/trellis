---
id: lcp-issue-creation-api-state-and-invariant
node: lcproject.lcp-issue-creation-api
type: qa
step: 2
tags: [作答]
---
## Q
在项目工单服务里，成员表、每个项目的工单、幂等键的回执、全局 id 计数器都放在内存里，多个线程同时调用。要存哪些状态？每部分用什么结构？哪条不变量最要紧，什么会打破它？

## A
**评分点**
- 说出成员表构造时复制并冻结：之后改传入的集合不影响授权
- 说出每个项目一份状态：工单列表按 id 升序追加（id 全局递增所以天然有序）、按 id 查找的字典，查找只在本项目内，天然隔离
- 说出回执表按 (用户, 键) 存"规范化后的请求加工单引用"：比较就是值相等，重放看到的是最新状态
- 说出最要紧的不变量：同一范围内一个键至多对应一张工单，所以"查键、分配 id、追加、记回执"必须在同一个临界区里
- 说出打破它的做法：不加锁或分两步加锁、先自增 id 再检查冲突、`get` 不加锁读到状态已改版本未加的半截
- 说出对外只给字典快照，不交出内部对象

<details class="pt"><summary>参考答案</summary>

状态：冻结的成员表；每个项目一个 `Board`（升序工单列表、id 字典、(用户, 键)→回执）；一个全局 id 计数器；一把锁。最要紧的不变量：一个键在一个范围内至多对应一张工单、id 序列没有洞。它靠"查键、分配 id、追加、记回执"在一个临界区里，并且所有可能抛错的检查都在第一次写之前来保证；读也要在锁里，返回的都是快照。

```python
with self._lock:
    existing = board.replay(user, key, request)   # 可能抛 409
    if existing is not None:
        return 200, existing.snapshot()
    issue = Issue(self._next_id, project, user, request.title, request.description)
    self._next_id += 1                            # 此后不再有会抛错的语句
    board.add(issue, key, request)
```

</details>

**知识点：** 复合操作（Compound Actions）、防御性拷贝（Defensive Copying）、不变量与封装（Invariants）
