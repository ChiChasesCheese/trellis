---
id: concurrency-depth-gil-guarantee
node: concurrency-depth.memory-model
type: qa
step: 1
---
## Q
GIL 到底保证了什么？为什么 `box.n += 1` 这一行，在 3.11 上压测看不出问题，仍然不是线程安全的？

## A
**GIL 保证单条字节码和单个 C 调用不被打断，不保证几条合起来**

- **保证的**：同一时刻只有一个线程在解释执行字节码；一次属性读、一次 `list.append`、一次 `d[k] = v`（键是内置类型）不会被别的线程打断，也不会读到写了一半的值，容器内部结构不会被弄坏；
- **没保证的**：`box.n += 1` 编译成 `LOAD_ATTR`、`BINARY_OP`、`STORE_ATTR` 三条以上，线程可以在任意两条之间被换走，再换回来时写回的是旧值；
- **为什么测不出**：3.11 主要在 Python 函数入口和循环回跳处响应切换请求，这三条字节码之间碰巧没有。实测（4 线程各加 10000 次，300 轮）默认间隔和 `setswitchinterval(1e-6)` 都是 0/300 轮出错；缺口里放一次 Python 方法调用，1e-6 下 100/100 轮出错。这是实现细节，不是承诺；
- **所以要锁的是“组合”**：检查再执行、读改写、多个字段一起变，GIL 对它们都没有说话；
- **free-threaded 构建（3.13t 起）没有这个巧合**：同样的 `+=` 在 3.14t 默认间隔下 100/100 轮出错。

```python
import dis

class Box:
    n = 0

def inc(box):
    box.n += 1

print([i.opname for i in dis.get_instructions(inc)])
# 3.11：['RESUME', 'LOAD_FAST', 'COPY', 'LOAD_ATTR', 'LOAD_CONST',
#        'BINARY_OP', 'SWAP', 'STORE_ATTR', 'LOAD_CONST', 'RETURN_VALUE']
```

**知识点：**内存模型与可见性（Memory Model）
