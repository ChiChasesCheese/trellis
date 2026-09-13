# q07 Inorder Traversal (Morris) — report

## 摘要

LeetCode 94 是 Snowflake 电面的经典开场题，真正的考点不是"写出中序遍历"而是现场追问"能不能把
空间压到 O(1)"（Morris 遍历）。三个 part 强制候选人依次交出递归、迭代、Morris 三种实现，且必须
保证输出完全一致——面试官关心的是候选人能不能在压力下讲清楚"调用栈 O(h) vs 显式堆栈 O(h) vs
穿线 O(1)"这三者的区别，而不仅仅是背出 Morris 的代码。

## 来源与置信度

- medium-high：https://leetcode.com/discuss/interview-question/424385/snowflake-phone-screen-patching-array/
  （2019 phone screen，逐字引用"bonus point if constant space"追问）。
- medium-high：LC 94 原题 + 2023 Canada 题库索引 #20 复用（OA 题池直接搬运同一道题）。

## 逐 part 思路

1. **part1**：教科书递归中序（left, node, right），用一个内部闭包 `visit()` 累积到外层
   `out` 列表，避免用递归返回值拼接列表（拼接会额外增加复杂度且容易在大树上产生大量中间列表）。
2. **part2**：显式栈迭代——不断把左链压栈直到叶子，弹栈输出，再转向右子树。栈是 Python list，
   分配在堆上，和调用栈无关，因此在递归深度受限的场景下依然安全。
3. **part3**：Morris 遍历。对每个当前节点，若有左子树，找它的中序前驱（左子树最右节点）：
   第一次到达时穿线 `predecessor.right = node` 并转向左子树；通过穿线第二次回到该节点时，先拆线
   恢复原状再输出、转向右子树。若无左子树直接输出并右移。全程 O(1) 额外空间，不递归、不用栈。

`build_tree` 用标准的 BFS 队列构建（`values` 里 `"null"`/空字符串跳过，不产生新的队列项），本身
是迭代实现，构造 ~1e5 节点的树也不会触发递归限制。

## 隐藏测试针对的坑

- **调用栈 vs 堆栈的混淆**：这是本题唯一"决定成败"的坑，因此单独做了一个显式测试
  (`test_morris_and_iterative_survive_constrained_recursion_limit`)，在
  `sys.setrecursionlimit(300)` 的约束下，构造一条 2000 节点右链：`part1` 必须抛出
  `RecursionError`，`part2`/`part3` 必须都成功且结果正确——用 try/finally 恢复原始
  recursion limit，避免污染其它测试（pytest 模块级 `impl` fixture 是 scope="module"，如果不恢复
  会连累同文件后续测试）。
- **Morris 穿线未拆除**：遍历后如果忘记 `predecessor.right = None`，树结构会被永久破坏。测试
  `test_part3_restores_tree_shape` 在跑完 `part3` 之后再跑一次 `part1` 在同一棵树对象上，两次
  结果必须一致；`test_part3_no_dangling_threads` 额外递归遍历整棵树显式断言没有任何
  `predecessor.right is node` 的残留。
- **build_tree 的 null 跳过逻辑**：容易写错导致 null 子节点错误地消耗/不消耗队列位置，用官方
  worked example（`5,3,8,1,4,7,9` 的经典树形状）交叉验证。
- **三个 part 互相分叉**：只要有一个 part 在非平凡树上跟另外两个结果不一致，说明某个实现的遍历
  顺序错了；`test_part2_matches_part1_random_trees` 用 20 棵随机平衡树做交叉验证。

## 复杂度与实测

- part1：O(n) 时间，O(h) 调用栈（h = 树高，最坏 O(n)）。
- part2：O(n) 时间，O(h) 堆内存（显式栈），O(1) 调用栈。
- part3：O(n) 时间（每条边最多访问两次：一次建穿线，一次拆穿线），O(1) 额外空间与调用栈。
- 实测：10 万节点的近似平衡树上 `part3` 远小于 2s 预算（迭代构造，构造阶段本身不触发递归限制）。

## 测试清单

19 个测试 — part1: 6 · part2: 3 · part3: 6 · io: 5（不同 part 标记按主要覆盖对象分类，
交叉验证测试标在被验证的高阶 part 上）。标记分布：edge 6（含关键的递归深度差异化测试）·
perf 1 · io 5。`IMPL=starter` 下 12/19 测试失败（真实断言失败 / `DID NOT RAISE`，非 collection
error），`solution.py` 下全绿。

## 技能 ids

S08 LC 原题 + 复杂度再压一档（Morris、Floyd、O(m·n)）· S04 树的递归/迭代/O(1) 空间三种遍历范式
互换 · S09 精确格式化输出（stdin/stdout 单行 CSV 协议）。
