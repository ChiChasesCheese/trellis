---
id: patterns-singleton-costs
node: patterns.creational
type: qa
---
## Q
Why is Singleton the most criticized GoF pattern, and what's the modern alternative when you genuinely need one instance?

## A
Singleton couples two decisions that should be separate: *one instance exists* and *everyone accesses it globally*.

- The global access point makes dependencies **invisible** (nothing in a signature says the class uses it) and makes tests share **hidden mutable state** you can't swap or reset.
- It hard-codes the concrete class — no substituting a test double.

Modern alternative: keep the class ordinary, create **one instance at the composition root** and inject it (DI container or hand-wired `main`). Reserve true singletons for stateless, cross-cutting facts (e.g. a process-wide logger), and if forced, use an `enum` singleton / static holder for safe lazy init.

## Q zh
为什么 Singleton 是 GoF 里被批评最多的模式，当你确实只需要一个实例时，现代的替代方案是什么？

## A zh
Singleton 把两个本该分开的决定耦合在了一起：*只存在一个实例*，以及*所有人都通过全局入口访问它*。

- 那个全局访问点让依赖**变得不可见**（签名里没有任何东西表明这个类用了它），也让测试之间共享**隐藏的可变状态**，既换不掉也重置不了。
- 它把具体类写死了 —— 没法替换成测试替身。

现代替代方案：让这个类保持普通，在 **composition root 创建唯一的那个实例**并注入下去（DI 容器，或者手写装配的 `main`）。真正的单例留给无状态的、横切的事实（比如进程级 logger）；如果确实被迫要写，就用 `enum` 单例 / static holder 来获得安全的延迟初始化。
