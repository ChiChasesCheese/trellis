%% trellis:begin %%
# 幻读与 RR 下怎么解决（Phantom Read）
*B 其余知识点 / MySQL*

幻读在 RR 下靠 MVCC（快照读）加 next-key lock（当前读）解决，但仍有特例。

## Cards (1)
1. [[bagu-phantom-read-1-phantom-rr]]
%% trellis:end %%

## Notes
