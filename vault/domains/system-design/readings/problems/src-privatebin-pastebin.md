---
nodes: [problems.foundations.pastebin]
url: https://privatebin.info/
tags: [reference]
---
# PrivateBin — 项目主页

值得读：一个真实存在、开源的"零知识"粘贴服务，客户端 AES-256-GCM 加密（密钥放在 URL
fragment 里，服务端从不接触明文）和阅后即焚选项，证明"私有内容需要不同于公开内容的处理
方式"不是本题解臆造的顾虑。不同于本题解的地方：PrivateBin 用客户端零知识加密解决私密性，
代价是服务端完全无法读取内容，因而做不了语法高亮渲染或恶意内容/密钥泄露扫描；本题解需要
服务端可见内容才能满足扫描需求，因此改用高熵随机 id（16 位 Base62）加访问控制作为私有
粘贴的防线，这是两者在隐私模型上的主要分歧。

%% trellis:begin %%
## Source
[Open the original ↗](https://privatebin.info/)

## Archived copy
![[src-privatebin-pastebin-clip]]
%% trellis:end %%
