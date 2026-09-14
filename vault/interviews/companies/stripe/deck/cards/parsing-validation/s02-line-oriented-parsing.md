---
id: s02-line-oriented-parsing
node: stripe.parsing-validation
type: qa
---

## Q
为什么几乎每道 Stripe OA 题的前 10 分钟都花在解析上？遇到"多种记录类型混在 stdin 纯文本里，靠第一个 token 区分"、"setup 行可能出现在文件任何位置，但语义上先于所有事件生效"这类题面，标准做法和必须遵守的纪律是什么？

## A
**为什么考**：几乎每道题的前 10 分钟都是解析。Stripe 员工在 Blind 上的原话是
"input parsing, creating classes, proper data structures, business logic" —— 解析排第一。

**怎么识别**：输入是 stdin 上的纯文本，多种记录类型混在一起，靠第一个 token 区分。

**标准做法**：

```python
def parse(lines):
    for raw in lines:
        line = raw.strip()
        if not line:                      # 空行永远先跳过
            continue
        parts = [p.strip() for p in line.split(",")]   # 容忍逗号周围的空格
        kind, rest = parts[0], parts[1:]
        ...
```

四条纪律：
1. **先 `strip()` 再判空**，空行不是错误。
2. **每个字段都 `strip()`**，题面写 "spaces around commas tolerated" 时这是必须的。
3. **用 `maxsplit` 保护含分隔符的字段**：`line.split(",", 2)` 让第 3 个字段里可以有逗号。
4. **setup 行可能出现在文件任何位置**，但语义上"先于所有事件生效" → **两遍扫描**：
   第一遍只收 setup，第二遍只处理事件。

**典型翻车**：把 setup 和事件放在一个循环里按出现顺序处理 —— 题面明确说
"Setup lines are applied **before** any event, wherever they appear"。
