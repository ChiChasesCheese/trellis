---
id: cc-input-gram-parens-recursion
node: input.grammar
type: qa
---
## Q
Where do parentheses belong in a recursive-descent parser, and what makes the recursion terminate?

## A
**In the innermost function — `primary` — where `(` re-enters the top-level `expr` and then requires a matching `)`.**

```python
def parse_primary(t):
    if t.peek() == "(":
        t.next(); node = parse_expr(t); t.expect(")")
        return node
    return parse_comparison(t)
```

That single case gives you arbitrary nesting for free. Termination comes from the tokenizer: every path through `primary` either consumes at least one token or raises, so the position strictly advances. The two bugs to watch: forgetting `expect(")")` (which silently accepts `(a OR b`), and consuming the `(` twice.

## Q zh
在递归下降解析器里，括号属于哪一层？递归靠什么终止？

## A zh
**属于最内层的 `primary`：`(` 在那里重新进入顶层的 `expr`，随后要求一个匹配的 `)`。**

```python
def parse_primary(t):
    if t.peek() == "(":
        t.next(); node = parse_expr(t); t.expect(")")
        return node
    return parse_comparison(t)
```

这一个分支就免费给了你任意层嵌套。终止性来自分词器：经过 `primary` 的每条路径要么至少消耗一个 token，要么抛错，因此位置严格前进。要盯住的两个 bug：漏掉 `expect(")")`（会默默接受 `(a OR b`），以及把 `(` 消耗了两次。
