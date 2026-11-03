---
id: craft-dispatch-tables-5-scales-rules-as-data
node: craft.idioms.dispatch-tables
type: qa
step: 5
---
## Q
**分派表 · 从 atoi 的状态表到规则引擎**｜写法

字符串转整数（atoi）常见写法是一堆 if 判断空格、符号、数字、其他字符。把它写成状态表之后，和售货机的转移表、线上「配置驱动的规则引擎」有什么共同点？每一步放大，表带来的收益和代价怎么变？

## A
**要点。** 三个规模是同一个想法：把「什么条件下做什么」放进数据，控制流缩成「查表、执行」。LeetCode 级：状态 × 字符类别 → 下一状态，一个函数处理所有输入；LLD 级：状态 × 事件 → 新状态，可穷举测试；系统级：规则放在配置里，发布规则不发布代码。随规模增加，表的维护者从程序员变成运营，所以需要校验、版本和审计。

```python
INT_MAX, INT_MIN = 2**31 - 1, -2**31
START, SIGNED, NUMBER, END = range(4)
# 字符类别：0 空格, 1 正负号, 2 数字, 3 其他
TABLE = {
    START:  (START, SIGNED, NUMBER, END),
    SIGNED: (END, END, NUMBER, END),
    NUMBER: (END, END, NUMBER, END),
    END:    (END, END, END, END),
}

def klass(ch: str) -> int:
    if ch == " ": return 0
    if ch in "+-": return 1
    if ch.isascii() and ch.isdigit(): return 2
    return 3

def my_atoi(s: str) -> int:
    state, sign, n = START, 1, 0
    for ch in s:
        state = TABLE[state][klass(ch)]           # 整个控制流就是这一行
        if state == SIGNED:
            sign = -1 if ch == "-" else 1
        elif state == NUMBER:
            n = n * 10 + int(ch)
        elif state == END:
            break
    return max(INT_MIN, min(INT_MAX, sign * n))

for s in ["42", "   -42", "4193 with words", "words 987", "-91283472332", "+-12", "  +0 123"]:
    print(repr(s), my_atoi(s))
```

实际输出：

```
'42' 42
'   -42' -42
'4193 with words' 4193
'words 987' 0
'-91283472332' -2147483648
'+-12' 0
'  +0 123' 0
```

**变化。** 表在 LeetCode 里是性能无关的整洁；在 LLD 里换来穷举测试；在分布式系统里换来「不发版改规则」。同时风险也上升：配置里的一条错规则会同时影响所有机器，所以规则要在加载时校验（键是否合法、是否有遗漏的状态）、带版本号、能灰度、能回滚。

**信号。** 看到一串 `if x == A ... elif x == B ...`，每个分支做的是同一类事、只是参数不同时，先想表；分支里需要不同的局部逻辑、顺序依赖或复杂副作用时，不要。
