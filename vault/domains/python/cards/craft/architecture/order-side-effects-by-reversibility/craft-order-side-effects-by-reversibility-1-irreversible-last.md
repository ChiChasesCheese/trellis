---
id: craft-order-side-effects-by-reversibility-1-irreversible-last
node: craft.architecture.order-side-effects-by-reversibility
type: qa
step: 1
---
## Q
**副作用按可逆性排序 · 下单的三步，顺序怎么排**｜架构

下单要做三件事：预留库存（失败可撤）、扣款（可能被拒，事后能退）、发确认邮件（发出去收不回）。最容易写的顺序是按「先通知用户」「再处理」。如果扣款被拒，三种顺序各会留下什么？

## A
**要点。** 把多步操作里的副作用按可逆性排序：先做会失败的、可回滚的，最后做不可撤销的。失败总会发生，而撤销只能撤销已经做的事；不可逆的步骤放在最后，前面的失败就不会留下收不回的东西。

```python
@dataclass
class Step:
    name: str
    action: Callable[[], None]
    undo: Callable[[], None] | None            # None = 不可撤销

def run(steps: list[Step]) -> list[str]:
    log, done = [], []
    for s in steps:
        try:
            s.action()
        except RuntimeError as e:
            log.append(f"{s.name} 失败: {e}")
            for d in reversed(done):                 # 倒序撤销已完成的
                if d.undo is None:
                    log.append(f"  {d.name} 已经做了，撤销不了")
                else:
                    d.undo(); log.append(f"  撤销 {d.name}")
            return log
        done.append(s)
        log.append(f"做了 {s.name}")
    return log

def charge_declines() -> None:
    raise RuntimeError("卡被拒")

ok = lambda: None
reserve = Step("预留库存", ok, ok)
charge = Step("扣款", charge_declines, ok)
email = Step("发确认邮件", ok, None)

print("\n".join(run([email, reserve, charge])))
print("---")
print("\n".join(run([reserve, charge, email])))
```

分别以 `[email, reserve, charge]` 和 `[reserve, charge, email]` 的顺序运行，实际输出：

```
做了 发确认邮件
做了 预留库存
扣款 失败: 卡被拒
  撤销 预留库存
  发确认邮件 已经做了，撤销不了
---
做了 预留库存
扣款 失败: 卡被拒
  撤销 预留库存
```

**为什么。** 邮件先发，用户收到「订单成功」却没扣到款，只能再发一封更正邮件；邮件放最后，失败路径上根本没有发出去。

**易错。** 不是所有步骤都能排出完美顺序：扣款成功和落库之间仍有窗口。这时靠补偿（退款）和幂等收尾，排序的作用是让需要补偿的情形尽可能少。

**简化。** 这段代码把失败的那一步当成原子的：扣款被拒就等于什么都没发生，所以只撤销已完成的步骤。动作可能做到一半才抛异常时，失败的那一步自己也要补偿，见后面讲 Saga 成对声明的那一张。
