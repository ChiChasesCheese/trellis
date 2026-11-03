---
id: craft-ordered-multi-lock-acquisition-4-layer-discipline
node: craft.patterns.ordered-multi-lock-acquisition
type: qa
step: 4
---
## Q
**固定顺序加多把锁 · 服务锁、池锁为什么只能单向**｜模式

叫车系统有服务（DispatchService）一把锁，司机池（DriverPool）一把锁；订座系统有服务锁和每个航班实例一把锁。两个系统的代码里都写明了「服务锁里绝不去拿下层的锁」或「池子从不回调服务」。这条纪律和按 id 排序是什么关系？

## A
**要点。** 同一件事的另一半。按 id 排序处理同层、数量不定的多把锁；分层规则处理不同层之间：规定拿锁的方向只有一个（服务锁 → 池锁），锁序图里没有环，就不会有死锁。池子一旦回调服务，反方向的边就出现了。

```python
# ride-sharing.DriverPool 的约定
# 池子从不回调 DispatchService。锁序因此只有一个方向（服务锁 → 池锁），不存在环。

# airline.AirlineService 的约定
# 它自己的锁只保护目录和订单表，绝不在持有它时去拿某个 FlightInstance 的锁。
# 库存那一侧的多锁顺序由 reserve_across 统一按 key 排序，两层永不交叉。
```

池子在持池锁时回调服务（反方向），与服务正常地先锁自己再锁池：

```
池回调服务: True -> 卡住: True
池回调服务: False -> 卡住: False
```

**不变。** 每把锁都属于某一层，拿锁的方向只有一个。**变化。** 同层多把锁用排序，不同层用方向。

**见于。** digital-wallet、airline、rate-limiter、ride-sharing。

**信号。** 代码里一个持锁的方法调用了回调、监听器，或另一个对象的公开方法；一个操作要同时修改多个对象的状态。
