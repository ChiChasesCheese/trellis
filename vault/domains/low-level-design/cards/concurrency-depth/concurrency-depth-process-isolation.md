---
id: concurrency-depth-process-isolation
node: concurrency-depth.memory-model
type: qa
step: 3
---
## Q
服务用 `multiprocessing` 起了几个 worker，每个 worker 里都有同一个模块级字典做计数，而且加了 `threading.Lock`。为什么总数对不上？GIL 和 `threading.Lock` 在多进程下管什么？

## A
**GIL 和线程锁都只在一个进程里有效，进程之间不共享内存**

- **每个进程各有一份**：子进程启动时拿到模块的一份拷贝（`fork` 复制，`spawn` 重新导入），之后各改各的。实测 2 个子进程各改一次 `counts["n"] += 1`，父进程里 `counts` 仍是 `{'n': 0}`；
- **各有自己的 GIL**：这也是多进程能并行跑纯 Python 计算的原因；
- **`threading.Lock` 没用**：别的进程看不见这把锁；每个实例里的限流器各放行 `limit` 个，总放行数是进程数乘以 `limit`；
- **要共享状态，换成跨进程的东西**：`multiprocessing.Value`（自带锁）、`Manager`，或者更常见的，放到外部存储：数据库带条件的更新、Redis 里的原子脚本；
- **在面试里的表述**：进程内用锁，跨进程跨机器用数据库的约束和条件更新。

```python
import multiprocessing as mp

counts = {"n": 0}

def bump(_):
    counts["n"] += 1

if __name__ == "__main__":
    with mp.Pool(2) as pool:
        pool.map(bump, range(4))            # 子进程里各改各的 counts
    print(counts)                           # {'n': 0}：父进程的没变
```

**知识点：**内存模型与可见性（Memory Model）
