# pc22 · Document Predicate Search Engine — 倒排索引 OR → AND/OR 优先级 → NOT/括号 + 删除

> TrueInterview 87 题清单第 26 题，2026-04 报告。Part 1 的命令名与"OR 语义"是一手预览原文；
> Part 2、Part 3（包括精确输出格式）**(reconstructed)**。

## 背景

TrueInterview（`kevin-2023-code/Tech-Interview-Questions`，见 `../../../catalog/raw/github_repos.md`
§2 第 26 行、§3）列出 Snowflake 一轮 Algorithm 题 "Document Predicate Search Engine"：
`INSERT_DOC` 插入文档，`CHECK_CONTAINS "a b c"` 查询——预览明确说这是"OR over words"，即只要文档命中
查询词里的**任意一个**就算匹配。预览没有给出更复杂的布尔语法、输出格式细节、删除接口，本 kit 按
"OR → AND/OR 优先级 → NOT/括号 + 删除"的自然难度递进补齐 Part 2、Part 3。

## 输入

一串命令（stdin，每行一条），每条命令产生**至多一行**输出（`INSERT_DOC`/`DELETE_DOC` 不产生输出）：
- `INSERT_DOC <id> <word1> <word2> ...`：插入 / 覆盖一篇文档（`id` 是整数，`words` 是空格分隔的普通词）
- `DELETE_DOC <id>`：删除一篇文档（Part 3 引入）
- `CHECK_CONTAINS "<query>"`：查询，`query` 用英文双引号包住

## API 契约（英文签名）

```python
class DocumentIndex:
    def insert_doc(self, doc_id: int, words: list[str]) -> None
    def delete_doc(self, doc_id: int) -> None
    def check_contains_or(self, query: str) -> list[int]     # Part1
    def check_contains_bool(self, query: str) -> list[int]   # Part2
    def check_contains_full(self, query: str) -> list[int]   # Part3
```

## 规则

底层用**倒排索引**（`word -> 命中该词的 doc id 集合`）实现，随 `INSERT_DOC`/`DELETE_DOC` 增量维护，
每次查询都是索引上的集合运算，不逐篇文档扫描。

### Part 1 — 纯 OR（一手原题）

`CHECK_CONTAINS "a b c"` = 查询词之间是 **OR**：文档只要命中 `a`/`b`/`c` 中任意一个词就匹配。
`check_contains_or(query)` 就是把 `query` 按空格切开的每个词各自的倒排集合做**并集**。
再次 `INSERT_DOC` 同一个 `id` 会**整体替换**这篇文档（先撤销旧倒排项，再登记新的）。

### Part 2 — AND / OR，AND 优先级更高 **(reconstructed)**

查询变成一个真正的布尔表达式，可以出现 `AND`、`OR` 关键字，**`AND` 结合得比 `OR` 紧**（和大多数
语言的布尔运算符优先级一致）：`"a AND b OR e"` 等价于 `"(a AND b) OR e"`。本 Part **不支持**
`NOT` 和括号——遇到就是 `ValueError`（这两个到 Part 3 才引入，提前出现被当成语法错误，而不是被
默默忽略）。

### Part 3 — NOT、括号、删除文档 **(reconstructed)**

`check_contains_full` 支持完整语法：`NOT`（优先级最高）、括号分组、`AND`/`OR`（同 Part 2 优先级）。
文法：
```
expr   := term (OR term)*
term   := factor (AND factor)*
factor := NOT factor | WORD | '(' expr ')'
```
`NOT x` 的语义是"倒排索引里**当前存在**的所有文档 id" 减去 `x` 命中的集合（不是"所有理论上可能的
文档"，删除过的文档不算在全集里）。`DELETE_DOC <id>` 把该文档从倒排索引里摘除（`id` 不存在时是
no-op，不报错）。

## 输出格式（本 kit 声明，题面未给出）

每条 `CHECK_CONTAINS` 命令输出一行：匹配的文档 id **按数值升序、空格分隔**；如果没有任何匹配，
输出字面量 **`NONE`**（不是空行）。

