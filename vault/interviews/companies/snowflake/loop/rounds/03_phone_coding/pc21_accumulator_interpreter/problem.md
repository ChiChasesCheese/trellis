# pc21 · Accumulator Interpreter — String-Command Calculator → SnowCal → 仿射映射记忆化

> TrueInterview 87 题清单第 34 题（String-Command Calculator，2026-02）与第 19 题（SnowCal，
> 2026-05）同族，本 kit 合并成一题的三个 Part（都是"单变量累加器上的小型解释器"）。Part 1、Part 2
> 的语言设计是一手预览原文；Part 2 的"未定义函数 / 无限递归都要报错"是原文明确要求，检测方式与
> Part 3 全部 **(reconstructed)**。

## 背景

TrueInterview（`kevin-2023-code/Tech-Interview-Questions`，见 `../../../catalog/raw/github_repos.md`
§2 第 19、34 行、§3）列出两道 Snowflake 题：一道是"String-Command Calculator"（`ADD`/`SUB`/`MULT`/`DIV`
累加器），一道是"SnowCal"（`ADD`/`MUL`/`FUN…END`/`INV` 单变量小语言）。二者都是"在一个累加器/变量上跑一串
指令"，本 kit 按复杂度递增合并为 pc21 的三个 Part：Part 1 是最简单的版本，Part 2 加上函数声明与调用，
Part 3 在此基础上加"海量重复调用 + 取模"的性能追问。

## 输入

Part 1：一串命令（`ADD n` / `SUB n` / `MULT n` / `DIV n`）。
Part 2/3：一段程序，由 `ADD n` / `MUL n` / `FUN name` ... `END`（声明函数，函数体只包含
`ADD`/`MUL`/`INV`，不允许嵌套 `FUN`）/ `INV name`（调用已声明的函数）组成；Part 3 额外允许
`REPEAT count name`（把 `name` 连续调用 `count` 次，`count` 可以到 `~10^15`）。

## API 契约（英文签名）

```python
def run_calculator(commands: list[str]) -> int
def run_snowcal(lines: list[str]) -> int
def run_snowcal_mod(lines: list[str]) -> int
```

## 规则

### Part 1 — String-Command Calculator（一手原题）

累加器从 `0` 开始，依次执行 `ADD n`（`+n`）、`SUB n`（`-n`）、`MULT n`（`*n`）、`DIV n`
（整数除法，**向零截断**，不是 Python `//` 的向下取整——两者只在符号不同时才不一样，比如
`-7 DIV 2` 向零截断是 `-3`，`//` 会给 `-4`）**(reconstructed，声明的选择)**；除以 0 抛
`ValueError`；未知命令抛 `ValueError`。

### Part 2 — SnowCal：单变量、函数声明与调用（一手原题）

单个全局变量 `X` 从 `0` 开始。`ADD n`/`MUL n` 直接作用于 `X`。`FUN name` ... `END` **声明**一个函数
（此时不执行函数体，只是把它记下来）；`INV name` 才真正**执行**这个函数体（函数体里的指令按顺序作用于
同一个全局 `X`，不是独立作用域）。函数可以 `INV` 其它函数（包括间接调用）。原文明确要求：
调用未声明的函数、或出现调用环（自己直接或间接调用自己）都必须报错——本 kit 的检测方式是维护"当前正在
执行的函数名集合"，一旦即将 `INV` 一个已经在这个集合里的函数就立刻报错，而不是真的死循环再检测超时
**(reconstructed 检测机制)**。

### Part 3 — 海量重复调用，取模，仿射映射记忆化 **(reconstructed)**

新增指令 `REPEAT count name`：把 `name` 连续调用 `count` 次（`count` 可以大到 `~10^15`），所有运算
对 `1_000_000_007` 取模。直接循环 `count` 次显然太慢；观察到每条指令对 `X` 的作用都是一个**仿射变换**
`x → a·x + b`（`ADD n` 是 `(a,b)=(1,n)`；`MUL n` 是 `(a,b)=(n,0)`；调用一个已经算好仿射映射的函数
也是复合仿射变换），于是给每个函数**只算一次**它整体的 `(a,b)`（记忆化），"连续调用 `count` 次"就是把
这个仿射映射自己复合 `count` 次，有闭式解：
- `a' = a^count mod MOD`（快速幂，`O(log count)`）
- `b' = b · (a^count - 1) / (a - 1) mod MOD`（等比数列求和，用费马小定理求 `(a-1)` 的模逆元；
  如果 `a mod MOD == 1`，退化成等差数列 `b' = b · count mod MOD`，因为这时 `a-1 ≡ 0`，不能求逆元）

