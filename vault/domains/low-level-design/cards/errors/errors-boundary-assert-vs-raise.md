---
id: errors-boundary-assert-vs-raise
node: errors.boundary-validation
type: qa
step: 6
---
## Q
校验调用方传来的参数应该用 `assert` 还是 `raise`？内部不变量呢？

## A
**输入用 `raise`，内部不变量用 `assert`**

- **`python -O` 会删掉所有 `assert`**：用它校验输入，优化模式下整个校验消失，非法数据直接进系统；
- **输入出错是预期的失败**：调用方的错，需要稳定的异常类型和消息，上层能捕获并映射成 400；
- **`assert` 表示“这里不可能发生”**：触发就是我们自己的 bug，让它崩出来；
- **后果严重的不变量也用 `raise`**：计数超过上限、余额为负这类会伤数据的状态，抛 `RuntimeError`，不依赖 `-O`。

```python
def set_age(age):
    if type(age) is not int or age < 0:
        raise ValueError("age")           # 外部输入：raise
    return age

def top(stack: list):
    assert stack, "callers guarantee a non-empty stack"   # 内部契约：assert
    return stack[-1]

print(set_age(30), top([1, 2]))
```

<details class="pt"><summary>延伸</summary>

被测试覆盖的 `assert` 在开发时是最便宜的文档；生产里要不要保留，取决于“触发后继续运行”和“崩溃”哪个代价更低。涉及钱和权限的，选前者之外的另一条路：显式 `raise`。

</details>

**知识点：**边界校验（Validate at the Boundary）
