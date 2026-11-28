---
id: bagu-shell-log-3-reliable-bash
node: a.linux.shell-log
type: qa
step: 3
---
## Q
**Shell 一行流 · 可靠的 bash 脚本**｜追问

面试官：「你写了一个 bash 脚本自动跑测试、收集结果。怎么保证它出错时不会悄悄继续、不会误删文件、临时文件一定被清理？」

## A
**基本回答。** 开头写 `set -euo pipefail`，所有变量加双引号，必填参数用 `${1:?说明}` 检查，临时目录用 `mktemp -d` 创建并用 `trap '...' EXIT` 清理，用退出码表达结果，最后用 `shellcheck` 检查一遍。
`set -u`：拼错的 `$WORKDIIR` 不再被当空串，否则 `rm -rf "$WORKDIIR/"*` 会删当前目录。`pipefail`：管道退出码默认只看最后一个命令，`false | true` 算成功。允许失败要写明：`cmd || true`，或 `if ! grep -q ...; then`。`trap` 在正常结束、出错、Ctrl-C 时都会清理。`shellcheck` 查漏引号、空变量把 `rm -rf $dir/*` 变成 `rm -rf /*` 之类的错。
**举个例子。** 一个统计失败用例数的脚本：
1. **没传参数：** `./ok.sh` 打印 `usage: ok.sh <log>`，退出码 1。
2. **有失败：** `./ok.sh "logs/run 2.log"` 打印 `1 failed`，退出码 1，CI 据此把这一步标红；文件名带空格也没问题，因为变量都加了引号。
3. **没有失败：** grep 没找到时走 `if ! grep -q` 的分支，打印 `no failures`，退出码 0。
4. **无论哪种结束：** `trap` 都会删掉 `mktemp -d` 创建的临时目录。
5. **shellcheck 的提示：** 对 `rm -rf $f/*` 报 SC2115，提醒用 `"${f:?}"/*`，防止 `f` 为空时展开成 `/*`。
**代码。** 脚本骨架：
```bash
#!/usr/bin/env bash
set -euo pipefail
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT          # 任何方式退出都清理
log="${1:?usage: ok.sh <log>}"         # 缺参数：清楚地报错退出
if ! grep -q FAILED "$log"; then       # grep 退出码 1 = 没匹配，这里不是错误
  echo "no failures"; exit 0
fi
grep FAILED "$log" | awk '{print $1}' > "$workdir/failed.txt"
n=$(wc -l < "$workdir/failed.txt")
echo "$n failed"
exit 1
```
**容易错。**
- **以为 `set -e` 处处生效：** 写在 `if`、`while` 条件里，或 `&&`、`||` 左边的命令失败不会触发退出；在函数里被 `if` 调用时同样失效。关键步骤要显式检查。
- **`local x=$(cmd)` 吞掉错误：** `local` 自己总是成功，把 `cmd` 的失败盖住了。先 `local x` 再 `x=$(cmd)`。
- **管道没开 pipefail：** `make | tee build.log` 里 make 失败了，tee 成功，整条命令看起来是成功的。
- **在 macOS 上测、在 Linux 上跑：** macOS 自带的是 bash 3.2，很多行为和 Linux 上的 bash 5 不同，要在目标环境的 bash 里测脚本。
**业务场景。** 对账脚本每天凌晨下载、校验、入库结算文件。没有 `pipefail` 时下载失败、文件为空，后面照样跑完，报告显示「0 笔差异」；加严格模式后下载失败直接让任务失败并告警。
