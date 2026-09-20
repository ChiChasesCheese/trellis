---
nodes: [problems.social.chat-messaging]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp
tags: [no-archive]
---
# WhatsApp | Systems Design Interview Questions With Solutions
值得读：按"需求→容量→API→高层→深入"框架完整走了一遍 WhatsApp 设计，给出具体吞吐量估算（约 4 万消息/秒基线，含群聊放大后约 10 万写/秒）和分级追问（mid/senior/staff 期待的深度不同）。与本题解的分歧：它把消息存储笼统放在 DynamoDB + Redis Pub/Sub，没有深入讨论热分区和时间分桶，本题解补上了这部分论证。
