# pc19 · Rewrite Tree With Subtree Sums：练的是"数组下标单调性 → 换表示后必须改成迭代"

> [!tldr]
> - 这题考的是：把每个节点的子树和写回对应位置；Part 1 是完全二叉树数组、一手预览原题，Part 2 是一般二叉树、节点对象、必须迭代 **(reconstructed)**
> - 三步套路：利用完全二叉树"孩子下标 > 父下标"反向扫描一遍 → 识别数组表示在深度 1e5 时物理不可行 → 换成节点对象后用显式栈做两遍迭代后序
> - 最值得带走的一个模式：**满二叉树数组的下标单调性能把后序处理压成一次反向扫描；当规模逼得表示法本身撑不住时，才换成节点对象 + 显式栈的迭代后序**

## 1. 题目在说什么（人话版）

两棵"同形"完全二叉树用层序数组表示，把第二棵树的每个位置改写成第一棵树对应子树的和；第二棵树原
来的值完全不重要，只是用来对齐形状。Part 2 把这个操作搬到一般二叉树（可能有空洞、深度可以到
1e5），用节点对象表示，必须迭代实现。

小例子：
```
rewrite_subtree_sums([5, 2, 3, 1, 4, 6, 7], [0]*7) -> [28, 7, 16, 1, 4, 6, 7]
# 下标 0 的子树和 = 5+2+1+4+3+6+7 = 28；下标 1 的子树和 = 2+1+4 = 7；……
```

## 2. 读题：把文字变成模型

- **实体**：完全二叉树数组（Part 1）/ 节点对象树（Part 2）。
- **输入**：Part 1 是两个等长数组；Part 2 是一个可能有空洞的树。
- **输出**：新数组 / 新树，值是子树和。
- **状态**：Part 1 只需要原地累加；Part 2 需要"孩子先算完才能算父亲"的处理顺序。
- **一句话建模**：这是一个 **"自底向上聚合"** 问题——完全二叉树数组靠下标单调性省掉递归，一般
  树靠显式栈的迭代后序保证同样的处理顺序。

> [!note] 为什么两个 Part 要换两种完全不同的写法
> 完全二叉树数组的下标运算 `2i+1`/`2i+2` 隐含"这是一棵接近满的树"；一条深度 1e5 的纯链表形状
> 用这种数组要开 `2^100000` 个格子，物理上不可行。这不是"要不要用递归"的问题，是表示法本身在
> 极端规模下失效——必须换成节点对象。

## 3. 下笔顺序

1. **问清**：Part 1 的 `root2` 原值是不是完全不重要？Part 2 的深度上限是多少（决定了能不能用
   递归）？
2. **Part 1 最小可用**：从下标 `n-1` 倒着扫到 `0`，扫到 `i` 时孩子（若存在）已经算完子树和，
   直接把两个孩子的和累加到自己身上。
3. **Part 2 叠加**：写一个迭代后序遍历（显式栈，`(node, processed)` 二元组）得到"孩子先于父
   节点"的处理顺序；先跑一遍算出每个节点的子树和（存进以节点对象为 key 的字典），再跑一遍按
   同样顺序建新树（此时孩子的新节点已经在字典里）。
4. **收尾**：空树、只有一个节点、只有左/右孩子的链、负数子树和、深度 1e5 的退化链不能触发
   `RecursionError`。

## 4. 代码怎么组织

```
rewrite_subtree_sums(root1, root2)         # Part 1：反向扫描，O(1) 额外空间
_postorder_nodes(root)                     # 迭代后序，Part 2 两遍都靠它
rewrite_subtree_sums_tree(root1)           # Part 2：两遍迭代（算和 → 建新树）
_build_tree / _serialize_preorder          # 前序 + '#' 的序列化，同样迭代实现
part1 / part2(lines)
```
`_postorder_nodes` 只负责给出"孩子先于父节点"的节点顺序，算子树和与建新树是两个独立的遍历，
职责单一，容易验证。

## 5. 核心代码（骨架）

```python
# Part 1：反向扫描，孩子下标永远大于父下标
def rewrite_subtree_sums(root1, root2):
    if len(root1) != len(root2):
        raise ValueError("root1 and root2 must have the same shape")
    n = len(root1)
    sums = list(root1)
    for i in range(n - 1, -1, -1):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n: sums[i] += sums[left]
        if right < n: sums[i] += sums[right]
    return sums

# Part 2：迭代后序，两遍算和 / 建树
def _postorder_nodes(root):
    if root is None: return []
    order, stack = [], [(root, False)]
    while stack:
        node, processed = stack.pop()
        if processed:
            order.append(node); continue
        stack.append((node, True))
        if node.left: stack.append((node.left, False))
        if node.right: stack.append((node.right, False))
    return order

def rewrite_subtree_sums_tree(root1):
    order = _postorder_nodes(root1)
    sums = {}
    for node in order:
        sums[node] = node.val + sums.get(node.left, 0) + sums.get(node.right, 0)
    new_of = {}
    for node in order:
        new_of[node] = TreeNode(sums[node], new_of.get(node.left), new_of.get(node.right))
    return new_of.get(root1)
```

## 6. 面试里怎么说

- 开始前：「我确认一下：`root2` 里原来的值是不是完全不重要，只是用来对齐形状？」
- 写 Part 1 时：「完全二叉树数组有个好性质——孩子下标永远大于父下标，所以从后往前扫一遍，扫到
  某个节点时它的孩子已经算完了，不需要递归。」
- 到 Part 2 时：「深度 1e5 的树用数组表示要开 `2^100000` 个格子，物理上不可行，所以我换成节点
  对象；同时也不能递归，一条纯链的树会在 Python 里撞到递归深度上限，我用显式栈做迭代后序。」
- 交付时：「样例过了；如果时间允许，我会把算和与建树合并成同一次遍历，减少一次栈操作，但拆成两
  遍职责更清楚也更好测。」

## 7. 常见跑偏

- Part 2 直接用递归写后序遍历，忘了题目明确要求"深度 1e5"这个提示就是在逼你换成迭代。
- 把 Part 1 的数组下标运算直接搬到 Part 2（比如假设树是"接近满"的），碰到空洞或退化链就崩溃。
- 序列化/反序列化也用递归实现，看似只是"读入"逻辑，实际上同样会在深度 1e5 时撞递归上限。

## 8. 同族题 / 延伸

- 与 `pc17`（森林 parent 数组的下标重新压缩）同属"数组编码的树结构"考法，但 pc17 考删除后的
  重新编号，pc19 考子树聚合。
- 与 `pc10`（Distributed Tree Count，节点只能异步通信）同样考"自底向上聚合"，但 pc10 是分布式
  消息模拟，pc19 是单机迭代遍历。
- 练习命令：`python3 loop/mock.py start pc19`
