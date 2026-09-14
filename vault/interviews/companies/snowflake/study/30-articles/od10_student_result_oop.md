# od10 · Student / Result OOP：练的是"OA 里的 OOP 题，考的是校验、精度和封装"

> [!tldr]
> - 与 q19 同场的 2026-05 AIML 实习 OA 第二题。**原帖只给骨架（继承、3 科、百分比、及格线 33.33%、复查），校验范围、四舍五入、复查规则、排名全部是 (reconstructed)**
> - 这题考的是：继承关系、构造校验、`Decimal` 百分比、封装（不暴露可变内部状态）、一次性复查的状态规则
> - 三步套路：先写契约与不变量 → `Result.__init__` 先 `super()` 再校验 → 复查"先校验、再查是否用过、再比较"
> - 最值得带走的一个模式：**成绩、金额、阈值比较一律 `Decimal` 或整数**——`33.33` 这种阈值用 float 比较迟早出错

## 类设计先定契约

```python
class Student:
    def __init__(self, roll: int, name: str) -> None: ...     # roll > 0，name 非空白
    def describe(self) -> str: ...                            # "<roll> <name>"

class Result(Student):
    def __init__(self, roll, name, marks: list[int]) -> None: ...  # 恰好 3 科，0..100
    @property
    def marks(self) -> list[int]: ...                         # 返回副本
    def percentage(self) -> Decimal: ...                      # HALF_UP 两位
    def passed(self) -> bool: ...                             # >= 33.33
    def report(self) -> str: ...
    def recheck(self, subject: int, new_mark: int) -> str: ...     # UPDATED/UNCHANGED/REJECTED

class Registry:
    def add(self, r: Result) -> None: ...     # 重复学号 ValueError
    def get(self, roll: int) -> Result: ...   # 不存在 KeyError
    def top(self, k: int) -> list[Result]: ...
```

**不变量**：
1. 构造成功的 `Result` 永远恰好 3 科、每科 0–100。
2. 外部拿到的 `marks` 是副本，改它不影响内部。
3. 每科至多一次**有效**复查（非法请求不消耗机会）；复查只升不降。
4. 百分比是确定的十进制值，不受浮点误差影响。

## 1. 题目在说什么（人话版）

建两个类：学生（学号、名字）和成绩（继承学生，多了三科分数）。能算百分比、判断是否及格、打印一行报告。追问：学生可以申请复查某一科；再加一个注册表支持按成绩排名。

```
ADD 7 Ana 34 33 33  → REPORT → 7 Ana 33.33 PASS   （100/300，恰好及格）
ADD 3 Bo 33 33 33   → REPORT → 3 Bo 33.00 FAIL
```

## 2. 读题：把文字变成模型

- **实体**：学生、成绩、注册表。
- **输出**：命令流逐行输出；非法 ADD 为 `ERROR`，不存在为 `NOT_FOUND`。
- **状态**：`_marks` 列表、`_rechecked` 集合、注册表的 `roll → Result` 字典。
- **一句话建模**：这是一个 **"带校验与一次性状态规则的继承类 + 一个字典注册表"**。

> [!note] 为什么 `Result` 继承而不是组合
> 题目要求继承；面试里补一句"一个学生多次考试时，组合（Student has many Results）更合适"是加分项。

## 3. 下笔顺序

1. **先把契约与四条不变量写在注释里**，和面试官确认满分、四舍五入方式、复查规则。
2. `Student.__init__` 校验；`Result.__init__` 先 `super().__init__`，再校验 3 科。
3. `percentage`：`Decimal(sum) * 100 / 300`，`quantize(Decimal("0.01"), ROUND_HALF_UP)`。
4. `marks` 属性返回 `list(self._marks)`。
5. `recheck`：非法 → `REJECTED`（不记录）；已复查 → `REJECTED`；记录已复查；更高 → 替换 `UPDATED`，否则 `UNCHANGED`。
6. `Registry.top`：`sorted(key=(-percentage, roll))`。
7. **命令流**：自己读 stdin——原帖说平台模板的 `main` 是坏的。

## 4. 代码怎么组织

```
Student / Result / Registry          # 领域对象，只负责规则
run_commands(lines)                  # 解析 + 分发 + 格式化，吞掉 ValueError/KeyError 转成输出
part1 / part2 / main
```
异常在领域层抛出，在命令层翻译成 `ERROR` / `NOT_FOUND`——领域对象不知道输出格式。

## 5. 核心代码骨架

```python
class Result(Student):
    def __init__(self, roll, name, marks):
        super().__init__(roll, name)
        if len(marks) != 3 or any(not isinstance(m, int) or not 0 <= m <= 100 for m in marks):
            raise ValueError("need exactly 3 marks in 0..100")
        self._marks, self._rechecked = list(marks), set()

    @property
    def marks(self):
        return list(self._marks)

    def percentage(self):
        return (Decimal(sum(self._marks)) * 100 / 300).quantize(Decimal("0.01"), ROUND_HALF_UP)

    def passed(self):
        return self.percentage() >= Decimal("33.33")

    def recheck(self, subject, new_mark):
        if not 1 <= subject <= 3 or not 0 <= new_mark <= 100:
            return "REJECTED"                         # 非法请求不消耗机会
        if subject in self._rechecked:
            return "REJECTED"
        self._rechecked.add(subject)
        if new_mark > self._marks[subject - 1]:
            self._marks[subject - 1] = new_mark
            return "UPDATED"
        return "UNCHANGED"
```

## 6. 每个 part 叠加什么

| Part | 改动 |
|---|---|
| 1 | 继承、校验、Decimal 百分比、报告、注册表 add/get |
| 2 | 复查规则、排名 |

## 7. 常见坑

- float 百分比：`100/300*100 = 33.33333…`，四舍五入方式不一致时边界翻转。
- `marks` 直接返回内部列表：外部 `append` 就破坏"恰好 3 科"。
- 复查的消耗语义：非法请求消耗了机会；或更低分数没消耗。
- 学号重复没报错；排名同分没按学号。
- 依赖平台给的 `main`。

## 8. 并发追问怎么答

1. **两个请求同时复查同一科？** "检查是否用过 + 记录用过 + 改分"是 check-then-act，每个 `Result` 一把锁包住 `recheck`。
2. **注册表并发 add 同一学号？** 字典插入前的存在性检查与插入必须原子；一把注册表锁，或存储层唯一约束。
3. **怎么测？** 多线程同时对同一科发 10 次更高分数的复查，断言恰好一次 `UPDATED`。

## 9. 自测清单

- [ ] 写出四条不变量
- [ ] 说清为什么用 Decimal
- [ ] 说清复查"非法不消耗、合法都消耗"的理由

## 相关题与 skills

S09 类设计先定契约。相关：`q19`（同一场 OA）、Stripe 金额题（`study/00-essentials/04-money-and-rounding.md` 同一精度纪律）。
