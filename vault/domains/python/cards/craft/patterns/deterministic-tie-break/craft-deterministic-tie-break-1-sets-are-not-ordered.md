---
id: craft-deterministic-tie-break-1-sets-are-not-ordered
node: craft.patterns.deterministic-tie-break
type: qa
step: 1
---
## Q
**确定性平局规则 · 同一份输入，为什么测试有时过有时不过**｜写法

通知服务向用户启用的所有渠道（短信、邮件、推送、Slack）各发一条。渠道存在一个 `set` 里，`for ch in channels` 直接遍历。测试断言「第一条发出的是邮件」，有时过，有时不过，重跑又好了。原因是什么？怎么让输出可预测？

## A
**要点。** Python 的 `str` 哈希在每个进程启动时随机加盐（防哈希碰撞攻击），所以字符串集合的迭代顺序**每次运行都可能不同**。依赖集合或字典（对哈希顺序而言）迭代顺序的代码，输出就不稳定。修法：凡是输出顺序会被观察到（返回给调用方、写日志、断言），在边界上 `sorted(...)`。

```python
@property
def target_channels(self) -> tuple[str, ...]:
    """按名字排序，让扇出的顺序可预测——测试因此不必迁就 set 的迭代顺序。"""
    return tuple(sorted(self.enabled_channels))
```

```python
import subprocess, sys

CODE = '''
channels = {"sms", "email", "push", "slack"}
print("set 迭代:", list(channels), " sorted:", sorted(channels))
'''
for seed in ("1", "2", "3"):                  # PYTHONHASHSEED 控制字符串哈希的盐
    out = subprocess.run([sys.executable, "-c", CODE], env={"PYTHONHASHSEED": seed},
                         capture_output=True, text=True).stdout.strip()
    print(f"PYTHONHASHSEED={seed}:", out)
```

同一个集合在三个进程里（`PYTHONHASHSEED` 控制加盐）：

```
PYTHONHASHSEED=1: set 迭代: ['sms', 'push', 'slack', 'email']  sorted: ['email', 'push', 'slack', 'sms']
PYTHONHASHSEED=2: set 迭代: ['push', 'sms', 'slack', 'email']  sorted: ['email', 'push', 'slack', 'sms']
PYTHONHASHSEED=3: set 迭代: ['sms', 'slack', 'push', 'email']  sorted: ['email', 'push', 'slack', 'sms']
```

**为什么。** 不确定的输出有两层伤害：测试时偶发失败，没人敢信红灯；生产里相同请求在两台机器上给出不同顺序，复现不了问题。字典自 Python 3.7 起保持插入顺序，所以字典是确定的，但"先插入谁"本身可能来自集合或并发，问题只是后移。

**代价。** `sorted` 要求元素可比较，且是 O(n log n)；元素很多、只需要最小的 k 个时用 `heapq.nsmallest`。排序键要选业务上稳定的东西（名字、编号），不要选 `id(obj)` 或 `hash(obj)`，它们本身就随进程变。

**怎么发现。** 用不同的 `PYTHONHASHSEED` 反复跑测试套件；顺序相关的失败会现形。
