---
id: venv-isolation-not-in-git
node: engineering.packaging-env
type: qa
source: python-docs
---
## Q
虚拟环境（virtual environment）目录（如 `.venv`）为什么默认应该被隔离且不纳入版本控制（如不加进 Git）？

## A
虚拟环境建立在某个已安装的「基础」（base）Python 之上，默认只让显式安装到这个环境里的包可用，与基础环境及其他虚拟环境相互隔离，这样不同项目的依赖版本不会互相冲突。它应被当作一次性、可随时删除重建的产物：目录里混有绝对路径、平台相关的解释器拷贝或符号链接，不具备可移植性，纳入版本控制既没有意义也会带来体积和平台不兼容问题；真正该提交的是能重新生成它的依赖清单（如 `requirements.txt`）。
