---
id: principles-temporal-coupling
node: principles.coupling
type: qa
step: 3
---
## Q
```python
svc = ReportService()
svc.store = store
svc.init()
svc.run()          # 少走一步就是 AttributeError 或 RuntimeError
```
说出这种耦合的名字、两个能识别它的信号，以及修法。

## A
**Temporal coupling（时序耦合）**——正确性依赖一个调用顺序，但这个顺序并没有被类型本身表达出来。信号：

- 方法开头写着 `if not self._initialized: raise RuntimeError(...)`；
- 给一个"没它就没法工作"的东西提供了单独的 setter（`svc.store = store`），也就是说构造函数放行了一个尚不完整的对象。

修法：**让不完整的对象根本构造不出来**——把所有必需的协作者都放进构造函数（或者用一个校验完才返回就绪对象的工厂函数），把 `init()` 里的内容并进构造过程。当几个阶段确实彼此不同时，把阶段编码进类型本身：一个 `open_connection()` 返回的对象只在"已打开"这个类型上才有 `query()` 方法，"未打开"状态下这个方法根本不存在。

同一种坏味道的放大版：跨对象的两次调用必须按固定顺序发生——把它们合并成一个方法，由这个方法自己拥有这个顺序。
