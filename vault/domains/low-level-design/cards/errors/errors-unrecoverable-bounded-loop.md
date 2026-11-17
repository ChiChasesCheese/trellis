---
id: errors-unrecoverable-bounded-loop
node: errors.unrecoverable
type: qa
step: 3
---
## Q
生成唯一短码的代码是 `while code in taken: code = gen()`。生成器出了问题，一直撞已有的码，会怎样？该怎么改？

## A
**“靠运气”的循环要设上限，用完就明确失败**

- **无上限就是死循环**：线程一直转，请求不返回，服务的线程池很快被占满，没有任何报错；
- **设次数上限**：随机碰撞通常一两次就解决，五次还撞，说明生成器坏了或空间满了；
- **用完以后抛异常**：别返回重复的码或者 `None` 让后面悄悄出错；这不是用户的错，对外是 500；
- **生成器当参数传进来**：测试里换成一个永远撞的假生成器，断言恰好调用了 5 次再失败；
- **同理**：重试、轮询、等待锁，每个循环都要有“最多多久、最多几次”。

```python
def new_code(gen, taken: set, attempts: int = 5) -> str:
    for _ in range(attempts):
        code = gen()
        if code not in taken:
            return code
    raise RuntimeError(f"no free code after {attempts} tries")   # 不是用户的错

calls = []
def stuck(): calls.append(1); return "a"
try: new_code(stuck, {"a"})
except RuntimeError as e: print(e, len(calls))    # no free code after 5 tries 5
```

**知识点：**不可恢复错误与顶层处理（Crash vs Recover）
