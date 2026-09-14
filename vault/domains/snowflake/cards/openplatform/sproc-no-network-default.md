---
id: sproc-no-network-default
node: openplatform.stored-procedure-sandboxing
type: qa
tags: [grown]
---
## Q
一个 Python 存储过程里调用 `requests.get('https://api.example.com')` 失败了。为什么 Snowflake 默认禁止用户代码访问网络？怎样安全地开放？

## A
用户代码在仓库上的沙箱中运行，与客户数据处于同一环境；默认允许出网就意味着任何能创建过程的人都能把数据发往任意外部地址，形成数据外泄通道。因此出网默认被阻断。需要访问外部 API 时，管理员创建出站（`MODE = EGRESS`）的网络规则列出允许的主机，把它和所需的密钥对象（secret）放进外部访问集成（external access integration），再在函数或过程定义中引用该集成；这样只放行白名单主机，凭证也不以明文写进代码。
