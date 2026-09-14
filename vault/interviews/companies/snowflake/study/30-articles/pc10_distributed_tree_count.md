# pc10 · Distributed Tree Count：练的是"把'等所有孩子回复'建模成一个计数器"

> [!tldr]
> - Part 1 按来源题面实现，逐字复现来源样例的 9 行轨迹；**Part 2 丢消息、重试一次、放弃后部分计数是 (reconstructed)**；`REPORT <v>` 的逐字格式来源未给出，本题自定
> - 这题考的是：节点之间只能发消息，统计整棵树有多少节点，并按投递顺序记录日志
> - 三步套路：建孩子表（升序）+ 判环 → 全局 FIFO 队列模拟信道 → 每个节点一个 `pending` 计数，归零就上报
> - 最值得带走的一个模式：**分布式聚合的正确性不依赖投递顺序，只依赖每条消息恰好一次**——所以用一个队列模拟就足以证明协议对

## 1. 题目在说什么（人话版）

树上的节点不共享内存，只能给父节点或子节点发消息。根节点问"你们下面各有多少人"，叶子回答 1，中间节点等所有孩子都回了再把 `1 + 孩子总数` 报给自己的父亲。你要模拟整个过程，记下每条消息被投递的顺序，最后输出根算出的总数。

来源样例 `parent = [-1, 0, 0, 1, 1]`：
```
0->1:GET_COUNT   0->2:GET_COUNT   1->3:GET_COUNT   1->4:GET_COUNT
2->0:REPORT 1    3->1:REPORT 1    4->1:REPORT 1    1->0:REPORT 3
ROOT_COUNT:5
```

## 2. 读题：把文字变成模型

- **实体**：节点、消息 `(from, to, kind, value)`、一个全局 FIFO 信道。
- **状态**：`kids[i]`（升序）、`pending[i]`（还没报告的孩子数）、`total[i]`（1 + 已收到的报告）。
- **输出**：每次投递一行，最后 `ROOT_COUNT:n`。
- **一句话建模**：这是一个 **"事件驱动的状态机模拟"**：出队一条消息，按消息类型改状态并产生新消息。

> [!note] 为什么不直接递归数节点
> 递归只给答案，不给消息顺序；而且面试官要看的是你能不能把"异步等待"写成显式状态（`pending`），这是真实分布式代码的样子。

## 3. 下笔顺序

1. **问清**：日志是发送时记还是投递时记？孩子按什么顺序发？单节点树输出什么？
2. **建图 + 校验**：恰好一个根、父节点不越界不自指、从根能到所有节点（否则有环）。
3. **初始化**：`pending[i] = len(kids[i])`、`total[i] = 1`；根向孩子发 `GET_COUNT`。
4. **主循环**：出队、记日志；`GET_COUNT` 到叶子回 `REPORT 1`，到内部节点向孩子扇出；`REPORT v` 到达就 `total += v`、`pending −= 1`，为 0 时上报或在根处结束。
5. **Part 2**：发送时分配全局发送号；投递时若号在 `drops`：首次记 `LOST` 并重发，重发也丢记 `GIVEUP`，由这条边上的**父节点**记 0、`pending −= 1`，并标记 `PARTIAL`。

## 4. 代码怎么组织

```
_children(parent) -> (root, kids)         # 校验 + 建孩子表
simulate_tree_count(parent, drops=None)   # 一个函数两种模式
  send(frm, to, msg, is_retry)            # 分配发送号并入队
  child_done(node, value)                 # 唯一改 pending/total 的地方
part1 / part2
```
"一个孩子完成了"在正常报告和放弃两条路径上都会发生，抽成 `child_done` 避免两处逻辑分叉。

## 5. 核心代码骨架

```python
def simulate_tree_count(parent, drops=None):
    drops = drops or set()
    root, kids = _children(parent)
    if not kids[root]:
        return ["ROOT_COUNT:1"]
    q, log, next_id, partial = deque(), [], 0, False
    pending, total = [len(k) for k in kids], [1] * len(parent)

    def send(f, t, msg, retry=False):
        nonlocal next_id
        q.append((f, t, msg, next_id, retry)); next_id += 1

    def child_done(node, v):
        total[node] += v; pending[node] -= 1
        if pending[node] == 0:
            if node == root:
                return f"ROOT_COUNT:{total[node]}" + (" PARTIAL" if partial else "")
            send(node, parent[node], f"REPORT {total[node]}")

    for c in kids[root]:
        send(root, c, "GET_COUNT")
    while q:
        f, t, msg, sid, retry = q.popleft()
        if sid in drops:
            if not retry:
                log.append(f"{f}->{t}:{msg} LOST"); send(f, t, msg, True); continue
            log.append(f"{f}->{t}:{msg} GIVEUP"); partial = True
            end = child_done(f if msg == "GET_COUNT" else t, 0)
        else:
            log.append(f"{f}->{t}:{msg}")
            if msg == "GET_COUNT":
                if not kids[t]: send(t, f, "REPORT 1")
                else:
                    for c in kids[t]: send(t, c, "GET_COUNT")
                continue
            end = child_done(t, int(msg.split()[1]))
        if end:
            log.append(end); return log
```

## 6. 每个 part 叠加什么

| Part | 改动 |
|---|---|
| 1 | FIFO 模拟 + `pending` 计数 |
| 2 | 发送号、`LOST` 重发一次、`GIVEUP` 由父节点记 0、`PARTIAL` |

## 7. 常见坑

- 孩子没按 id 升序发送：日志顺序全错。
- 用"已报告孩子集合 == 全部孩子"来判断完成：每次 O(孩子数)，10⁵ 节点慢。
- 单节点树仍然发消息。
- 根不在下标 0。
- Part 2 放弃 `REPORT` 时去改了子节点的计数，而不是父节点。

## 8. 追问怎么接

1. **消息可能重复（至少一次）？** 报告带 `(child_id, epoch)`，父节点去重。
2. **节点崩溃而不是丢包？** 父节点对每个孩子设超时，超时后标记缺失或向孙子重新发起。
3. **10⁹ 个节点跨机器？** 按子树分片，报告只传聚合值；协议不变。
4. **要的不是计数而是求和 / 最大值？** 把 `1 + sum` 换成任何可结合的聚合函数（sum、max、HyperLogLog 合并）。

## 9. 自测清单

- [ ] 手推来源样例的 9 行轨迹
- [ ] 说清 `pending` 计数为什么比集合比较好
- [ ] 说清为什么协议正确性不依赖投递顺序

## 相关题与 skills

S07 消息传递模拟 · S09 协议契约 · S10 失败语义。相关：`od09` 队列（至少一次投递）、`sd05` 分布式队列、`sd02` 调度器（超时与重试）。
