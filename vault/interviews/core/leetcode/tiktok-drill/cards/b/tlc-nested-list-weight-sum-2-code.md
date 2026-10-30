---
id: tlc-nested-list-weight-sum-2-code
node: b.nested-list-weight-sum
type: qa
step: 2
---
## Q
**LC 339 嵌套列表加权和**｜写出 Python 实现

嵌套整数列表 `nestedList`（`1 <= 长度 <= 50`，整数值 `[-100, 100]`，最大深度 `<= 50`），元素通过 `isInteger()`、`getInteger()`、`getList()` 访问，最外层深度为 `1`，返回所有整数「值 × 深度」之和。

## A
**思路。** 递归 `dfs(items, depth)`：`items` 是同一深度的一组元素。整数加上 `值 × depth`；子列表带着 `depth + 1` 递归，把返回的和加进来。最外层从 `depth = 1` 开始。

```python
def depth_sum(nestedList: list[NestedInteger]) -> int:
    def dfs(items: list[NestedInteger], depth: int) -> int:   # items 里的元素深度都是 depth
        total = 0
        for item in items:
            if item.isInteger():
                total += item.getInteger() * depth        # 整数：值 × 当前深度
            else:
                total += dfs(item.getList(), depth + 1)   # 子列表：深度加一，递归求和
        return total

    return dfs(nestedList, 1)
```

运行（`NestedInteger` 是题目给的接口）：`[[1,1],2,[1,1]]` → `10`；`[1,[4,[6]]]` → `27`；`[0]` → `0`；嵌套 `50` 层的 `[[...[1]...]]` → `50`；嵌套 `2001` 层在默认递归上限下抛 `RecursionError`。

**复杂度。** 时间 `O(N)`：每个整数和子列表各处理一次；空间 `O(D)`：递归栈，`D` 是最大嵌套深度（题目保证 `D <= 50`）。

**写法要点。** 嵌套函数 `dfs` 返回这一组元素的加权和，调用方直接把子结果加进 `total`，不需要 `nonlocal`；先 `isInteger()` 分流，再对子列表 `getList()`，不能把 `NestedInteger` 当列表迭代；`depth` 作为参数下传，不用在返回时再减；空列表的 `for` 不执行，返回 `0`，空子列表不需要特判。
