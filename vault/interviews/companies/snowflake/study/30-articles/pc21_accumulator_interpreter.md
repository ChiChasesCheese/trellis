# pc21 · Accumulator Interpreter：练的是"可结合的变换记忆化 = 快速幂压缩海量重复调用"

> [!tldr]
> - 这题考的是：单变量累加器上的小型解释器，从纯累加器算术到函数声明/调用（含环检测）再到海量重复调用取模；Part 1/2 语言元素一手预览原文，检测机制与 Part 3 **(reconstructed)**
> - 三步套路：顺序执行累加器指令 → 声明时不执行、调用时才执行，用调用链集合防环 → 把每条指令看成仿射变换，复合后记忆化，用快速幂压缩 `REPEAT`
> - 最值得带走的一个模式：**可结合的运算（仿射变换）复合后仍是同类运算，可以只算一次整体效果并记忆化，把 O(count) 的暴力循环压成 O(log count) 的快速幂**

## 1. 题目在说什么（人话版）

一个全局变量 `X` 从 0 开始。Part 1 只有 `ADD`/`SUB`/`MULT`/`DIV` 顺序执行。Part 2 加上
`FUN name ... END`（声明函数，声明时不执行）和 `INV name`（调用，才真正执行函数体）；调用未声明
的函数或出现调用环都要报错。Part 3 加上 `REPEAT count name`（连续调用 `count` 次，`count` 可以
到 `~10^15`），所有运算取模。

小例子：
```
run_calculator(["ADD 6","SUB 3","MULT 4","DIV 2"]) -> 6         # (0+6-3)*4/2
run_snowcal(["ADD 3","FUN double","MUL 2","END","INV double"]) -> 6
run_snowcal_mod(["ADD 3","FUN double","MUL 2","END","REPEAT 5 double"]) -> 96   # 3*2^5
```

## 2. 读题：把文字变成模型

- **实体**：累加器/全局变量、指令、函数（名字 → 指令列表）、调用链。
- **输入**：一串命令或一段程序。
- **输出**：最终的累加器/变量值。
- **状态**：Part 2 需要"当前正在执行的函数名集合"防环；Part 3 需要每个函数的仿射映射记忆表。
- **一句话建模**：这是一个 **"单变量小型解释器"**，Part 3 的关键洞察是每条指令对 `X` 的作用都是
  一个仿射变换 `x -> a*x + b`，可结合，可以记忆化。

> [!note] 为什么 `REPEAT` 不能直接循环
> `count` 可以到 `10^15`，直接循环显然太慢。但每条指令（`ADD n` 是 `(1,n)`，`MUL n` 是
> `(n,0)`，调用函数是其记忆化的 `(a,b)`）都是仿射变换，复合两个仿射变换还是仿射变换——所以整个
> 函数的净效果只需要算一次，"重复 count 次"就是把这个仿射映射自己复合 count 次，有闭式解。

## 3. 下笔顺序

1. **问清**：`DIV` 是向零截断还是向下取整？（预览没说，本 kit 选向零截断，因为大多数"计算器"
   题的直觉是这样。）无限递归具体怎么检测？
2. **Part 1 最小可用**：累加器从 0 开始顺序执行四种指令；`DIV` 用 `abs(a)//abs(b)` 再按符号
   取负实现向零截断；除零、未知命令报错。
3. **Part 2 叠加**：先扫描把所有 `FUN...END` 块抽出到字典（声明不执行），剩余顶层指令顺序求值；
   `INV` 用"当前调用链"集合传递，即将调用一个已在链上的函数就立刻报错。
4. **Part 3 叠加**：给每条指令定义仿射变换，顺序复合得到函数/程序的净仿射映射（记忆化）；
   `REPEAT count name` 用等比数列闭式解（`a≠1` 用模逆元，`a==1` 退化成等差数列）把 count 次
   压缩成 `O(log count)`。
5. **收尾**：`REPEAT 0` 恒等；`a mod MOD==1`（纯 `ADD` 函数）必须走等差分支，避免对 0 求逆元。

## 4. 代码怎么组织

