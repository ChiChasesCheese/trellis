---
id: testing-testable-design-pure-core
node: testing.testable-design
type: qa
step: 3
---
## Q
一个限流器要「每个窗口内最多放行 N 个请求」。把判断逻辑和线程、锁、时钟都写在一个类里，测试为什么难写？怎么拆？

## A
**核心写成纯逻辑，线程和时钟放到外壳**

- **核心**：`admit(now) -> bool` 只依赖入参和自己的状态；没有线程、没有锁、不读时钟；
- **测试**：一串时间戳进去，一串 True/False 出来，断言一行；边界（刚好等于窗口长度）也是一行；
- **外壳**：另一层负责取当前时间、加锁、多线程调用；它很薄，只剩「加锁后调用核心」，用少量并发测试覆盖；
- **好处**：难的逻辑（边界、清理）在没有并发的环境里测透；并发测试只需证明外壳没有破坏核心；
- **决策**：当逻辑本身有边界和状态时才拆；三行的包装不需要一个独立的核心。

```python
class AdmissionWindow:                      # 无线程、无时钟：输入决定输出
    def __init__(self, limit: int, window: float):
        self.limit, self.window, self.stamps = limit, window, []

    def admit(self, now: float) -> bool:
        self.stamps = [t for t in self.stamps if now - t < self.window]
        if len(self.stamps) >= self.limit: return False
        self.stamps.append(now)
        return True

w = AdmissionWindow(2, 10)
print([w.admit(t) for t in (0, 1, 2, 10, 11)])    # [True, True, False, True, True]
```

**知识点：**可测的设计（Design for Testability）
