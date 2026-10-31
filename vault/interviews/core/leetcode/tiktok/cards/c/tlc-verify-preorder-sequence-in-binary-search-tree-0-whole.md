---
id: tlc-verify-preorder-sequence-in-binary-search-tree-0-whole
node: c.verify-preorder-sequence-in-binary-search-tree
type: qa
---
## Q
**LC 255 验证前序遍历序列二叉搜索树**｜Medium · LC TikTok 全时段热度 25/100 · CodeTop 国内累计 1 次 · 最近 2020-07-10（国内 CodeTop）

给定一个无重复元素的整数数组 `preorder`，如果它是某棵二叉搜索树（BST）的前序遍历序列，返回 `true`。`1 <= preorder.length <= 10^4`，`1 <= preorder[i] <= 10^4`，`preorder` 中无重复元素。例：`preorder = [5,2,1,3,6]` → `true`；`preorder = [5,2,6,1,3]` → `false`。进阶：能否使用恒定的空间复杂度来完成？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按前序「根、左、右」的顺序模拟建树：每个子树只接受落在 `(lo, hi)` 开区间里的数，递归消费序列，最后看是否恰好用完，`O(n)`；进阶的 `O(1)` 空间在拓展优化里。

**识别。** 前序遍历的 BST 序列：第一个数是根，其后先是一段全小于根的数（左子树），再是一段全大于根的数（右子树），递归成立。「验证一个序列是不是某种遍历」常用「按遍历规则重建一遍」来做。

**推导。** 暴力：取第一个数为根，找到第一个大于根的位置切成左右两段，检查右段全大于根，递归，最坏 `O(n²)`。更好的：不切分序列，只维护每个子树允许的取值范围 `(lo, hi)`：消费下一个数 `x`，若 `lo < x < hi` 它就是当前子树的根，然后左子树范围 `(lo, x)`、右子树范围 `(x, hi)`，先左后右。下一个数不在范围内就返回，交给外层。序列恰好被用完才合法。

```python
from math import inf


def verify_preorder(preorder: list[int]) -> bool:
    n = len(preorder)
    i = 0                                        # 下一个待消费的位置

    def build(lo: float, hi: float) -> None:
        nonlocal i
        if i == n or not (lo < preorder[i] < hi):
            return                               # 序列用完，或下一个数不属于这棵子树
        root = preorder[i]
        i += 1
        build(lo, root)                          # 左子树：值在 (lo, root)
        build(root, hi)                          # 右子树：值在 (root, hi)

    build(-inf, inf)
    return i == n                                # 恰好全部用完才是合法的前序序列
```

运行：`[5,2,1,3,6]` → `True`，`[5,2,6,1,3]` → `False`；`[1]` → `True`，`[2,1,3]` → `True`，`[3,1,2,4,5,0]` → `False`；`10000` 到 `1` 递减的序列（单链）在默认递归上限下抛 `RecursionError`，调到 `20000` 后输出 `True`。

**复杂度。** 时间 `O(n)`，每个数被消费一次；空间 `O(h)`（递归栈，链状时 `h = n`）。

**拓展优化。**
- 用显式栈代替递归（同样是 `O(n)`）：栈里放「等待右子树的祖先」；一旦出现比栈顶大的数，说明走进某个祖先的右子树，被弹出的最后一个祖先 `low` 成为此后所有数的下界。

```python
def verify_preorder_stack(preorder: list[int]) -> bool:
    stack: list[int] = []                        # 严格递减：等待右子树的祖先
    low = 0                                      # 之后所有数必须大于 low（值都 >= 1）
    for x in preorder:
        if x < low:
            return False                         # 进入右子树后又出现了更小的数
        while stack and stack[-1] < x:
            low = stack.pop()                    # x 在这些祖先的右子树里，下界抬高
        stack.append(x)
    return True
```

- 进阶 `O(1)` 空间：把输入数组本身当栈（`top` 指针只会不超过当前下标），其余逻辑相同；代价是修改输入。

```python
def verify_preorder_in_place(preorder: list[int]) -> bool:
    low, top = 0, -1                             # preorder[0..top] 是栈
    for x in preorder:
        if x < low:
            return False
        while top >= 0 and preorder[top] < x:
            low = preorder[top]
            top -= 1
        top += 1
        preorder[top] = x                        # 栈顶下标不超过 x 的位置，覆盖已读过的元素
    return True
```

**易错点。**
- 忘了检查序列是否用完：`[5,2,6,1,3]` 在 `build` 里消费到 `6` 之后就卡住，不检查 `i == n` 会返回 `True`，正确是 `False`。
- 递归深度：降序序列是一条 10^4 层的左链，CPython 默认上限约 1000，会抛 `RecursionError`，要调高上限或改用拓展优化里的栈版本。

**追问。**
- 验证后序遍历（LC 255 的姊妹题）：从右往左读，镜像地套用栈做法。
- 输入允许重复值：BST 的定义要明确重复值放左还是放右，再相应调整比较符号。

**同模式。** LC 449 序列化和反序列化二叉搜索树、LC 1008 前序遍历构造二叉搜索树、LC 98 验证二叉搜索树、LC 105 从前序与中序遍历序列构造二叉树、LC 331 验证二叉树的前序序列化。
