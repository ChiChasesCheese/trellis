---
id: craft-per-key-and-sharded-locks-1-lock-per-object
node: craft.patterns.per-key-and-sharded-locks
type: qa
step: 1
---
## Q
**每对象一把锁与分片锁 · 锁应该放在哪个对象上**｜写法

订座系统里每场电影有自己的座位表。最省事的写法是整个服务一把锁。两场不同的电影同时有人买票，会怎样？锁放在 Show 上、放在 Movie 上、放在整个服务上，各自的取舍是什么？

## A
**要点。** 锁的粒度跟着不变量走：不变量覆盖什么，锁就覆盖什么。「同一个座位不能卖两次」的范围是一场电影（Show），所以锁在 Show 上；不同场次的座位完全无关，没有理由互相等。放到整个服务上，互不冲突的操作也被串行化；放到 Movie 上（同一部电影的所有场次）又粗了一层，错在不变量并不跨场次。

```python
class Show:
    def __init__(self, name):
        self.lock = threading.Lock()        # 每场自己的锁

def buy(show, use_global):
    lock = GLOBAL if use_global else show.lock
    with lock:
        time.sleep(0.1)                     # 临界区里的工作量
        show.sold += 1
```

两个不同场次同时买票（每次临界区约 0.1 秒），全局锁与每场一把锁：

```
全局一把锁   两个不同场次同时买票，总耗时 0.32s
每场一把锁   两个不同场次同时买票，总耗时 0.20s
```

耗时受机器影响，量级关系才是要点：全局锁时两个互不相干的购买被串行，每场一把锁时并行。

**易错。** 太细也会出问题：把锁放到每个座位上，一次选三个座位就要拿三把锁，要全有或全无，又得引入加锁顺序（见固定顺序加锁）。

**为什么。** 航班里的锁放在「某一天的某班飞机」（FlightInstance）上，而不是航班号上：只有同一天同一班的旅客才抢同一批座位。
