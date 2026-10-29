%% trellis:begin %%
# Go 调度器与定时器：工作窃取与四叉堆
*Go 与 Rust 的运行时和集合*

G、M、P；每个 P 一个本地运行队列（环形数组）加全局队列，空闲时去别的 P 偷一半；定时器用四叉堆。

## Cards (3)
1. [[uth-go-rust-go-scheduler-1-gmp]]
2. [[uth-go-rust-go-scheduler-2-steal]]
3. [[uth-go-rust-go-scheduler-3-timers]]
%% trellis:end %%

## Notes
