# pc10 · Distributed Tree Count — 只靠消息传递数出一棵树有多少节点

> 40 分钟电面题。Part 1 按来源题面实现（含来源样例的 9 行轨迹）；Part 2 丢消息 + 重试一次 + 放弃后部分计数 **(reconstructed)**。

## 背景

想象一个分布式元数据服务：每个节点只知道自己的父节点和子节点，没有共享内存，只能发消息。要统计整棵树有多少节点——根节点发起、叶子应答、中间节点汇总后上报。这就是 fan-out / fan-in 聚合，Snowflake 这类平台团队天天在写的东西的最小模型。

面试考的不是树的遍历（那是 5 行递归），而是**把"等所有子节点回复"建模成状态**、**严格按消息队列的顺序模拟**、**日志格式逐字对**，以及追问时能讲清**消息丢了怎么办**。

## 输入

`parent[i]` 是节点 `i` 的父节点，根为 `-1`。节点编号 `0..n-1`，根不一定是 0。

非法输入抛 `ValueError`：空数组、根不是恰好一个、父节点越界或指向自己、存在环（有节点不挂在根下）。

## API 契约（英文签名）

```python
def simulate_tree_count(parent: list[int], drops: set[int] | None = None) -> list[str]
```

## 规则

### Part 1 — 可靠信道上的计数协议

- 只有**一个全局 FIFO 信道**：消息按发送先后依次投递，每条恰好投递一次。每次投递记一行日志 `from->to:MESSAGE`。
- 开始：根节点按**子节点 id 升序**向每个子节点发 `GET_COUNT`。
- 节点收到 `GET_COUNT`：
  - 叶子 → 立即向父节点发 `REPORT 1`；
  - 非叶子 → 按子节点 id 升序向每个子节点发 `GET_COUNT`，然后等待。
- 节点收到子节点的 `REPORT v`：累加。**所有子节点都报告后**，向父节点发 `REPORT (1 + 子节点总和)`；如果自己是根，追加最后一行 `ROOT_COUNT:<总数>` 并结束。
- 只有一个节点的树：输出只有 `ROOT_COUNT:1`。

### Part 2 — 不可靠链路：丢失、重试一次、放弃 **(reconstructed)**

- 每次发送（包括重试）按发送先后得到一个全局发送号 `0, 1, 2, …`。
- 发送号在 `drops` 里的那次投递**丢失**：在它的投递轮次记 `from->to:MESSAGE LOST`，发送方**立即重发一次**（新发送号，排到队尾）。
- 重发也丢失 → 链路判死：记 `from->to:MESSAGE GIVEUP`。链路两端都能感知失败，于是**这条边上的父节点**把该子节点的整棵子树当作缺失（贡献 0），并视为"这个孩子已经报告"。
- 结束行：`ROOT_COUNT:<n>`；如果有任何子树被放弃，写 `ROOT_COUNT:<n> PARTIAL`。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1（来源样例）** `parent = [-1, 0, 0, 1, 1]`
```
0->1:GET_COUNT
0->2:GET_COUNT
1->3:GET_COUNT
1->4:GET_COUNT
2->0:REPORT 1
3->1:REPORT 1
4->1:REPORT 1
1->0:REPORT 3
ROOT_COUNT:5
```

**例 2（根不在 0）** `parent = [1, -1, 1, 0]`
```
1->0:GET_COUNT
1->2:GET_COUNT
0->3:GET_COUNT
2->1:REPORT 1
3->0:REPORT 1
0->1:REPORT 2
ROOT_COUNT:4
```

**例 3（Part 2：丢一次后重试成功）** `parent = [-1,0,0,1,1]`，`drops = {0}`
```
0->1:GET_COUNT LOST
0->2:GET_COUNT
0->1:GET_COUNT
2->0:REPORT 1
1->3:GET_COUNT
1->4:GET_COUNT
3->1:REPORT 1
4->1:REPORT 1
1->0:REPORT 3
ROOT_COUNT:5
```
（发送号 0 是 `0->1`，丢失后重发得到发送号 2，排在 `0->2` 之后。）

**例 4（Part 2：重试也丢，放弃整棵子树）** `drops = {0, 2}`
```
0->1:GET_COUNT LOST
0->2:GET_COUNT
0->1:GET_COUNT GIVEUP
2->0:REPORT 1
ROOT_COUNT:2 PARTIAL
```

## `main()` 命令流

```
PART 1                  PART 2
-1 0 0 1 1              -1 0 0 1 1
                        DROPS 0 2
```

## 边界清单

- 单节点树、两节点树、链状树（报告逐层冒泡）
- 根不在下标 0
- 子节点必须按 id 升序发送
- 非法数组：空、两个根、没有根、越界、自环、环
- 每条边恰好一条 `GET_COUNT` 一条 `REPORT`（无丢失时日志共 `2(n-1)+1` 行）
- Part 2：丢的是 `GET_COUNT` 还是 `REPORT`，放弃时都由**父节点**计 0
- Part 2：`drops` 里的发送号大于实际发送总数时无影响
- 10^5 个节点 2 秒内（别用递归，别每次线性扫描孩子是否都报告了）

## 追问

1. **"等所有孩子"怎么记？** 每个节点一个 `pending` 计数，初始为孩子个数，收到一个报告减一；为 0 就上报。别存"已报告孩子集合"再比长度。
2. **为什么用一个全局队列就能模拟分布式？** 它把"异步 + 可靠有序"建模成确定的投递顺序；真实系统里顺序不确定，但协议的正确性不依赖顺序（只依赖每条恰好一次），所以换任何投递顺序最终计数都一样——这是面试里最好的一句话。
3. **至少一次投递、消息可能重复怎么办？** 报告带 `(child_id, epoch)`，父节点去重。
4. **节点崩溃而不是链路丢包？** 需要超时 + 心跳；父节点超时后把子树标记缺失或向孙子重新发起。
5. **规模变成 10^9 节点、跨机器？** 按子树分片并行，报告只传聚合值，协议不变。

## 来源与置信度

- **MED**：fastprep "Distributed Tree Counting State Machine"（Phone Screen，2026-07）题面与 `parent=[-1,0,0,1,1]` → 9 行轨迹结尾 `ROOT_COUNT:5` 的样例；prachub "Distributed Tree Node Count with Two Messages"；1point3acres 2026 面经索引标题 "Distributed Tree Counting"。见 `../../../../catalog/raw/coding_phone_onsite.md` #14、`../../../../catalog/raw/ood.md` #7。
- 来源未给出 `REPORT` 消息的逐字格式，本题定为 `REPORT <v>`；Part 2 为重建。

## 考什么

S07 消息传递模拟 / 异步聚合协议 · S09 先定协议契约再写状态 · S10 失败语义（丢失、重试、放弃后的部分结果）。
