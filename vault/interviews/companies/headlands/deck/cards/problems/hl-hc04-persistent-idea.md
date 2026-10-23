---
id: hl-hc04-persistent-idea
node: problems.hc04-queue-mean-snapshot
type: qa
step: 9
---
## Q
持久化数据结构（persistent data structure）是什么？队列版本化时为什么不能每个版本复制一份，用什么结构？

## A
普通数据结构一改就丢旧状态；**持久化**每次修改生成新版本，旧版本仍可读，新旧版本**共享**没变的部分。最简例子：链表 `1→2→3` 前面加 0，只新建一个节点，后面全部共享。

每版本复制整份：n 个版本 O(n²)（2 万版本 168 ms，按平方外推 30 万版本约 37 秒必超时）。

**树 + 版本三元组**：队列内容 = push 序列去掉最前面已 pop 的若干个，即一段后缀。把所有 push 过的元素放进一棵**后继树**：`push(version, x)` 新建节点（值 `x`，父亲 = 该版本的队尾节点），根到某节点的路径就是一条 push 序列；同一版本 push 两个不同值 = 同一节点两个孩子 = **分叉**。一个版本只存三个数：
- `tail`：队尾节点；
- `headDepth`：已弹出多少个（队头在路径上的深度 = `headDepth + 1`）；
- `sum`：当前内容之和（128 位）。

push 新建节点 O(1)；`size = depth[tail] - headDepth`，均值 = `sum / size`，O(1)；`pop` 要知道被弹值才能 `sum -= 值`，它是路径上深度 `headDepth + 1` 的祖先（level ancestor）。

为什么不是银行家队列（两个栈实现队列）：它的 pop 只是**均摊** O(1)，持久化时同一旧版本被反复 pop，昂贵的「翻转」反复触发，均摊失效，最坏 O(n)（Okasaki 专门讲）。
