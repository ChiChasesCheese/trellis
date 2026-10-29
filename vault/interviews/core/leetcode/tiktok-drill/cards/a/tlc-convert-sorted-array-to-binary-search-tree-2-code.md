---
id: tlc-convert-sorted-array-to-binary-search-tree-2-code
node: a.convert-sorted-array-to-binary-search-tree
type: qa
step: 2
---
## Q
**LC 108 将有序数组转换为二叉搜索树**｜写出 Python 实现

严格递增的整数数组 `nums`（长度 `1` 到 `10^4`）。构造一棵高度平衡的二叉搜索树并返回根结点，结点类型 `TreeNode(val, left, right)`。任何合法的平衡 BST 都可以。

## A
**思路。** `build(lo, hi)` 用 `nums[lo:hi]` 建树：区间为空返回 `None`；否则取中点 `mid` 作根，左子树由 `[lo, mid)` 递归得到，右子树由 `[mid + 1, hi)` 递归得到。

```python
def sorted_array_to_bst(nums: list[int]) -> TreeNode | None:
    def build(lo: int, hi: int) -> TreeNode | None:      # 用 nums[lo:hi]（左闭右开）建树
        if lo >= hi:
            return None
        mid = (lo + hi) // 2               # 中点当根，左右两半个数最多差 1
        return TreeNode(nums[mid], build(lo, mid), build(mid + 1, hi))
    return build(0, len(nums))
```

运行（层序，`None` 表示空位）：`[-10,-3,0,5,9]` → `[0,-3,9,-10,None,5]`；`[1,3]` → `[3,1]`；`[1]` → `[1]`；`[1,2,3,4,5,6]` → `[4,2,6,1,3,5]`。

**复杂度。** 时间 `O(n)`：每个元素恰好建一个结点，`build` 总调用 `2n + 1` 次；空间 `O(log n)`：递归栈深度等于树高，不含输出的树本身。

**写法要点。** 左闭右开区间 `[lo, hi)` 让空区间的判断是 `lo >= hi`，右半段起点是 `mid + 1`，没有 `±1` 的混乱；`TreeNode(val, left, right)` 在构造时直接把两个子树传进去，不需要先建结点再赋值；传下标而不是 `nums[:mid]`，避免每层复制切片。
