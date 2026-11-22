---
id: aie-agent-sandbox-two-isolations
node: t04.agent-sandbox-execution-environment
type: qa
step: 1
tags: [摘要]
---
## Q
**Agent sandbox · 文件隔离和网络隔离为什么缺一不可**｜摘要 · 必会

编码 agent 每执行一条命令都弹窗要人批准，用户很快就一路点「允许」。想让它自由干活又不出事，怎么设计？

## A
**approval fatigue 是问题：** 频繁确认让人不再看内容。更好的办法是划定边界：边界内自动执行，越界才问。

**sandbox 要两层，缺一不可：**

| 只有… | 后果 |
|---|---|
| 网络隔离，没有文件隔离 | 被攻破的 agent 能逃出 sandbox，再上网 |
| 文件隔离，没有网络隔离 | 被攻破的 agent 能把 SSH key 等敏感文件发出去 |

**Claude Code 的做法：**
- 用操作系统的原语（Linux 的 bubblewrap，macOS 的 seatbelt）；
- 文件：当前工作目录可读写，目录外被拦；
- 网络：只能通过 Unix socket 连到沙箱外的代理，代理按域名白名单放行，新域名要用户确认；
- 限制同样作用于它启动的子进程和脚本；
- 内部使用中，权限弹窗减少 84%。

**凭据不进沙箱：** 云端版本里，git 凭据、签名密钥不放在沙箱内；沙箱里的 git 客户端用受限凭据连一个代理，代理校验操作（如只允许推到指定分支）后才加上真实 token 转发。

**检查清单：** 容器或沙箱、网络出口白名单、资源限额（CPU、内存、时间）、凭据不在沙箱里、代码解释器和浏览器各自隔离。

<details class="pt" markdown="1"><summary>出处</summary>

Anthropic《Making Claude Code more secure and autonomous with sandboxing》anthropic.com/engineering/claude-code-sandboxing（2026-11-21 读）；Huyen ch6 §Capability extension（代码解释器）

</details>
