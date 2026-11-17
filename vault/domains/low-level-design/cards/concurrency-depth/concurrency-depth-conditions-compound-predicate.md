---
id: concurrency-depth-conditions-compound-predicate
node: concurrency-depth.conditions
type: qa
step: 4
---
## Q
后台工作线程要等到“没有暂停，并且队列里有任务”才干活，随时可能被要求停止。用 `Event`、`queue.Queue` 和 `Condition` 各自能不能写？什么时候该选 `Condition`？

## A
**谓词涉及多个状态，才轮到 `Condition`**

- **`Event` 只有一个布尔**：一次性的“好了”信号，用它最简单；两个标志要同时满足，没法一次等两个 `Event`，只能轮询；
- **`Queue` 只传递元素**：生产者放、消费者取，暂停和停止要靠塞特殊元素，已经排队的任务拦不住；
- **`Condition` 把谓词写成任意表达式**：谓词读几个变量都行，等待和检查在同一把锁里；
- **每个相关字段变化都要通知**：暂停被取消、任务入队、停止，都可能让某个等待者的谓词成立，一律 `notify_all()`；
- **没有这种需求就别用**：一个标志用 `Event`，传元素用 `Queue`，手写 `Condition` 的出错面更大。

```python
import threading
c = threading.Condition()
st = {"paused": True, "jobs": [1], "stop": False}
def next_job():
    with c:
        c.wait_for(lambda: st["stop"] or (not st["paused"] and st["jobs"]))
        return None if st["stop"] else st["jobs"].pop(0)
def update(**kw):
    with c:
        st.update(kw)
        c.notify_all()                # 任何字段变化都可能使某个谓词成立
threading.Timer(0.1, update, kwargs={"paused": False}).start()
print(next_job())                     # 1：暂停取消后才返回
```

<details class="pt"><summary>延伸</summary>

状态字段越多，谓词越难一眼看对。把状态和锁封装进一个类，对外只留 `pause()`、`submit()`、`stop()` 和 `next_job()`，谓词只写在类里面一处。

</details>

**知识点：**条件变量（Condition Variables）
