---
id: ai-decomposition-red-for-right-reason
node: ai.decomposition
type: qa
step: 3
---
## Q
智能体写出一个“会失败的测试”，也确实红了。为什么还要看它为什么红？

## A
**红要红在你假设的那个缺陷上**

- **同样是红**：断言失败、拼写错误（`NameError`）、夹具没建好，在测试结果里都只是一行失败；
- **只有断言失败才有信息**：它说明代码跑到了被测的行为，结果和期望不同；
- **做法**：读失败信息，确认是断言、数值和你的假设一致；然后才让它改代码；
- **并发类缺陷**：用线程和屏障制造交错，确认红来自竞争，而不是线程没起来；

```python
class Slot:
    def __init__(self): self.free, self.state = 0, "active"

def cancel(s):                                  # 缺陷：重复取消再次释放
    s.free += 1; s.state = "cancelled"

def test_cancel_twice():
    s = Slot(); cancel(s); cancel(s)
    assert s.free == 1, f"free={s.free}"

def test_typo():
    cancle(Slot())                              # 拼错了函数名

for t in (test_cancel_twice, test_typo):
    try: t()
    except AssertionError as e: print(t.__name__, "红在断言:", e)
    except Exception as e: print(t.__name__, "红在别处:", type(e).__name__)
```

**知识点：**拆成可验证的小步（Decomposition）
