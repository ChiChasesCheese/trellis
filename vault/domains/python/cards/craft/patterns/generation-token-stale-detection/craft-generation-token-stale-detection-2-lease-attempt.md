---
id: craft-generation-token-stale-detection-2-lease-attempt
node: craft.patterns.generation-token-stale-detection
type: qa
step: 2
---
## Q
**代号令牌 · 租约被夺走后，旧拥有者为什么不能再动钱**｜模式

幂等转账里，拥有者占了键、开始执行，然后卡住了（垃圾回收停顿、网络挂起）。租约过期，新拥有者接手并完成了转账。旧拥有者醒来，也要走到「动钱」这一步。怎么保证钱最多动一次？

## A
**要点。** 每一轮拥有者有一个轮次号（attempt），接手时加一。动钱之前核对「我的轮次是不是记录里现在的轮次」，对不上就放弃，并且旧一轮也不唤醒等待者（等待者属于新一轮）。

```python
def move_money(rec, mine, check_attempt):
    if check_attempt and rec.attempt != mine:
        raise RuntimeError(f"租约已被收回（我是第 {mine} 轮，现在是第 {rec.attempt} 轮）")
    money["alice"] -= 60
    money["bob"] += 60
    rec.result = f"moved by attempt {mine}"

# 旧拥有者（第 1 轮）卡住，租约被接手（第 2 轮），新拥有者先转账，旧拥有者再来
```

转 60，alice 有 100，不检查与检查轮次各运行一次：

```
不检查   -> alice 余额 -20 （应当只扣一次，剩 40）
旧拥有者被拒: 租约已被收回（我是第 1 轮，现在是第 2 轮）
检查轮次 -> alice 余额 40 （应当只扣一次，剩 40）
```

**为什么。** 幂等转账里有两道保险：动钱前在锁内确认 `self._keys.get(k) is rec` 且结果尚未写入；收尾时 `if rec.attempt == mine` 才唤醒等待者。

**代价。** 租约时长要比正常执行时间长得多，否则健康的拥有者也会被夺走；被夺走的旧拥有者要承认「我的这一轮作废」，而不是报错重试。