## Worked examples（全部由 `solution.py` 实际运行得出）

- 插入 `1:{a,b,c}`、`2:{b,d}`、`3:{e}`：`check_contains_or("a b c")` = `[1, 2]`
- 插入 `1:{a,b}`、`2:{e}`、`3:{a}`：`check_contains_bool("a AND b OR e")` = `[1, 2]`
  （`3` 只有 `a` 没有 `b`，`(a AND b)` 不成立，`3` 不在结果里）
- 插入 `1:{a,b}`、`2:{b}`、`3:{c}`：`check_contains_full("NOT (a OR c)")` = `[2]`
- 删掉 `id=1` 后 `check_contains_or("d")` = `[]`（Part 1 空结果是空列表；`main()` 的行输出层
  才把空列表转成字面量 `NONE`）
- `check_contains_bool("NOT a")` → `ValueError`（Part 2 不支持 `NOT`）

## `main()` 命令流

```
PART 1                              PART 2                                  PART 3
INSERT_DOC 1 a b c                  INSERT_DOC 1 a b                        INSERT_DOC 1 a b
INSERT_DOC 2 b d                    INSERT_DOC 2 e                          INSERT_DOC 2 b
CHECK_CONTAINS "a b c"              INSERT_DOC 3 a                          INSERT_DOC 3 c
→ 1 2                               CHECK_CONTAINS "a AND b OR e"           CHECK_CONTAINS "NOT (a OR c)"
                                     → 1 2                                  DELETE_DOC 1
                                                                             CHECK_CONTAINS "a"
                                                                             → 2
                                                                               NONE
```

## 边界清单

- 查询没有任何文档命中 → 输出 `NONE`
- 同一个 `id` 重复 `INSERT_DOC` → 整体替换（旧倒排项必须清干净，不能残留）
- Part 2：查询里出现 `NOT`、`(`、`)` → `ValueError`
- Part 3：`DELETE_DOC` 一个不存在的 `id` → no-op，不报错
- Part 3：`NOT` 的全集是"当前索引里存在的文档"，删除过的文档不应该被 `NOT` 捞回来
- Part 3：括号不匹配、悬空操作符（如 `"a AND"`）→ `ValueError`

## 追问

1. **为什么用倒排索引而不是每次查询都扫描所有文档？** 倒排索引把每次查询的开销从"文档总数"降到
   "命中词的倒排表大小"；`AND`/`OR` 直接是集合交/并，`NOT` 是全集减法，三者都是 O(结果规模) 级别的
   操作，不需要逐篇检查。
2. **`AND` 优先级更高，为什么不干脆要求用户自己加括号？** 这是布尔表达式的标准约定（和大多数编程语言
   的 `&&`/`||` 一致），减少"简单查询也要写括号"的负担；Part 3 加上括号是给用户在需要打破默认优先级
   时用的，不是唯一的分组方式。
3. **Part 2 为什么要显式拒绝 `NOT`/括号，而不是"忘了实现就不管"？** 显式拒绝能在电面里体现"我知道
   这道题还没到这一步"，避免面试官以为你悄悄支持了还没讲的语法、或者反过来以为你没考虑到边界。

## 来源与置信度

- **MED（聚合站，题面付费，仅预览可见）**：`kevin-2023-code/Tech-Interview-Questions`
  `companies/snowflake.md`，2026-04 报告，"Document Predicate Search Engine"，Algorithm。见
  `../../../catalog/raw/github_repos.md` §2 第 26 行、§3。`INSERT_DOC`/`CHECK_CONTAINS` 命令名
  与"OR over words"语义为原文。
- 精确输出格式（`NONE`、升序空格分隔）、Part 2、Part 3 全部为本 kit 重建。

## 考什么

S09 倒排索引与集合运算 · S04 递归下降解析器（表达式文法、运算符优先级）· 增量维护索引（插入替换、
删除）而不是每次查询重建。
