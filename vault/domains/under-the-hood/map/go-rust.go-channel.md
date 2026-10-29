%% trellis:begin %%
# channel：环形缓冲 + 等待队列
*Go 与 Rust 的运行时和集合*

有缓冲 channel 是一个环形数组加发送、接收两个等待队列，外加一把锁；无缓冲 channel 直接在两个 goroutine 之间交接。

## Cards (3)
1. [[uth-go-rust-go-channel-1-hchan]]
2. [[uth-go-rust-go-channel-2-unbuffered]]
3. [[uth-go-rust-go-channel-3-select]]
%% trellis:end %%

## Notes