```
run_calculator(commands)                     # Part 1
_split_functions(lines) -> (top_level, funcs)  # 声明与顶层指令分离，Part 2/3 共用
_exec_snowcal_stmt(stmt, x, funcs, chain)    # Part 2：递归执行 + 调用链防环
run_snowcal(lines)
_affine_of_function / _affine_of_instructions  # Part 3：仿射映射 + 记忆化
_affine_power(a, b, k)                       # 快速幂 + 等比数列闭式解
run_snowcal_mod(lines)
```
Part 2、Part 3 共用 `_split_functions`；Part 3 的"调用链防环"逻辑与 Part 2 完全一样，只是把
"执行一条指令"换成"计算一条指令的仿射变换"。

## 5. 核心代码（骨架）

```python
MOD = 1_000_000_007

def _compose(a1, b1, a2, b2):          # map2 after map1
    return (a2 * a1) % MOD, (a2 * b1 + b2) % MOD

def _affine_power(a, b, k):            # x -> a*x+b 复合自己 k 次，O(log k)
    if k == 0: return 1, 0
    a %= MOD
    if a == 1:
        return 1, (b * (k % MOD)) % MOD          # 等差数列，避免对 0 求逆元
    ak = pow(a, k, MOD)
    inv = pow(a - 1, MOD - 2, MOD)                # 费马小定理求模逆元
    return ak, b % MOD * ((ak - 1) % MOD) % MOD * inv % MOD

def _affine_of_instructions(instructions, funcs, memo, chain):
    a, b = 1, 0
    for stmt in instructions:
        op, *rest = stmt.split()
        if op == "ADD": a, b = _compose(a, b, 1, int(rest[0]) % MOD)
        elif op == "MUL": a, b = _compose(a, b, int(rest[0]) % MOD, 0)
        elif op == "INV":
            fa, fb = _affine_of_function(rest[0], funcs, memo, chain)
            a, b = _compose(a, b, fa, fb)
        elif op == "REPEAT":
            fa, fb = _affine_of_function(rest[1], funcs, memo, chain)
            ra, rb = _affine_power(fa, fb, int(rest[0]))
            a, b = _compose(a, b, ra, rb)
    return a, b
```

## 6. 面试里怎么说

- 开始前：「`DIV` 是向零截断还是 Python 的向下取整？两者只在符号不同时才分叉，我先确认一下。」
- 写 Part 2 时：「函数调用其它函数可能出现环，我用'当前调用链'这个集合传递下去，即将调用一个已
  经在链上的函数就立刻报错，而不是真的死循环再检测超时。」
- 到 Part 3 时：「`count` 到 10^15，直接循环不可行；我观察到每条指令对 `X` 的作用都是仿射变换，
  可结合，所以给每个函数只算一次它的净仿射映射，'重复 count 次'就是这个映射的 count 次幂，有
  闭式解，复杂度只有 `O(log count)`。」
- 交付时：「样例过了；`a mod MOD == 1` 的情况我单独处理了等差数列，避免对 0 求模逆元。」

## 7. 常见跑偏

- Part 2 用"函数体是否包含自己的名字"这种字符串匹配判环，漏掉间接互递归（`a` 调 `b`，`b` 调
  `a`）。
- Part 3 直接对 `REPEAT count name` 写循环，`count` 到 10^15 直接超时。
- 忘记 `a mod MOD == 1` 时不能用等比数列公式（`a-1 ≡ 0` 没有模逆元），需要单独退化成等差数列。

## 8. 同族题 / 延伸

- 与 `pc06`（Happy Number）同样是"反复套一个函数"的题型，但 pc06 考判环用快慢指针，pc21 考
  调用链集合防环 + 仿射映射记忆化。
- 与 `pc24`（依赖图环检测）同样考"隐式有向图上的环检测"，但 pc24 是拓扑排序判环，pc21 是调用链
  集合判环。
- 练习命令：`python3 loop/mock.py start pc21`

## 索引行

| [pc21_accumulator_interpreter](pc21_accumulator_interpreter.md) | `../../loop/rounds/03_phone_coding/pc21_accumulator_interpreter/` | 电面 coding | 可结合的运算（仿射变换）复合后仍是同类运算，可以只算一次整体效果并记忆化，把 O(count) 的暴力循环压成 O(log count) 的快速幂 |
