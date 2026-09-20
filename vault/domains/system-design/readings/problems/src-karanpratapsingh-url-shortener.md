---
nodes: [problems.foundations.url-shortener]
url: https://github.com/karanpratapsingh/system-design#url-shortener
tags: [reference]
---
# URL Shortener

值得读：把"计数器 + Zookeeper 分段区间"这个短码生成方案讲得最完整，包含 Key Generation Service（KGS）双表并发处理和缓存/清理策略的实现细节。比大多数来源更细致的是它给出了具体的 KGS 数据库容量估算（56.8 亿个 6 位 key ≈ 390GB）。本题解在此基础上补充了 KGS 调用频率的定量论证，并把它抽象为一个可短暂离线而不影响重定向的独立服务。
