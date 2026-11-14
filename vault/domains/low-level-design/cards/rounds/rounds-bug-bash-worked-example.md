---
id: rounds-bug-bash-worked-example
node: rounds.bug-bash
type: qa
step: 3
---
## Q
下面的代码读取每次 CI 运行的 JSON 结果文件，统计连续失败次数和通过率。其中埋了 4 个缺陷，找出来，说明触发条件和修法。

```python
import json
from datetime import datetime

def load_runs(paths, cache={}):
    runs = []
    for p in paths:
        if p not in cache:
            f = open(p)
            try:
                cache[p] = json.load(f)
            except Exception:
                continue
        runs.append(cache[p])
    return runs

def fail_streak(runs):
    """从最新一次往回数，连续失败了几次。"""
    ordered = sorted(runs, key=lambda r: datetime.fromisoformat(r["ts"]))
    count = 0
    for i in range(len(ordered) - 1, 0, -1):
        if ordered[i]["status"] != "fail":
            break
        count += 1
    return count

def pass_rate(runs, since):
    # since 带时区；r["ts"] 形如 "2026-11-14T03:00:00+00:00"
    recent = [r for r in runs if datetime.fromisoformat(r["ts"]) >= since]
    return sum(r["status"] == "pass" for r in recent) / len(recent) if recent else None
```

## A
**1. 可变默认参数，跨调用共享状态（第 4 行）：**
- 触发：同一进程里调两次，中间结果文件被重写。第二次仍返回旧内容；测试之间互相污染。
- 原因：`cache={}` 只在定义函数时创建一次。
- 修法：`cache=None`，函数内 `cache = {} if cache is None else cache`；真要缓存，按文件修改时间失效。

**2. 文件没关闭，资源泄漏（第 8 行）：**
- 触发：一次读几千个文件会耗尽文件描述符（`Too many open files`）；`python -X dev` 会打印 `ResourceWarning: unclosed file`。
- 修法：`with open(p, encoding="utf-8") as f:`，正常和异常路径都会关闭。

**3. 吞掉异常（第 11–12 行）：**
- 触发：一个文件写了一半、JSON 不合法，它被悄悄跳过，通过率按更少的运行算出来，没有任何提示。
- 修法：只捕获 `json.JSONDecodeError`，把文件名记入日志并计数，或者直接抛 `ValueError(f"{p}: 不是合法 JSON")`；由调用方决定是否容忍。

**4. 差一错误（第 20 行）：**
- 触发：3 次运行全是失败，返回 2。`range(len - 1, 0, -1)` 停在下标 1，从不检查下标 0。
- 修法：`for r in reversed(ordered):`，不再手写下标。

**不是缺陷的地方也要说：** `pass_rate` 两边都带时区，比较合法；空列表返回 `None`，没有除零。说出"我检查过、它是对的"，说明扫描是按清单做的。

**每条都补一个测试：** 例如三条 `{"ts": "2026-11-14T0<i>:00:00+00:00", "status": "fail"}`（i = 0、1、2），断言 `fail_streak(runs) == 3`；改回旧代码时它必须变红。
