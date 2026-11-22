---
id: k8s-command-args-env-exam
node: p3.t01.command-args-env
type: qa
step: 2
tags: [考点]
---
## Q
**命令拼接 · 考点**｜考点 · 必会

镜像里是 `ENTRYPOINT ["node", "app.js"]` 和 `CMD ["--listen-port", "8080"]`。下面三种 manifest，容器最终各执行什么？

1. 不写 `command` 和 `args`
2. 只写 `args: ["--listen-port", "9090"]`
3. 写 `command: ["node", "test.js"]` 和 `args: ["--listen-port", "9090"]`

## A
| manifest | 实际命令 |
|---|---|
| 1. 都不写 | `node app.js --listen-port 8080` |
| 2. 只写 args | `node app.js --listen-port 9090` |
| 3. 都写 | `node test.js --listen-port 9090` |

- **规则：** manifest 里写了的字段替换镜像里对应的；没写的沿用镜像。
- **实战：** 想临时打开 profiling，改 `command` 加 `--cpu-prof --heap-prof`，不用动 Dockerfile 也不用重新构建镜像。
- **常见踩坑：** 想给应用多传一个参数，却只写 `args: ["--debug"]`，结果把镜像默认的 `--listen-port 8080` 也替换掉了，应用换成了默认端口，Service 的 `targetPort` 就对不上。要保留默认参数就把它们一起写进 `args`。

**出处：** KIA2 §8.1.1（图 8.1：三种覆盖方式）
