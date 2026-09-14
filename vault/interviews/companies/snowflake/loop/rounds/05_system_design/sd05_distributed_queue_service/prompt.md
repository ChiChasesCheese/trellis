# Distributed Queue Service（从 deque 类到云端队列服务）

先给你一个简单的类：一个双端队列（deque），支持 `enqueue`、`dequeue`，就是最基本的 FIFO 数据结构，跑在单机内存里。现在我们要把它变成一个真正的云端队列服务，给公司内部各个系统之间做异步解耦用——一个生产者系统把消息放进队列，各种各样的消费者系统从队列里取消息处理。这个服务要处理几件单机 deque 完全不用考虑的事情：第一，消息进了队列之后，就算这台服务器立刻断电，这条消息也不能凭空消失——生产者拿到"入队成功"的确认之后，必须保证这条消息将来一定能被某个消费者拿到；第二，消费者处理消息的时候可能会挂掉、可能会处理很慢、也可能处理到一半崩溃重启，这个时候这条消息不能永远卡在"被取走了但没处理完"的状态，也不能因为消费者重复处理而对业务造成影响，但完全避免重复处理在这种分布式环境下并不现实；第三，不同的消息可能有不同的优先级或者不同的业务重要性，我们希望有一定的公平调度能力，不要让某一类消息的洪峰完全饿死其他类消息；第四，当生产者产生消息的速度持续超过消费者处理消息的速度时，系统不能无限制地堆积消息直到打爆存储或者内存，需要有一个背压机制让生产者知道"现在系统压力大，请放慢一点"。请把这个简单的 deque 类，设计成一个能撑住这些要求的分布式队列服务。

---

**面试环境说明**：这是 Snowflake onsite System Design 轮，时长 45–60 分钟。白板工具未证实；面试官风格两极分化。这道题有一手 onsite 报告明确记录候选人**未通过**这道题——说明这是一道容易在细节上翻车的题，尤其是"故障时 enqueue 是否需要确认落盘再返回"这类问题需要给出坚决、具体的答案，而不是含糊带过。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.6）：
- **一手**："Queue class（类 Python deque）→ 扩展为云端 queue service"，讨论 enqueue/dequeue 在故障下的行为；onsite SD，**候选人未通过** —— t.me/s/usinterview/29299 → 1p3a thread-1185881（**高**，复用 `../../raw/process_research.md` §3.2 #5）。
- **归类页证据**：StaffEngPrep 把 Snowflake SD 报告归到 "Distributed-Systems Scheduling/Queueing/Persistence"（60 min，4 篇独立报告合并——该聚合站单一题族里报告数最多）、"Distributed-Systems Queueing/AI-Tools/Idempotency"（60 min，1 篇）、"Distributed-Systems Ingestion/Queueing/Frontend"（60 min，1 篇）—— staffengprep.com（**中**）。
- 整体置信度 **HIGH**（onsite 一手挂经）。追问汇总（原文已给出）：故障时 enqueue 是否需要确认落盘再返回；at-least-once vs exactly-once 消费；多消费者的公平调度/优先级队列；队列积压时的背压策略。
