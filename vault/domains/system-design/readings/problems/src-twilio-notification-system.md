---
nodes: [problems.social.notification-system]
url: https://support.twilio.com/hc/en-us/articles/115002943027-Understanding-Twilio-Rate-Limits-and-Message-Queues
---
# Understanding Twilio Rate Limits and Message Queues

值得读：Twilio 官方支持文档，给出短信限速的确切数字——长号码每秒 1 条消息（1 MPS）、
短代码每秒 100 条（100 MPS）、以及消息在队列中最长保留 10 小时后放弃。比其他二手资料
更精确的地方在于给出了具体的队列容量例子（短代码 500 MPS 账号级配置下队列容量
1800 万条消息段）。本题解「深入探讨」第 3 节的幂等去重窗口（11 小时）直接由这里的
10 小时队列保留时长推出。

%% trellis:begin %%
## Source
[Open the original ↗](https://support.twilio.com/hc/en-us/articles/115002943027-Understanding-Twilio-Rate-Limits-and-Message-Queues)

## Archived copy
![[src-twilio-notification-system-clip]]
%% trellis:end %%
