---
id: hl-c06-sort-lambda
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 2
---
## Q
写出把 `std::vector<Trade> ts`（字段 `sym`、`qty`、`px`）先按 `sym` 升序、再按成交额 `qty*px` 降序排序的代码。`sort` 的复杂度和稳定性如何？

## A
```cpp
std::sort(ts.begin(), ts.end(), [](const Trade& a, const Trade& b) {
    if (a.sym != b.sym) return a.sym < b.sym;
    return a.qty * a.px > b.qty * b.px;
});
```
- `std::sort` 平均 **O(n log n)**，**不稳定**；要稳定用 `std::stable_sort`。
- 比较器必须是**严格弱序**：`a < b` 不能写成 `a <= b`，否则相等元素上 UB/崩溃。
- 先比第一关键字，相等再比第二关键字，是写多键比较器的标准形状。
