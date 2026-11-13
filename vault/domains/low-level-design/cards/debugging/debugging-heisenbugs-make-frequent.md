---
id: debugging-heisenbugs-make-frequent
node: debugging.heisenbugs
type: qa
step: 2
---
## Q
一个计数器在 4 个线程并发自增后偶尔少几个，CI 里大约 100 次运行失败 1 次。怎么把它变成稳定复现？修完之后要跑多少次才敢说修好了？

## A
**放大出错窗口、增加竞争、大量重复；修复后用「0 次失败的运行次数」换算有多大把握。**

```python
def work():
    nonlocal count
    for _ in range(20_000):
        v = count
        between()              # 读和写之间的窗口
        count = v + 1
```

4 个线程各自增 20,000 次，Python 3.14 实测每种设置跑 5 次、丢失的更新数：

| 设置 | 丢失 |
|---|---|
| `between` 是空函数，默认切换间隔 5 ms | 5 次都是 0 |
| 空函数，`sys.setswitchinterval(1e-6)` | 每次约 41,000–51,000 |
| `between` 里 `time.sleep(0)`（主动让出 GIL） | 每次约 60,000 |

- **放大窗口：** 在怀疑的读和写之间插入 `time.sleep(0)` 或短暂休眠。插入后必现，就证明了「这两步之间缺少同步」这个假设。
- **增加切换：** `sys.setswitchinterval(1e-6)` 让解释器频繁切换线程；C/C++ 里加线程数、把机器压满（`stress-ng --cpu 0`）。
- **大量重复：** `pytest --count=1000 -x tests/test_counter.py`（需要 `pytest-repeat`），或者在 shell 里 `for i in $(seq 1000); do ... || break; done`，第一次失败就停并保留现场。
- **固定其他变量：** 随机种子、测试顺序、输入数据都固定，只留并发这一个变量。
- **要跑多少次才敢说修好：** 原失败率是 1/100 时，跑 n 次全都通过的概率是 0.99^n。n = 300 时约 5%，也就是说「300 次全过」只有约 5% 的可能是运气。经验法则（三法则，rule of three）：n 次 0 失败，可以以 95% 的把握说真实失败率低于 3/n。
- **最好的证据：** 先用放大窗口的版本让它稳定失败，修复后同样的版本稳定通过。
