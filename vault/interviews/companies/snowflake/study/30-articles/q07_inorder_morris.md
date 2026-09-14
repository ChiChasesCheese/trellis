# q07 · Inorder Traversal 三连：递归 → 迭代 → Morris，练的是"同一个输出，三种空间代价"

> [!tldr]
> - 这题考的是：LC 94 中序遍历的三种实现，输出必须完全一致，区别只在调用栈/堆空间开销
> - 三步套路：先写最熟悉的递归版本 → 用显式栈翻译成迭代版本（结构不变，栈换个地方存）→ 用"穿线"技巧把栈也省掉（Morris）
> - 最值得带走的一个模式：**Morris 遍历靠"临时改树"换空间**——用中序前驱的空闲右指针搭一条临时线索，走完就拆掉，全程 O(1) 额外空间

## 1. 题目在说什么（人话版）
给一棵二叉树，按"左子树、根、右子树"的顺序输出所有节点值（中序遍历）。这题本身很基础，Snowflake
真正想看的是现场追问：能不能把递归版本改写成不用调用栈的迭代版本，再进一步改写成完全不用额外空间的
Morris 遍历——三个版本对同一棵树必须产出完全相同的结果。

三行小例子：
```
build_tree(["1","null","2","3"])  # root=1，右孩子=2，2的左孩子=3
inorder = [1, 3, 2]                # part1 == part2 == part3
```

## 2. 读题：把文字变成模型
- **实体**：二叉树节点（`val`、`left`、`right`）。
- **输入长什么样**：`PART n` + 一行 LeetCode 风格 level-order CSV（`null` 表示缺失子节点）。
- **输出要什么**：一行逗号连接的中序遍历值，空树输出空行。
- **状态**：递归版本靠调用栈记"回到哪个父节点"；迭代版本用显式栈做同样的事；Morris 版本完全不存
  状态，靠临时修改树的右指针（穿线）当"回去的路"。
- **一句话建模**：这是同一个遍历顺序的 **三种空间复杂度实现**，核心考点是理解"调用栈"和"显式栈"
  的本质是一回事，而 Morris 是用树本身的空闲指针位省掉这个栈。

> [!note] 为什么选这个数据结构
> Morris 遍历的关键洞察是：一个节点在中序遍历里，如果有左子树，它的中序前驱（左子树最右节点）的
> `right` 指针在遍历前是空闲的（它没有右孩子，否则它就不是"最右"）。借用这个空闲指针临时指向当前
> 节点，就能在访问完左子树后"找到回去的路"，不需要额外的栈或调用栈。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析 `PART`/CSV 建树，调 `part1/2/3`，逗号拼接输出。
2. **Part 1 最小可用**：标准递归 `visit(left); out.append(val); visit(right)`。这是最容易写对的版本，
   先确保输出正确。
3. **Part 2 叠加**：把递归换成显式栈——一路把左链压栈到底，弹出一个就输出，再转向它的右子树重复。
   逻辑和递归版本是同构的，只是"回溯点"从调用栈变成了显式的 Python list。
4. **Part 3 叠加**：Morris——对每个节点先看有没有左子树；有就找中序前驱，第一次到达就穿线再往左走，
   第二次通过穿线回来就拆线、输出、往右走；没有左子树就直接输出、往右走。**遍历完必须把树复原**。
5. **收尾**：验证三个版本在同一棵树上跑输出完全一致；确认 Morris 遍历后树结构没有残留穿线指针
   （再跑一次 part1 应该得到相同结果）。

## 4. 代码怎么组织
```
build_tree(values) -> TreeNode | None     # LeetCode 风格 level-order 建树
part1(root) -> list[int]                  # 递归，O(h) 调用栈
part2(root) -> list[int]                  # 显式栈迭代，O(h) 堆空间
part3(root) -> list[int]                  # Morris，O(1) 额外空间
main(stdin, stdout)                        # 解析、按 PART 分派
```
三个 part 各自独立实现（不是互相调用），因为面试官想看到你分别掌握三种范式的写法，而不是只写一个
再"伪装"成三个。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def part1(root):                          # 递归：调用栈隐式记录回溯点
    out = []
    def visit(node):
        if node is None:
            return
        visit(node.left)
        out.append(node.val)
        visit(node.right)
    visit(root)
    return out

def part2(root):                          # 显式栈：把调用栈搬到堆上
    out, stack, node = [], [], root
    while stack or node is not None:
        while node is not None:            # 一路把左链压栈到底
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out

def part3(root):                          # Morris：借前驱的空闲 right 指针当"回去的路"
    out, node = [], root
    while node is not None:
        if node.left is None:
            out.append(node.val)
            node = node.right
            continue
        predecessor = node.left            # 找中序前驱：左子树里最右的节点
        while predecessor.right is not None and predecessor.right is not node:
            predecessor = predecessor.right
        if predecessor.right is None:      # 第一次到达：穿线，往左走
            predecessor.right = node
            node = node.left
        else:                              # 第二次通过穿线回来：拆线、输出、往右走
            predecessor.right = None
            out.append(node.val)
            node = node.right
    return out
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先写熟悉的递归版本确保输出正确，再逐步压缩空间——迭代版本用显式栈，最后 Morris 做到
  真正的 O(1)。」
- 写 Part 2 时：「递归和显式栈本质是同一件事，只是『回溯点』存在调用栈还是堆上的 list——这里我把
  左链一路压栈到底，弹出一个就输出，再转向它的右子树。」
- 写 Part 3 时：「Morris 的关键是：一个有左子树的节点，它的中序前驱在遍历前 `right` 指针是空的，
  我借用这个空位临时指向当前节点，走完左子树后就能找到回来的路；第二次经过时说明左子树访问完了，
  这时候要把线索拆掉，恢复树的原状，再输出并往右走。」
- 如果面试官问"极端深的树会怎样"：「递归版本会在深链上炸调用栈，我可以现场构造一棵 2000 层的纯右链
  树，用一个降低的 `recursionlimit` 证明递归版本会报错，而迭代和 Morris 都能正常跑完。」
- 交付时：「三个版本在所有样例上输出完全一致；Morris 跑完之后我额外验证了树本身没有残留穿线指针——
  再跑一次递归版本结果不变。」

## 7. 常见跑偏（方法层面，3 条）
- **Morris 遍历完不拆穿线**：树被永久性地改坏了，之后任何遍历（包括再跑一次 part1）都会得到错误结果
  甚至死循环。拆线这一步不能忘，且必须在"输出之前"拆（顺序错了会漏输出或重复输出）。
- **迭代版本没有正确处理"外层循环条件"**：`while stack or node is not None` 两个条件缺一个都会漏掉
  最后一部分节点，纯右链或纯左链的树很容易暴露这个问题。
- **用递归版本去验证 Morris 时不构造深树**：极端深度（纯右链）是这题隐藏测试明确要求的差异化场景，
  不构造它就发现不了递归版本的调用栈问题。

## 8. 同族题 / 延伸
- 同一场电面（2019）还问了 `q06` Patching Array，是同一场"经典算法 + 现场压复杂度"的电面链条。
- 延伸思考：前序/后序遍历也有 Morris 变体，后序的 Morris 需要"逆转右链"技巧，比中序难得多，是常见的
  进一步追问。
- 练习命令：`python3 loop/mock.py start q07`
