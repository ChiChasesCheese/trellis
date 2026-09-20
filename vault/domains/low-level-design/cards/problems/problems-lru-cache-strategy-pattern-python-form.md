---
id: problems-lru-cache-strategy-pattern-python-form
node: problems.components.lru-cache
type: qa
step: 3
tags: [grown]
---
## Q
LRU/LFU 缓存里“淘汰策略可替换”用的是什么模式？它在这里的 Python 写法和典型的 Java 版策略模式有什么不同？

## A
这是策略模式（Strategy）：把“容量满了该淘汰谁”这个会变化的算法，从 `Cache` 里抽出来，做成一个独立、可替换的对象。Java 版通常会有一个抽象策略接口加多个实现类，调用方在构造时传入策略实例——这里的 Python 写法完全一样（`Cache(capacity, policy=LFUPolicy())`），因为策略本身是有状态的（LRU 要记住顺序，LFU 要记住频率），不能像无状态的单方法策略那样简化成一个普通函数；换成函数会丢失“记住上次调用留下的状态”这个能力，所以这里没有出现“策略模式在 Python 里其实不需要”的简化。
