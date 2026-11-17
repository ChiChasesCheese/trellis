---
id: bank-log-processing-bad-lines
node: bank.practical.log-processing
type: qa
step: 2
---
## Q
日志里混着空行、被截断的行、时间戳不是数字的行。解析时写 `try: ... except: continue` 一律跳过，会留下什么隐患？怎样处理才算对？

## A
**坏行要记行号和原文，再继续**

- **静默跳过的隐患**：上游改了格式（比如多了一列），几乎每一行都成了「坏行」，统计照常输出，只是数字全错，没有人知道；
- **三件事一起做**：计数、留前几条样本（行号加原文）、继续。坏行比例超过阈值时整体失败，还是照常输出，由合同决定，解析器不擅自决定；
- **`try` 要短，`except` 要窄**：`try` 里只放 `split` 和 `int`，只接 `ValueError`。裸 `except:` 连 `KeyboardInterrupt` 一起吞；`except Exception` 会把解析代码自己的 bug 当成坏行；
- **坏行策略做成参数**：解析函数收一个 `on_bad(n, line)`，调用方决定是计数、抛异常还是写旁路文件，解析逻辑不用改；
- **空行与残行**：空行拆不出三段，同样是 `ValueError`，不用特判。读一个还在写入的文件时，最后一行可能没有换行符，说明还没写完，下一轮再解析。

```python
def parse(lines, on_bad):
    for n, line in enumerate(lines, 1):
        try:
            ts, level, msg = line.rstrip("\n").split(" ", 2)
            rec = (int(ts), level, msg)
        except ValueError:                   # try 里只放会抛 ValueError 的解析
            on_bad(n, line)
            continue
        yield rec

bad = []
rows = ["1 INFO boot", "", "x INFO oops", "3 WARN", "4 ERROR disk"]
print(list(parse(rows, lambda n, line: bad.append((n, line)))))
print(bad)                                   # 行号 + 原文，不是一个静默的计数
```

<details class="pt"><summary>延伸</summary>

`yield` 放在 `try` 之外还有一个好处：消费者那边出的错不会被解析的 `except` 接住。「失败要留下可查的痕迹，而不是静默」是同一条原则，在流式处理里表现为：坏数据既不能让整批作废，也不能悄悄消失。

</details>

**知识点：**日志处理与聚合（Log Processing）
