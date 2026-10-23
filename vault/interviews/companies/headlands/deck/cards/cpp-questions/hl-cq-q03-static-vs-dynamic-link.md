---
id: hl-cq-q03-static-vs-dynamic-link
node: cpp-questions.a-why-fast
type: qa
step: 18
---
## Q
追问：静态链接和动态链接有什么区别？
Static vs dynamic linking?

## A
- **静态链接**：把库代码拷进可执行文件。自包含，文件更大，运行时没有查找开销。
- **动态链接**：程序启动时加载共享库。文件更小，库可以单独更新，多一层间接。
