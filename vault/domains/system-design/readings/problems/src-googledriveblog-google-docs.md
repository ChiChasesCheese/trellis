---
nodes: [problems.media.google-docs]
url: https://drive.googleblog.com/2010/09/whats-different-about-new-google-docs_22.html
tags: [engineering-blog]
---
# What's different about the new Google Docs: Conflict resolution

值得读：Google Docs 工程师 John Day-Richter 在 2010 年撰写的一手技术博客，三篇系列文章之
一（另两篇是同一博客上的 "Working together, even apart" 和 "Making collaboration fast"）。
这一篇直接给出了操作转换（OT）本身：文档存成一个由插入文字、删除文字、应用样式三种变更组
成的修订日志（revision log），显示文档时从头重放这份日志；并用具体例子说明了转换函数如何
处理"样式区间在文字插入后要跟着扩展""不冲突的变更不需要转换"这类规则。本题解「深入探讨」
第 1 节引用这篇文章作为"Google Docs 使用 OT"这一事实的一手依据，不再转引维基百科或商业备
考网站。