这样 `REPEAT` 的开销只有 `O(log count)`，与 `count` 的大小无关。

## Worked examples（全部由 `solution.py` 实际运行得出）

- `run_calculator(["ADD 6", "SUB 3", "MULT 4", "DIV 2"])` = `6`（`(0+6-3)*4/2 = 12/2 = 6`）
- `run_calculator(["SUB 7", "DIV 2"])` = `-3`（`-7` 向零截断除以 `2`；向下取整会得到 `-4`）
- `run_snowcal(["ADD 3", "FUN double", "MUL 2", "END", "INV double"])` = `6`
- `run_snowcal(["FUN a", "INV b", "END", "FUN b", "INV a", "END", "INV a"])` → `ValueError`
  （`a` 调 `b`、`b` 调 `a`，间接环）
- `run_snowcal_mod(["ADD 3", "FUN double", "MUL 2", "END", "REPEAT 5 double"])` = `96`
  （`3 * 2^5 = 96`，与直接循环 5 次 `INV double` 结果一致）
- `run_snowcal_mod(["FUN inc", "ADD 1", "END", "REPEAT 1000000000000 inc"])` =
  `pow(10, 12, 1_000_000_007)` = `999993007`（`a=1` 分支：等差数列 `1 * 10^12 mod MOD`）

## `main()` 命令流

```
PART 1                              PART 2                          PART 3
ADD 6;SUB 3;MULT 4;DIV 2            5                                5
→ 6                                 ADD 3                            ADD 3
                                     FUN double                      FUN double
                                     MUL 2                            MUL 2
                                     END                              END
                                     INV double                      REPEAT 5 double
                                     → 6                              → 96
```
Part 1 每行一个完整程序，命令用 `;` 分隔。Part 2/3 第一行是接下来的指令行数 `N`，然后是 `N` 行程序
（`FUN`/`END` 占各自一行）。

## 边界清单

- Part 1：空程序（结果 `0`）、除以 0、未知命令
- Part 1：负数向零截断与向下取整不同的例子必须覆盖
- Part 2：只声明不调用（no-op）、函数调用其它函数（间接但无环）、调用未声明函数、直接自递归、
  间接互递归（环）
- Part 3：`REPEAT 0` 是恒等、`a mod MOD == 1`（纯 `ADD` 函数）必须走等差分支而不是除零、
  极大 `count`（`~10^15`）、未定义函数与调用环在 Part 3 依然要检测

## 追问

1. **为什么 `DIV` 要向零截断而不是向下取整？** 这是本 kit 声明的重建选择——大多数"计算器"类题目
   的直觉是"和数学课本的整数除法一致"（向零），而不是 Python `//` 的向下取整；两者只在正负号不同时
   才分叉，测试专门覆盖了这一点。
2. **调用环为什么不能靠"运行时间过长就判定超时"来发现？** 那样既慢又不确定（环外面套一层大循环
   会拖慢正常程序的检测），维护一个"当前调用链"集合是 `O(1)` 每次判断、确定性的做法。
3. **仿射映射复合为什么一定还是仿射？** `y = a2*(a1*x+b1)+b2 = (a2*a1)*x + (a2*b1+b2)`，代数上直接
   展开就是新的 `(a,b)`，这也是为什么"函数调用函数"依然能整体记忆化成一个仿射映射，不需要展开成
   具体数值再算。
4. **如果 `REPEAT` 出现在函数体内部（不止顶层）呢？** 本题的实现天然支持——`REPEAT` 只是又一种
   会被折进当前累积仿射映射的指令，出现在哪一层都一样处理。

## 来源与置信度

- **MED（聚合站，题面付费，仅预览可见）**：`kevin-2023-code/Tech-Interview-Questions`
  `companies/snowflake.md`，第 34 行 "String-Command Calculator"（2026-02 报告）、第 19 行
  "SnowCal"（2026-05 报告）。见 `../../../catalog/raw/github_repos.md` §2 第 19、34 行、§3。
  Part 1 的四个命令名与 Part 2 的 `ADD`/`MUL`/`FUN`/`END`/`INV` 语言元素、"检测未定义函数与无限
  递归"均为原文要求。
- `DIV` 向零截断的选择、无限递归的具体检测机制、Part 3 全部（`REPEAT`、取模、仿射映射记忆化）为重建。

## 考什么

S04 小型解释器 / 状态机（累加器上的指令流）· S06 图上的环检测（调用链构成的隐式有向图）·
S08 把"暴力循环"压缩成"矩阵/仿射映射快速幂"，识别可结合的线性变换是记忆化的关键。
