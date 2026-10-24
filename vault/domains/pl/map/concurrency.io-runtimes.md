%% trellis:begin %%
# 各运行时怎样接入 I/O
*并发与并行*

Go netpoller 把阻塞调用变成调度点、Java NIO 与虚拟线程的挂起、Rust tokio/mio 的 reactor、Python asyncio 的 selector 事件循环；同一套 epoll，四种包装。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/concurrency.io-models|I/O 模型：阻塞、多路复用与完成通知]], [[domains/pl/map/concurrency.green-threads|用户态线程：goroutine 与虚拟线程]]

## Cards (10)
1. [[pl-conc-ioruntimes-principle]]
2. [[pl-conc-ioruntimes-found-go]]
3. [[pl-conc-ioruntimes-found-java]]
4. [[pl-conc-ioruntimes-found-rust]]
5. [[pl-conc-ioruntimes-found-python]]
6. [[pl-conc-ioruntimes-mechanism-files]]
7. [[pl-conc-ioruntimes-table]]
8. [[pl-conc-ioruntimes-unique-java-layers]]
9. [[pl-conc-ioruntimes-best-practice]]
10. [[pl-conc-ioruntimes-pitfall-no-timeout]]
%% trellis:end %%

## Notes
