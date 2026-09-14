# pc22 · Document Predicate Search Engine：练的是"倒排索引的集合代数 + 运算符优先级解析"

> [!tldr]
> - 这题考的是：文档搜索从纯 OR 到 AND/OR 优先级再到 NOT/括号+删除；Part 1 的命令名与 OR 语义一手预览原文，Part 2/3（含精确输出格式）**(reconstructed)**
> - 三步套路：倒排索引 `word -> doc id 集合` → 词之间取并集就是 OR → 加入 AND 优先级更高的递归下降解析器 → 加 NOT（全集减法）和括号分组
> - 最值得带走的一个模式：**倒排索引把查询开销从"文档总数"降到"命中词的倒排表大小"，AND/OR/NOT 天然对应集合的交/并/补运算，不需要逐文档扫描**

## 1. 题目在说什么（人话版）

`INSERT_DOC` 插入文档（一串词），`CHECK_CONTAINS "query"` 查询哪些文档匹配。Part 1 的查询是
纯 OR（命中任意一个词就算）；Part 2 变成真正的布尔表达式（AND 结合更紧）；Part 3 加上 NOT、
括号分组和 `DELETE_DOC`。

小例子：
```
INSERT_DOC 1 a b c; INSERT_DOC 2 b d
check_contains_or("a b c") -> [1]                      # 只有文档 1 命中 a/b/c 中任意一个
check_contains_bool("a AND b OR e")                    # (a AND b) OR e，AND 优先级更高
check_contains_full("NOT (a OR c)")                    # 全集减去命中 a 或 c 的文档
```

## 2. 读题：把文字变成模型

- **实体**：文档、词、倒排索引 `word -> doc id 集合`、查询表达式（AST）。
- **输入**：一串命令，每条命令产生至多一行输出。
- **输出**：匹配的文档 id，升序、空格分隔，无匹配输出 `NONE`（本 kit 声明的格式）。
- **状态**：倒排索引随 `INSERT_DOC`/`DELETE_DOC` 增量维护。
- **一句话建模**：这是一个 **"倒排索引 + 布尔表达式求值"** 问题；查询语法越来越复杂，但底层
  永远是集合运算。

> [!note] 为什么用倒排索引而不是每次扫描全部文档
> 倒排索引把每次查询的开销降到"命中词的倒排表大小"，而不是"文档总数"；`AND`/`OR` 直接是集合的
> 交/并，`NOT` 是"当前索引里存在的文档"全集减法，三者都不需要逐篇文档检查。

## 3. 下笔顺序

1. **问清**：查询没有命中时输出什么？重复 `INSERT_DOC` 同一个 id 算不算替换？
2. **Part 1 最小可用**：把 `query` 按空格切开的每个词，各自的倒排集合取并集。
3. **Part 2 叠加**：写一个递归下降解析器（`expr := term (OR term)*`，
   `term := factor (AND factor)*`），在倒排索引上对 AST 求值；显式拒绝 `NOT`/括号（题目还没
   引入，遇到就报错而不是默默忽略）。
4. **Part 3 叠加**：文法加上 `factor := NOT factor | '(' expr ')'`；`NOT` 用"当前索引里存在
   的全部文档 id"做差集；`DELETE_DOC` 把文档从倒排索引摘除。
5. **收尾**：同一 id 重复插入要整体替换（旧倒排项先清干净）；删除不存在的 id 是 no-op；括号
   不匹配、悬空操作符报错。

## 4. 代码怎么组织

```
class DocumentIndex:
    insert_doc / delete_doc                  # 增量维护倒排索引，三个 Part 共用
    check_contains_or(query)                 # Part 1：并集
    check_contains_bool(query)               # Part 2：解析 + 集合求值，拒绝 NOT/括号
    check_contains_full(query)               # Part 3：完整文法
_tokenize / _Parser / _eval_sets             # 递归下降解析器 + AST 求值，Part 2/3 共用
```
`_Parser` 和 `_eval_sets` 是 Part 2、Part 3 共用的核心；区别只在解析前要不要拒绝 `NOT`/括号
这一层校验。

## 5. 核心代码（骨架）

```python
_TOKEN_RE = re.compile(r"\(|\)|[^\s()]+")

class _Parser:
    def __init__(self, tokens): self.tokens, self.pos = tokens, 0
    def _peek(self): return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def _advance(self):
        tok = self.tokens[self.pos]; self.pos += 1; return tok
    def _expr(self):
        node = self._term()
        while self._peek() == "OR":
            self._advance(); node = ("OR", node, self._term())
        return node
    def _term(self):
        node = self._factor()
        while self._peek() == "AND":
            self._advance(); node = ("AND", node, self._factor())
        return node
    def _factor(self):
        tok = self._advance()
        if tok == "NOT": return ("NOT", self._factor())
        if tok == "(":
            node = self._expr(); self._advance(); return node   # consume ')'
        return ("WORD", tok)

def _eval_sets(node, index, universe):
    kind = node[0]
    if kind == "WORD": return set(index.get(node[1], ()))
    if kind == "AND": return _eval_sets(node[1], index, universe) & _eval_sets(node[2], index, universe)
    if kind == "OR": return _eval_sets(node[1], index, universe) | _eval_sets(node[2], index, universe)
    if kind == "NOT": return universe - _eval_sets(node[1], index, universe)
```

## 6. 面试里怎么说

- 开始前：「没有命中的时候输出什么？我建议用一个明确的字面量而不是空行，避免歧义。」
- 写 Part 1 时：「用倒排索引，每次查询是把命中词的倒排集合取并集，不逐文档扫描。」
- 到 Part 2 时：「布尔表达式的标准约定是 AND 比 OR 结合得紧，我写一个小的递归下降解析器产生
  AST，再在倒排索引上对 AST 求值；`NOT`/括号还没引入，我先显式拒绝，避免面试官以为我悄悄支持了
  还没讲的语法。」
- 交付时：「样例过了；`NOT` 的全集我用的是'当前索引里存在的文档'，删除过的文档不会被 `NOT`
  捞回来。」

## 7. 常见跑偏

- 每次查询都逐文档扫描一遍判断是否包含关键词，而不是维护倒排索引——功能正确但复杂度不对。
- 重复 `INSERT_DOC` 同一个 id 时没有先撤销旧倒排项，导致旧词的倒排集合里残留了这篇文档。
- `NOT` 的全集用"所有出现过的文档 id"而不是"当前还在索引里的文档 id"，导致删除过的文档被
  `NOT` 错误地捞回来。

## 8. 同族题 / 延伸

- 与 `pc26`（Top K Hashtags）同属"维护一个哈希结构随增量更新"的考法，但 pc22 考的是集合代数与
  运算符优先级解析，pc26 考的是去重计数与排序。
- 与 `pc01`（RBAC DAG 权限）同样涉及"图/索引上的集合运算"，但 pc01 是拓扑序 DP 求权限并集，
  pc22 是倒排索引上的布尔表达式求值。
- 练习命令：`python3 loop/mock.py start pc22`

## 索引行

| [pc22_document_predicate_search](pc22_document_predicate_search.md) | `../../loop/rounds/03_phone_coding/pc22_document_predicate_search/` | 电面 coding | 倒排索引把查询开销从"文档总数"降到"命中词的倒排表大小"，AND/OR/NOT 天然对应集合的交/并/补运算，不需要逐文档扫描 |
