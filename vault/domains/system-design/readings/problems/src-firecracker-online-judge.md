---
nodes: [problems.realtime.online-judge]
url: https://www.usenix.org/system/files/nsdi20-paper-agache.pdf
---
# Firecracker: Lightweight Virtualization for Serverless Applications (NSDI '20)

值得读：AWS 在 NSDI 2020 发表的一手论文（AWS 官方博客
https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/
给出同一组数字的通俗版本），实测 microVM 启动时间 < 125ms、每个 microVM 内存开销
< 5MiB、单机可打包上千个 microVM，是 AWS Lambda 用它隔离每次函数调用的依据。本题解用
这组第一手数字论证"逐提交一个 microVM"在容量估算给出的爆发并发度（约 533 个）下是可行的，
而不是停留在"虚拟机比容器慢"这种笼统印象。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.usenix.org/system/files/nsdi20-paper-agache.pdf)

## Archived copy
![[src-firecracker-online-judge-clip]]
%% trellis:end %%
