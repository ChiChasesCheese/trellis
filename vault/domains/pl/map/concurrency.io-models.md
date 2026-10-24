%% trellis:begin %%
# I/O 模型：阻塞、多路复用与完成通知
*并发与并行*

阻塞 I/O、非阻塞 I/O、就绪通知（select/epoll/kqueue）与完成通知（io_uring/IOCP）；C10K 问题；为什么“一个连接一个线程”在高并发下撑不住。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/concurrency.async-await|async/await 与函数着色]]

**Unlocks:** [[domains/pl/map/concurrency.io-runtimes|各运行时怎样接入 I/O]]

## Cards (10)
1. [[pl-conc-iomodels-principle]]
2. [[pl-conc-iomodels-found-nonblocking]]
3. [[pl-conc-iomodels-found-readiness]]
4. [[pl-conc-iomodels-found-completion]]
5. [[pl-conc-iomodels-mechanism-drain]]
6. [[pl-conc-iomodels-table]]
7. [[pl-conc-iomodels-unique-blocking-is-a-model]]
8. [[pl-conc-iomodels-best-practice]]
9. [[pl-conc-iomodels-pitfall-writable-spin]]
10. [[pl-conc-iomodels-evolution]]
%% trellis:end %%

## Notes
