---
nodes: [problems.components.logger, patterns.observer, patterns.structural]
tags: [problem]
---
# Drill：日志框架（Logging Framework）

一个进程内的日志框架：业务代码写一句 `log.info("下单成功", order_id=7)`，框架决定这条记录要不要
记、送到哪几个目的地、写成什么样。级别过滤谁都会写，这道题的分数全在两处——**按名字组成的 logger
树怎么传播**，以及**异步写入的关闭时刻记录到底丢没丢**。照真实机考的节奏分关来做，做完一关再看
下一关。时间一律来自注入的时钟，代码里不许出现 `time.time()`。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：五个级别；一条记录携带时间、级别、正文、产生它的 logger 名字和一组
  结构化上下文，并且**造出来之后不可变**；可以挂多个目的地，每个目的地有**自己的**阈值和
  **自己的**格式化器（至少写文本和 JSON 两种）。被级别关掉的调用必须连记录对象都不构造——
  用一个断言把这件事钉死，而不是嘴上说说。
- 第 2 关（约 12 分钟）：logger 按点分名字成树，`get_logger("a.b.c")` 要把缺失的中间祖先补齐，
  同名两次返回同一个对象。没设级别的 logger 向上继承；记录沿祖先链向上交给沿途每一个 handler。
  这一关必须答准两件事：**向上走时看不看祖先 logger 的级别**，以及怎么在中途截断传播。
- 第 3 关（约 10 分钟）：把任意 handler 包成异步的（一条有界队列加一个工作线程），并写出关闭
  语义。测试要这样写：八个线程各写一百条，队列只留十几个位置，全部生产者结束后关闭，断言
  内层 handler 收到整整八百条、丢弃计数为零。再写一个相反的：故意堵住工作线程，证明丢弃被计数了。
- 第 4 关（选做）：按大小滚动的文件 handler（最旧的备份必须被删掉），以及一个把 `/healthz`
  访问日志扔掉的过滤器。判分点只有一个：加这两样东西，前三关的 `Logger`、`LogRecord`、
  `Formatter` 是不是一行都不用改——handler 那边只该多一个子类和一个「收下一个谓词」的钩子。

**怎么练**：把 `vault/domains/low-level-design/problems/logger/starter.py` 的方法体补全，然后在
仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/logger -q`。

**评分点**
- 阈值分两层，并说得出两层的职责不同：logger 的阈值省开销、handler 的阈值做分流（[[problems-logger-two-level-thresholds]]）。
- 多目的地用列表而不是责任链，并说得出"责任链的终止语义和日志的广播语义相反"（[[problems-logger-chain-vs-handler-list]]）。
- 向上传播时**不再判祖先 logger 的级别**，截断靠 `propagate = False`（[[problems-logger-propagation-ignores-ancestor-level]]）。
- 有效级别沿 `parent` 向上找第一个显式设过的级别，根必须有具体级别；用 `None` 而不是 `NOTSET = 0` 表示继承（[[problems-logger-effective-level-and-notset]]）。
- 格式化器从目的地里拆出来（桥接），`emit` 同时收下行和原始记录，绝不回头解析自己刚生成的字符串（[[problems-logger-formatter-split-from-handler]]、[[patterns-bridge-when]]）。
- 异步 handler 关闭做满"拒收 → 排空 → join → 关内层"四步，且"判断是否已关闭"和"入队"在同一把锁里（[[problems-logger-async-close-contract]]）。
- 队列有界，满了阻塞还是丢弃说得出代价，丢弃一定计数并暴露成公开属性（[[problems-logger-drop-must-be-counted]]）。
- handler 集合存成元组、整体替换，分发热路径不加锁；说得清 GIL 保护不了"读—改—写"（[[problems-logger-handlers-tuple-and-gil]]）。
- 过滤器就是一个 `Callable[[LogRecord], bool]`，不为它写抽象基类（[[problems-logger-filter-is-a-plain-function]]）。
- 记录是冻结的事件对象，handler 拿到它之后不回头读 logger 的状态——这样才不会出现"持锁回调外部代码"的死锁（[[patterns-observer-notify-lock]]、[[patterns-observer-partial-failure]]）。
- `MemoryHandler` 有容量上限、滚动文件有备份数上限：一个日志组件里任何无界增长的容器都是事故。

**题解**：[[solution-logger]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
