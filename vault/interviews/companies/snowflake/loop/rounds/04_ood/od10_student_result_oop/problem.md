# od10 · Student / Result — OA 里内嵌的继承与封装题

> 与 q19 同场的 2026-05 AIML 实习 OA 第二题（一手原帖）。原帖只给出骨架，本题的具体规则（校验、四舍五入、复查规则、排名）大部分为 **(reconstructed)**，逐条标注。

## 背景

候选人原帖：

> "student Enrollment System (OOP) Implement Student and Result classes. Result inherits from Student, stores 3 subject marks, calculates percentage, handles recheck requests. Pass mark is 33.33%. the HackerRank input handler was broken for this one. Had to edit the main function to get it working. difficulty was easy-med"

它说明两件事：**Snowflake 的 OA 不只考算法，会塞一道纯 OOP 题**；以及**平台给的 `main` 可能是坏的，你得会自己读 stdin**。

## API 契约（英文签名）

```python
class Student:
    def __init__(self, roll: int, name: str) -> None
    def describe(self) -> str                       # "<roll> <name>"

class Result(Student):
    def __init__(self, roll: int, name: str, marks: list[int]) -> None
    @property
    def marks(self) -> list[int]                    # a copy
    def percentage(self) -> Decimal                 # 2 places, ROUND_HALF_UP
    def passed(self) -> bool                        # percentage >= 33.33
    def report(self) -> str                         # "<roll> <name> <pct> PASS|FAIL"
    def recheck(self, subject: int, new_mark: int) -> str   # Part 2

class Registry:
    def add(self, result: Result) -> None           # ValueError on duplicate roll
    def get(self, roll: int) -> Result              # KeyError if missing
    def top(self, k: int) -> list[Result]           # Part 2
```

## 规则

### Part 1 — 继承、校验、百分比

- `Student`：`roll` 正整数，`name` 非空白（去掉首尾空白后保存）；否则 `ValueError`。**(reconstructed)**
- `Result` 继承 `Student`，**恰好 3 科**，每科 `0..100` 的整数；否则 `ValueError`。（"3 subject marks" 为原文；满分 100 为重建）
- `percentage()` = 总分 / 300 × 100，**用 `Decimal` 按 `ROUND_HALF_UP` 保留两位**，不许用 float 累加。**(reconstructed)**
- `passed()` ⇔ `percentage() >= 33.33`（"Pass mark is 33.33%" 为原文）。整数成绩下等价于总分 ≥ 100。
- `marks` 属性返回副本，外部修改不影响内部状态（封装）。

### Part 2 — 复查与排名 **(reconstructed)**

`recheck(subject, new_mark)`，`subject` 从 1 开始：
- 科目号或分数非法 → `REJECTED`，**不消耗**复查机会；
- 每科**只能复查一次**；已复查过 → `REJECTED`；
- 新分数更高 → 替换，返回 `UPDATED`；否则不变，返回 `UNCHANGED`（**仍消耗**这次机会）。

`Registry.top(k)`：按百分比降序、学号升序取前 k 个。

### 命令流

```
ADD <roll> <name> <m1> <m2> <m3>     构造失败或学号重复 → ERROR
REPORT <roll>                         不存在 → NOT_FOUND
RECHECK <roll> <subject> <mark>       不存在 → NOT_FOUND
TOP <k>                               学号空格分隔；为空 → -
```

## Worked examples（全部由 `solution.py` 实际运行得出）

```
PART 1
ADD 7 Ana 34 33 33
ADD 3 Bo 33 33 33
ADD 5 Cy 90 85 80
REPORT 7        → 7 Ana 33.33 PASS      （100/300 = 33.333… → 33.33，恰好及格）
REPORT 3        → 3 Bo 33.00 FAIL       （99/300）
REPORT 5        → 5 Cy 85.00 PASS
REPORT 9        → NOT_FOUND
```

```
PART 2
ADD 3 Bo 33 33 33
RECHECK 3 2 40  → UPDATED
REPORT 3        → 3 Bo 35.33 PASS
RECHECK 3 2 50  → REJECTED              （第 2 科已复查过）
RECHECK 3 1 10  → UNCHANGED             （更低，不改，但消耗第 1 科机会）
RECHECK 3 4 50  → REJECTED              （没有第 4 科）
ADD 5 Cy 90 85 80
ADD 8 Di 80 90 85
TOP 2           → 5 8                   （同为 85.00，学号升序）
TOP 0           → -
```

四舍五入：`[100,100,99] → 99.67`，`[1,1,0] → 0.67`，`[0,0,1] → 0.33`，`[0,0,0] → 0.00`。

## 边界清单

- 及格线边界：总分 100 与 99
- `Decimal` 两位小数与 HALF_UP；`0.00` 的字符串形式
- 非法构造 8 种（学号 0/负、名字空/空白、2 科/4 科、101、-1）
- `marks` 返回副本
- 学号重复 → `ERROR`；构造失败 → `ERROR`
- 复查：同科第二次、非法科目或分数不消耗、相等分数算 `UNCHANGED`、复查使 FAIL 变 PASS
- 排名同分按学号；`TOP` 超过人数；空注册表
- 性能：5 万人 + 5 万次复查 + 排名 3 秒内

## 追问

1. **为什么 `Result` 继承 `Student` 而不是组合？** 题目要求继承；面试里可以补一句"如果一个学生有多次考试，组合（Student has many Results）更合适"。
2. **为什么不用 float？** `33.33` 这种阈值用 float 比较会出现 `33.329999…`；成绩、金额一律 `Decimal` 或整数。
3. **复查应该改原对象还是生成新版本？** 要审计就保留历史（append-only），`marks` 取最新；本题只保留最新。
4. **平台给的 `main` 读不了输入怎么办？** 自己 `sys.stdin.read().splitlines()`，不要依赖模板。

## 来源与置信度

- **HIGH（一手，存在性与骨架）**：Reddit r/cscareerquestions `1t0ogu7`（2026-05-01，Snowflake AIML Intern HackerRank）：https://www.reddit.com/r/cscareerquestions/comments/1t0ogu7/ ；全文 `../../../../catalog/discovery/harvest/reddit_posts_2026-09-13.json`。
- **LOW**：interviewfox 2026 OA 回忆（"Student base class and Result subclass … 33.33% threshold, and recheck functionality"），`../../../../catalog/raw/ood.md` #10。
- 具体规则为重建（见各条标注）。

## 考什么

S09 类设计先定契约（继承、校验、封装）· 金额/成绩用 `Decimal` · 读 stdin 不依赖平台模板。
