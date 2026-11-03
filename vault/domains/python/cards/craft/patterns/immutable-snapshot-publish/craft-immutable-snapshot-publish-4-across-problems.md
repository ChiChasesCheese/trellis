---
id: craft-immutable-snapshot-publish-4-across-problems
node: craft.patterns.immutable-snapshot-publish
type: qa
step: 4
---
## Q
**不可变快照整体替换 · 税率、日志处理器、订阅里同一种发布方式**｜模式

税率引擎的版本表、日志的处理器列表、发布订阅的订阅主题，都是读多写少，参考解的写法却一模一样。它们共同的做法是什么？写成本是多少，什么时候不再划算？

## A
**要点。** 数据用不可变容器（元组或冻结对象）保存；改动不就地修改，而是造一个新容器、一步换引用；读者先把引用读到局部变量。

```python
# billing-tax-engine.publish：造新快照换引用
self._schedules[merchant] = _Schedule(old.starts + (effective_from,), old.versions + (ordered,))

# logger.add_handler：整体替换元组，分发路径不加锁
self._handlers = (*self._handlers, handler)

# pub-sub Subscription：订阅的主题元组整体替换，读路径不加锁
self._topics = (*self._topics, topic)
```

每次发布要拷贝整个容器，写是 O(n)，实测元组加一个元素与列表原地 append 对比：

```
n=      100: 整体替换每次       0.4 us，原地 append 每次   0.10 us
n=    10000: 整体替换每次      20.1 us，原地 append 每次   0.40 us
n=  1000000: 整体替换每次    1374.1 us，原地 append 每次   0.40 us
```

处理器、规则版本这类只有几个到几百个元素、很少变化的集合，拷贝几乎免费；数据大或写频繁时，整体替换不再划算，要换成分段拷贝（持久化数据结构）、分片，或回到加锁。

**见于。** billing-tax-engine、logger、ride-sharing（司机记录用 `replace` 整条换）、pub-sub。

**信号。** 一份数据被很多线程频繁读、偶尔写；读路径在热点上，加锁会成为瓶颈；读者需要多个字段彼此一致。
