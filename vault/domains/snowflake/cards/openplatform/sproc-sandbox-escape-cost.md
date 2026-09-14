---
id: sproc-sandbox-escape-cost
node: openplatform.stored-procedure-sandboxing
type: qa
tags: [grown]
---
## Q
为了让存储过程方便地访问外网，团队建了一个允许所有主机的外部访问集成（external access integration）并广泛授予 USAGE。这样做的风险是什么？

## A
这等于重新打开了沙箱刻意关闭的数据外泄通道：任何能创建或修改使用该集成的函数/过程的人，都能把查询到的数据发送到任意外部地址，而且这类流量绕过了“只允许白名单主机”的审查。正确做法是按用途为每个集成只列出必需的主机、只把 USAGE 授予需要它的角色，并将凭证放入 secret 对象，保持最小权限。
