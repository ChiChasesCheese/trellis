---
id: amz-file-watcher-how-asked-and-three-questions
node: amazon.amz-file-watcher
type: qa
step: 1
tags: [grown]
---
## Q
文件监听器（File Watcher）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是一个盯着目录的后台工具：目录里有文件被新建、修改、删除时，调用订阅者登记的回调；可以一直跑，也可以停。三问：(1) 靠系统通知还是定期轮询（polling，隔一段时间自己去看一遍）——决定依赖与延迟，推荐轮询并把读文件系统藏在接口后；(2) 递归与否、是否过滤文件——两个参数；(3) 改名与写到一半的文件怎么处理——轮询只能比较前后两次结果，改名表现为一个删除加一个新建，半截文件要去抖（debounce，等写完再通知）。
