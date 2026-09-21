# pc04 · 大整数字符串加减乘：把竖式笔算搬进代码

> [!tldr]
> - 这题考的是：脱离语言内建大整数支持，手写进位/借位/竖式乘法
> - 三步套路：拆符号与数量级 → 按位对齐做加减（进位/借位） → 乘法退化成"多次移位加法"
> - 最值得带走的一个模式：加、减、乘三个运算共用同一套"数字字符 ↔ 数值"映射表和"数量级比较"
>   辅助函数，减法复用加法（加负数），不重复实现借位逻辑

## 1. 题目在说什么（人话版）
两个数字很大很大，大到超出正常整数类型能装下的范围，只能用字符串表示（比如
`"99999999999999999999"`），要求实现加法、（带符号的）减法、乘法——但**不许**把整个字符串转成
一个数字再算。就像小学生在纸上做竖式加法：从最右边一位开始往左，一位一位加，满十进一。

例：`"999" + "1"` → 逐位加：9+1=10 写 0 进 1，9+1(进位)=10 写 0 进 1，9+1(进位)=10 写 0 进 1，
最后还剩一个进位 1，补到最前面 → `"1000"`。

## 2. 读题：把文字变成模型
- **实体**：两个数字字符串（可能带符号），每个字符是一位数字（或十六进制/任意进制下的字母）。
- **输入长什么样**：字符串，从左到右是高位到低位（和读数习惯一致，但计算要从右边最低位开始）。
- **输出要什么**：一个规范化的数字字符串——不带前导零，`"0"` 本身不带符号。
- **状态**：逐位扫描时要记住"进位"（加法）或"借位"（减法）——这决定了用一个 `carry`/`borrow`
  变量、从右向左双指针遍历两个字符串。
- **一句话建模**：这是一个**按位对齐的数组遍历 + 进位传播**问题，和链表逐位相加（LC 2，只是数字
  用字符串而不是链表节点）是同一个骨架。

> [!note] 为什么先拆"符号"和"数量级"
> 加减法一旦要支持负数，最容易踩坑的就是符号判断——与其在加法循环里穿插符号逻辑，不如先把
> `"-123"` 拆成 `(负, "123")`，所有的进位/借位运算都只在无符号的"数量级"字符串上进行，最后再
> 根据同号/异号规则贴回符号。减法则直接复用"加上相反数"：`a - b == a + (-b)`，不用再写一套独立
> 的减法符号判断。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：先写 `add_unsigned(a, b)` 的函数签名和 `main()` 读入分发，用题面第一个例子
   （`"123" + "456"`）跑通。
2. **Part 1 最小可用**：双指针从两个字符串末尾往前走，`carry` 累加，每步 `divmod(da+db+carry, 10)`；
   循环结束条件是"两个指针都走完**且** carry 为 0"（别漏了最后一次进位可能多出一位）。
3. **Part 2 叠加**：拆符号（`_strip_sign`），同号直接调 Part1 的加法逻辑；异号先比较数量级大小
   （逐位比较前先去掉前导零，长度不同直接定大小，长度相同按字典序，因为 `'0'`-`'9'` 的 ASCII
   顺序恰好等于数值顺序），再用大的减小的。减法 = 加上取反后的第二个操作数。
4. **收尾（Part 3）**：乘法不能复用加法的双指针，需要新写一层嵌套循环（外层遍历一个操作数的每
   一位，内层遍历另一个操作数的每一位，往结果数组对应位置累加并本地传播进位）；结果数组长度
   固定为 `len(a) + len(b)`（不会更长），最后去掉多余前导零。

## 4. 代码怎么组织
```
_DIGITS / _VALUE                          # 数字字符 <-> 数值 的映射，加减乘共用
_strip_sign(s) -> (is_neg, magnitude)     # 只管拆符号，不做加减
_cmp_magnitude(a, b) -> -1/0/1            # 只管比大小，供加减法的异号分支用
_add_magnitude / _sub_magnitude(a, b)     # 无符号的加/减，只做进位/借位
add_unsigned(a, b)                        # Part1：直接调 _add_magnitude，加输入校验
add_signed / subtract_signed(a, b)        # Part2：拆符号 -> 调用上面几个 helper -> 贴回符号
multiply_signed(a, b, base=10)            # Part3：独立的竖式乘法，符号规则和加减法一致
main(stdin, stdout)                       # 按 PART 分发
```
核心是把"符号判断""数量级比较""进位/借位循环"拆成三类独立 helper，Part 2 的加减法几乎不用
重新写任何遍历逻辑，只是在最外层决定"该调哪个 helper、结果贴不贴负号"。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def _add_magnitude(a: str, b: str, base: int) -> str:
    i, j, carry = len(a) - 1, len(b) - 1, 0
    out = []
    while i >= 0 or j >= 0 or carry:
        da = _VALUE[a[i]] if i >= 0 else 0
        db = _VALUE[b[j]] if j >= 0 else 0
        carry, rem = divmod(da + db + carry, base)   # 逐位相加，满 base 进一
        out.append(_DIGITS[rem])
        i -= 1; j -= 1
    return "".join(reversed(out))  # 省略去前导零

def multiply_signed(a: str, b: str, base: int = 10) -> str:
    da = [_VALUE[c] for c in reversed(a)]
    db = [_VALUE[c] for c in reversed(b)]
    acc = [0] * (len(da) + len(db))
    for i, x in enumerate(da):
        carry = 0
        for j, y in enumerate(db):
            total = acc[i + j] + x * y + carry
            acc[i + j], carry = total % base, total // base   # 竖式乘法：逐位相乘再进位
        acc[i + len(db)] += carry
    return "".join(_DIGITS[d] for d in reversed(acc))  # 省略取符号、去前导零
```

## 6. 面试里怎么说（边写边讲）
- 开始前："Let me confirm: inputs are plain digit strings, no `int()` conversion allowed in the
  core logic, and I should handle the sign separately from the magnitude — is that right?"
- 写 Part 1 时："I'm walking both strings from the right with two pointers and a running carry,
  the same shape as adding two numbers on paper."
- 交付时："The examples pass; addition and subtraction are O(n), multiplication is O(n·m) because
  the result itself has Θ(n) digits — if time allows I can mention Karatsuba as the next step up."

## 7. 常见跑偏（方法层面，3 条）
- 一上来就想"偷偷" `int(a) + int(b)` 再转回字符串——面试官明确说过要看手写进位，这样写虽然
  结果对，但没展示考点要的东西。
- 减法单独写一套借位逻辑，和加法的进位逻辑重复了一遍——不如统一成"加上相反数"，复用同一套
  加法/比较 helper。
- 乘法只处理了不进位的情况，或者忘了内层循环结束后还可能有残留 `carry` 要继续往更高位传播
  （测试专门用大数交叉验证捕捉这个）。

## 8. 同族题 / 延伸
- `../../snowflake/loop/rounds/03_phone_coding/pc06_happy_number/`：同样是"用有限状态位运算，
  不依赖语言内建大整数/容器"的手写题（Floyd 判环要求 O(1) 空间，这里要求不调用 `int()`）。
- 本 kit `pc03_decorators/`：同一轮的另一道"Python 内功"题，风格互补（一个考数值手算，一个考
  函数式编程）。
- 练习命令：`python3 loop/mock.py start pc04`
