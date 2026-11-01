---
id: hi-x-blob-metadata-split-3-choose
node: sd.cross.blob-metadata-split
type: qa
step: 3
---
## Q
**字节与元数据分离**｜跨题模式 · 怎么选

遇到「有大对象或大历史」的新设计题，怎样决定字节、元数据和派生数据各放哪里，需要多重的机制？列出判断信号，每个分支给一个例子。

## A
| 信号 | 选择 | 例子 |
|---|---|---|
| 字节很大，多设备要保持一致 | 切块加指纹去重，元数据提交带 baseVersion，游标追变更日志，冲突保留两份 | [[file-sync-system\|设计云盘与文件同步系统（Dropbox / Google Drive）]] |
| 字节很大，主要是浏览和分享 | 直传加 CDN，多档缩略图，键集游标分页，分析走 CDC | [[photo-storage-sharing\|照片存储与分享系统（Google Photos）]] |
| 数据到期就该消失 | 选择支持 TTL 或时间窗口整体丢弃的存储，读取时再核对到期时间，入口前置拒绝 | [[disposable-email\|设计临时邮箱服务（类似 tempmail.org）]] |
| 主体是小文本，偶有大附件 | 正文一份加指针，附件只存引用，历史分层 | [[messenger-chat-system\|设计聊天/即时通讯系统（WhatsApp / Messenger）]] |
| 数据量小，限制来自外部窗口 | 存储用普通库，把工作放在拼装和压缩上 | [[chatbot-design\|对话式 AI 聊天服务（简化版 ChatGPT）]] |

再看三个旁支信号：要不要去重（内容寻址，注意跨用户去重的隐私风险和与端到端加密的冲突）；删除是否可恢复（软删加回收站，字节引用计数归零后延迟删）；有没有分析查询（CDC 流入数仓，不跑线上库）。
