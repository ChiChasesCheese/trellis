---
id: testing-flaky-event-not-sleep
node: testing.flaky
type: qa
step: 3
---
## Q
要测「任务 A 比任务 B 晚完成时，结果顺序仍然正确」。让 A 先 `sleep(0.1)` 再返回，测试大部分时间是绿的，CI 繁忙时偶尔变红。为什么？该怎么造出确定的顺序？

## A
**用事件（Event）表达「等谁」，不靠睡眠表达「多久」**

- **`sleep` 是在赌**：赌 B 在 0.1 秒内一定先跑完；机器繁忙、线程被饿住时赌输，这就是偶发红；
- **Event 链**：A 等一个 `Event`，B 完成后 `set()`；顺序由因果保证，调度怎么走都一样；
- **反序完成**：想让后开始的先完成，让先开始的那个等后开始那个的事件；
- **所有等待都带超时**：`event.wait(timeout=5)`，错误的逻辑变成一次可读的失败，而不是整套测试挂住；
- **同样的做法**：测「睡眠审核器」这类慢依赖，用一个受控的替身代替真的睡眠，断言在它被放行之后再做。

```python
import threading

b_done, order = threading.Event(), []

def task_a():
    assert b_done.wait(timeout=5)          # 等 B，不是等多久
    order.append("a")

def task_b():
    order.append("b")
    b_done.set()

ta, tb = threading.Thread(target=task_a), threading.Thread(target=task_b)
ta.start(); tb.start(); ta.join(); tb.join()
print(order)                                # ['b', 'a']：A 先启动，B 先完成
```

**知识点：**不稳定测试（Flaky Tests）
