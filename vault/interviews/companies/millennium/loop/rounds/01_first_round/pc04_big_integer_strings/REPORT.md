# pc04 Big-Integer String Arithmetic — report

## Summary
一手电面原题：45 分钟 C++ Developer 电面（15 min 背景 + 30 min 编码），"两个字符串表示的大整数
相加"。3-part 递进：Part 1 无符号十进制加法（一手）→ Part 2 带符号加减（同族延伸）→ Part 3 乘法
推广到任意进制 2–36 **(reconstructed)**。核心约束是全程不使用 `int()` 做数值转换，逐位手写
进位/借位/竖式乘法。

## Sources & confidence
HIGH（1point3acres thread-1090775，Part 1 原题原文）；Part 2、Part 3 为按"大整数字符串运算"
题族常见递进结构补齐的重建。

## Approach by part
1. `add_unsigned`：从右到左逐位相加，`carry` 累加进位，结果反转后去掉多余前导零；空串/非数字
   字符校验前置。
2. `add_signed` / `subtract_signed`：拆出符号与数量级（`_strip_sign`），同号直接加数量级、异号
   比较数量级（`_cmp_magnitude`）后用大的减小的（`_sub_magnitude`）；减法统一转成
   `add_signed(a, negate(b))`，避免重复实现一套借位逻辑；结果数量级为零时强制去掉符号。
3. `multiply_signed`：把操作数按 `base` 拆成逐位数值数组，做标准竖式长乘法（外层遍历 `a` 的每
   一位、内层遍历 `b` 的每一位并向更高位进位），O(len(a)·len(b))；数字字符与数值的映射表
   `_DIGITS`/`_VALUE` 同时服务 Part 1/2（固定 base=10）与 Part 3（任意 base），避免重复定义。

## Pitfalls hidden tests target
- 前导零输入（`"007"`）与连续进位链（`"999"+"1"`→`"1000"`，进位一路传到最高位新增一位）
- 负零归一化：`"-0"` 输入、以及运算结果数量级恰为零时，输出必须是 `"0"` 不能是 `"-0"`
- 空串 / 只有符号没有数字（`"-"`、`"+"`）→ `ValueError`
- 非数字字符（含空格、多余符号）→ `ValueError`
- Part 3：任一操作数为 `"0"` 的短路路径；`base` 越界（`<2`/`>36`）；数字字符超出该进制范围
  （如八进制里的 `'9'`）
- 随机数交叉验证：Part 1/2 对拍 Python `int()`（4000 组随机数，含负数、异号）；Part 3 对拍
  "转成十进制值相乘再转回目标进制"（1500 组随机数、随机 base 2–36）
- 大数性能：两个 2000 位十进制数相乘（`O(n·m)` = 4×10⁶ 次逐位乘法），验证纯 Python 实现不
  依赖 `int()` 转换也能在预算时间内完成

## Complexity & measured cost
加/减 `O(max(len(a), len(b)))`；乘法 `O(len(a)·len(b))`。编排者验证：`add_unsigned`/`add_signed`/
`subtract_signed` 与 Python `int()` 在 4000 组随机十进制数（含负数、前导零）上 0 处不一致；
`multiply_signed` 与"转十进制值相乘再转回目标进制"在 1500 组随机数、随机 base 2–36 上 0 处不
一致；两个 2000 位十进制数相乘实测 0.53 s（本机），远低于 2 s 预算。

## Test inventory
18 test functions（`grep -c "def test"` = 18），参数化展开后 pytest 收集 35 个用例——
`uv run --project /home/user/trellis --with pytest python -m pytest loop/rounds/01_first_round/pc04_* -p no:cacheprovider` → `35 passed`；
`IMPL=starter` 同一条命令 → `35 failed`。按 marker 统计（`grep -oE`）：part1 6 · part2 5 ·
part3 7；edge 10 · fmt 1 · perf 1 · io 3。

## Skills exercised
S02 字符串/数组的手写数值运算（进位、借位、竖式乘法）· S08 复杂度分析（加减 O(n) vs 乘法
O(n·m) 下界）· 不依赖语言内建大整数支持的"手写"实现能力。
