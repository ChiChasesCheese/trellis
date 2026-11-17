---
id: parsing-io-recursive-descent-left-recursion
node: parsing-io.recursive-descent
type: qa
step: 2
---
## Q
文法 `expr = expr "-" term | term` 看起来最贴近「左结合」，照它写成函数为什么栈溢出？改成递归右边又会让 `8-3-2` 算错，怎么办？

## A
**左递归改成循环，循环里从左往右折叠**

- **左递归**：`expr` 的第一步就是调用 `expr`，没有吃掉任何 token，下一层又是同样的位置，永远走不出去，抛 `RecursionError`；
- **改成右递归**：`expr = term "-" expr` 不再无限递归，但结合性反了：`8-3-2` 变成 `8-(3-2)` = 7，正确答案是 `(8-3)-2` = 3；
- **改成循环**：`expr = term ("-" term)*`，先读一个 `term`，然后 `while` 遇到运算符就把累计值和新读的 `term` 合并，天然左结合；
- **同一个办法**适用于所有左结合的二元运算符（加减乘除、比较、`and`）；
- **右结合的运算符**（乘方、赋值）才用右递归。

```python
def sub_right(nums):                          # expr = term "-" expr：右递归
    return nums[0] if len(nums) == 1 else nums[0] - sub_right(nums[1:])

def sub_loop(nums):                           # expr = term ("-" term)*：循环
    v = nums[0]
    for n in nums[1:]: v -= n
    return v

def expr_left(): return expr_left()           # expr = expr "-" term：没吃 token 就递归
try: expr_left()
except RecursionError: print("RecursionError")
print(sub_right([8, 3, 2]), sub_loop([8, 3, 2]))      # 7 3
```

**知识点：**递归下降解析（Recursive Descent）
