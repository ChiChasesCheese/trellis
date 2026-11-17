---
id: fluency-mutability-instance-isolation-test
node: fluency.mutability
type: qa
step: 6
---
## Q
一个 `RateService` 的单元测试每个单独运行都通过，整套一起跑却偶尔失败，换一下执行顺序结果也变。怎么判断是共享可变状态在作怪？怎样写一个测试专门把它揪出来？

## A
**造两个实例，一个动，另一个不能变**

- **症状**：单独通过、一起失败、顺序一变结果就变，都指向状态在测试之间残留：类属性、模块级字典、可变默认参数、单例；
- **排查顺序**：搜类体里的 `= []`、`= {}`，搜 `def …(…=[])`，搜模块顶层的可变对象，搜 `lru_cache` 一类的缓存；
- **隔离测试的写法**：同一个类造两个实例，只对第一个操作，断言第二个仍是初始状态；再用同一份输入重复调用两次，断言结果一样（无状态、可重复）；
- **修法**：状态移到 `__init__` 里的 `self`；默认参数用 `None`；需要全局配置就显式传进去，不用模块变量；
- **并发时更重要**：共享的可变状态是线程之间互相踩踏的来源，每个请求自己一份状态，就不需要锁。

```python
class Registry:
    items = []                           # 隐蔽的共享状态
    def add(self, x):
        self.items.append(x)
    def snapshot(self):
        return list(self.items)

def test_instances_are_isolated(cls):
    a, b = cls(), cls()
    a.add("x")
    assert b.snapshot() == [], "state leaked between instances"
    assert a.snapshot() == ["x"]

try: test_instances_are_isolated(Registry)
except AssertionError as e: print("FAIL:", e)    # FAIL: state leaked between instances
```

<details class="pt"><summary>延伸</summary>

可以顺手加第三条断言：`a.snapshot()` 返回的列表被调用方改动后，`a.snapshot()` 的下一次结果不变。这和防御性拷贝的测试是同一类。

</details>

**知识点：**可变性与别名（Mutability & Aliasing）
