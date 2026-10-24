---
id: pl-foundations-paradigms-best-practice
node: foundations.paradigms
type: qa
step: 9
---
## Q
多范式语言里，资深工程师怎样决定一段代码用命令式、函数式还是面向对象的写法？每门语言各有什么经验规则？

## A
通用判断标准是：这段代码的核心是「变换数据」还是「管理状态」。

- 数据变换（过滤、映射、聚合）：用函数式管道，输入输出都是值，没有隐藏状态，容易测试，也容易并行。
- 状态管理（状态机、I/O、缓存、资源生命周期）：用命令式加封装。强行用函数式表达会绕远路。
- 对象用来划分责任边界和持有有生命周期的状态，不是用来给数据分类。

各语言的做法：

- Go：不要模仿函数式，写朴素的 `for`。读你代码的人期待这个风格，而且循环能直接设断点。
- Java：`Stream` 里不写副作用；逻辑复杂到需要三层嵌套 lambda 时，换回循环。
- Rust：迭代器链是首选，因为它和手写循环一样快；遇到需要提前退出和多个可变状态的逻辑时用 `for`。
- Python：推导式只写一层；嵌套的推导式比循环难读，就拆开。

违反第一条的代价很具体。Java 并行流里往共享列表 `add`：

```java
List<Integer> bad = new ArrayList<>();
IntStream.range(0, 100_000).parallel().forEach(bad::add);
// bad.size() 三次运行分别约 15523、13841、13885
List<Integer> ok = IntStream.range(0, 100_000).parallel()
    .boxed().collect(Collectors.toList());   // 总是 100000
```

副作用写法丢了约八成元素（偶尔还会抛异常），而 `collect` 由流自己安全地合并。经验规则：管道里每一步都是纯函数，需要结果就让终端操作返回它，不要在中间往外写。
