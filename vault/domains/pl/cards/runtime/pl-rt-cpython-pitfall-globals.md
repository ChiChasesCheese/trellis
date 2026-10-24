---
id: pl-rt-cpython-pitfall-globals
node: runtime.cpython-internals
type: qa
step: 8
---
## Q
同一个 Python 循环，写在模块顶层和写在函数里，性能为什么能差一倍？还有哪些“看起来无害”的写法会拖慢解释器？

## A
实验（一次测量，Python 3.14，2000 万次 `s += i`）：
```python
# module level: s and i are globals
s = 0
for i in range(N): s += i
```
```python
# inside a function: s and i are locals
def loop(n):
    s = 0
    for i in range(n): s += i
```
模块顶层约 24.9 纳秒 / 次，函数内约 12.4 纳秒 / 次，慢一倍。

原因：函数内的局部变量保存在栈帧的固定槽位里，字节码是 `LOAD_FAST` / `STORE_FAST`，按下标读写；模块顶层的变量是全局变量，每次访问都是对模块字典的哈希查找（`LOAD_NAME` / `STORE_NAME` 或 `LOAD_GLOBAL`）。字节码对比：函数里 `s += i` 是 `LOAD_FAST_BORROW_LOAD_FAST_BORROW`、`BINARY_OP`、`STORE_FAST`，没有任何字典访问。

类似的“看起来无害”的陷阱：
1. **在热循环里反复访问属性、全局函数**：`for x in xs: result.append(math.sqrt(x))` 每次都查 `result.append` 和 `math.sqrt`。可以提取成局部变量 `append = result.append`。（3.11 起的内联缓存缩小了差距，但没有消除。）
2. **用 `+=` 拼接字符串**：在循环里反复生成新字符串，应该 `''.join(parts)`。
3. **类型不稳定**：同一位置交替传入 `int` 和 `float`、`str`，使特化版本失效，退回通用路径。
4. **把大列表当队列**：`list.pop(0)` 是 O(n)，换 `collections.deque`。
5. **不必要的异常控制流**、过深的函数调用链：每次调用都要建栈帧（3.11 后更便宜，仍比内联慢）。

判断方法：用 `dis.dis(func)` 看字节码，没有 `LOAD_GLOBAL`/字典查找的函数才算“紧”；用 `timeit` 比较改动前后；不要凭直觉。
