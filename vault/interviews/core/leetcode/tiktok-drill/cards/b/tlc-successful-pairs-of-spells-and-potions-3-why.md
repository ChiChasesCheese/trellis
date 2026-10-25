---
id: tlc-successful-pairs-of-spells-and-potions-3-why
node: b.successful-pairs-of-spells-and-potions
type: qa
step: 3
---
## Q
**LC 2300 咒语和药水的成功对数**｜正确性

为什么对乘积要用 `bisect_left` 找「第一个 `>= success`」的位置？如果改成 `bisect_right`，或者用 `success // s`（向下取整）当药水下限，会在哪个输入上出错？

## A
**不变量。** 药水升序、咒语为正，所以 `p * s` 随 `p` 不减。`i = bisect_left(potions, success, key=lambda p: p * s)` 满足：`potions[:i]` 的乘积都 `< success`，`potions[i:]` 的乘积都 `>= success`。后缀 `potions[i:]` 的长度 `m - i` 就是答案。

**为什么是 `bisect_left`。** 题目要求乘积 `>= success`，包含相等。`bisect_left` 返回第一个 `>= success` 的位置，相等的元素都在后缀里；`bisect_right` 返回第一个 `> success` 的位置，会把恰好等于 `success` 的组合排除在外。

**反例一：`bisect_right`。** `spells = [2]`，`potions = [8, 8]`，`success = 16`：
- 两瓶药水乘积都是 `16`，恰好等于 `success`，应各算一对，答案 `[2]`。
- `bisect_right` 找第一个 `> 16`，没有，位置 `2`，答案 `[0]`。

**反例二：向下取整的药水下限。** 把条件改写成 `p >= success // s`：
- `spells = [2]`，`potions = [3, 4]`，`success = 7`：`7 // 2 = 3`，药水 `3` 被算成成功，答案 `[2]`。
- 但 `2 * 3 = 6 < 7`，只有药水 `4` 成功，正确答案 `[1]`。要用向上取整 `-(-success // s)`，或者像代码里那样直接比较乘积。
