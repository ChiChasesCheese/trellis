%% trellis:begin %%
# 负数取模规范化（negative-mod-normalization）
*数学与数论（math / number theory）*

在 C++/Java 等语言中，对负数取模可能得到负结果，此时应使用 (x mod m + m) mod m 将结果规范到 [0, m-1]。
%% trellis:end %%

## Notes
