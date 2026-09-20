---
id: problems-file-sync-optimistic-concurrency-conflict
node: problems.media.file-sync
type: qa
step: 5
tags: [grown]
---
## Q
In a file sync system, how does having each version-submission request carry the parentVersionId it was based on let the server detect a true concurrent edit conflict, and what does the server do instead of silently picking a winner?

## A
The server only accepts a submitted new version as a linear update when the submitted parentVersionId matches the file's current version id; if two devices went offline, each based their edit on the same now-stale parent, and both later submit, the second submission's parentVersionId no longer matches (because the first submission already advanced it), which the server detects as a genuine concurrent conflict rather than a normal sequential update. Instead of using a rule like last-write-wins to silently overwrite one device's changes, the server stores the losing submission as a separate conflicted copy alongside the accepted version, so both sets of changes are preserved and a human or client can resolve the conflict later.

## Q zh
在文件同步系统中，每次版本提交请求携带其所基于的 parentVersionId，是如何让服务器检测到真正的并发编辑冲突的？服务器不会静默选一个赢家，而是怎么做？

## A zh
服务器只在提交的 parentVersionId 与文件当前版本号一致时，才把这次提交当作线性更新接受；如果两台设备断线期间各自基于同一个（此时已过期的）父版本做了修改，之后都提交上来，后到的那个提交的 parentVersionId 就不再匹配（因为第一个提交已经推进了版本号），服务器据此检测出这是一次真正的并发冲突，而不是普通的顺序更新。服务器不会用类似最后写入胜出（last-write-wins）的规则静默覆盖某一方的改动，而是把落败的那次提交存成一个与被接受版本并列的冲突副本，让双方的改动都被保留下来，后续由人工或客户端解决冲突。
