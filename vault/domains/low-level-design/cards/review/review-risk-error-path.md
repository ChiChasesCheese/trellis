---
id: review-risk-error-path
node: review.risk-patterns
type: qa
step: 1
---
## Q
评审一个 diff，新增的函数是：打开连接、取数据、没有数据就抛异常、最后关闭连接。主路径测试都过了。你为什么还要盯着“抛异常那一行”？

## A
**diff 里每个新增的提前退出，都问一句：它之前申请的资源谁来释放**

- **正常路径上的 `close()` 在异常路径上不会执行**：`raise`、`return`、被调用函数抛的异常，都会跳过后面的清理；
- **测试常常只走主路径**：泄漏在失败时才出现，上线后连接池慢慢被耗尽；
- **正确的写法是让语言保证释放**：`with` 语句、`contextlib.closing`、`try/finally`；
- **同类信号**：打开文件、加锁、开事务、起线程却没有对应的 `with`；
- **评审时的问法**：“这里抛异常时，前面打开的东西会怎样？”写不出答案，就要求作者补一条失败路径的测试。

```python
from contextlib import closing, nullcontext
class Conn:
    closed = False
    def close(self): self.closed = True

def load(conn, ok):
    if not ok: raise LookupError("没有数据")    # 提前退出：下面的 close 不会执行
    conn.close()

for safe in (False, True):
    c = Conn()
    try:
        with closing(c) if safe else nullcontext(): load(c, False)
    except LookupError: print("用 closing" if safe else "没有保护", "已关闭 =", c.closed)
# 没有保护 已关闭 = False / 用 closing 已关闭 = True
```

**知识点：**diff 里的高风险信号（Risk Patterns）
