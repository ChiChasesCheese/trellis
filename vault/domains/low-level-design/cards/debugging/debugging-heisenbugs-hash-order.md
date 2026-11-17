---
id: debugging-heisenbugs-hash-order
node: debugging.heisenbugs
type: qa
step: 4
---
## Q
单线程、没有随机数、没有时钟，一个测试在本机连跑十次都绿，CI 上却时绿时红。断言比的是「第一个用户的名字」，用户来自一个 `set`。哪里在变？怎么钉住、怎么修？

## A
**字符串的哈希每个进程随机，集合的遍历顺序跟着变**

- **来源**：`str` 和 `bytes` 的哈希默认按进程加盐（3.3 起），同一组元素在不同进程里落进集合的顺序可以不同；
- **为什么本机总绿**：一次 `pytest` 只起一个进程，一个进程内顺序是固定的；CI 每次新起进程，才换盐；
- **钉住复现**：设 `PYTHONHASHSEED=<固定值>` 跑，红绿就变成确定的；逐个试几个种子，找到红的那个；
- **修代码，不是固定种子**：对外的顺序要写进合同并显式排序（`sorted`、带键排序）；`dict` 按插入顺序，可以放心依赖，`set` 不行；
- **同类**：遍历 `set` 拼字符串、把 `set` 转 `list` 后取下标、按 `hash()` 分桶，都会这样随进程变。

```python
import os, subprocess, sys

code = "print(list({'alice', 'bob', 'carol'})[0])"
firsts = set()
for seed in range(1, 6):
    env = {**os.environ, "PYTHONHASHSEED": str(seed)}
    out = subprocess.run([sys.executable, "-c", code], env=env,
                         capture_output=True, text=True).stdout.strip()
    firsts.add(out)
print(sorted(firsts))          # 3.11 实测：['alice', 'carol']，不止一种
print(sorted({'alice', 'bob', 'carol'})[0])   # alice：排序后稳定
```

<details class="pt"><summary>延伸</summary>

分组、分片要跨进程稳定时，不能用内置 `hash()`，要用 `hashlib`（如 `sha256`）算出的值；功能开关的分桶就是这个道理。

</details>

**知识点：**时序与共享状态的 bug（Heisenbugs）
