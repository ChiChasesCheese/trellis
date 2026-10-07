# 快捷键与高频命令（macOS）

> Claude Code 一节对照官方文档 code.claude.com/docs/en/interactive-mode（2026-10-07）。带 ★ 的是面试里最常用、最显手熟的。
> `Alt/Option+字母` 在终端里要先开 "Option as Meta"（iTerm2：Profiles → Keys → Left Option = Esc+；Ghostty：`macos-option-as-alt = true`）。网页版 VS Code 里这个设置不受你控制，就用 `Ctrl` 系的键。

## 0. 网页版 VS Code：会被浏览器抢走的键

| 别按 | 浏览器会做什么 | 改用 |
|---|---|---|
| `Cmd+W` | **关掉整个浏览器标签页** | 关编辑器标签：命令面板输入 "Close Editor"；或鼠标点 × |
| `Cmd+T` / `Cmd+N` | 新开浏览器标签 / 窗口 | 跳符号：`Cmd+Shift+O`；新文件：命令面板 "New File" |
| `Cmd+Q` | 退出浏览器 | — |
| `Cmd+R` | 刷新页面（终端会话可能断） | — |
| `Ctrl+Tab` | 切换浏览器标签 | 切编辑器：`Cmd+P` 输文件名 |

开场先按一次 `Cmd+P`、`` Ctrl+` ``，确认快捷键被 VS Code 接住了。

## 1. Claude Code

| 键 | 作用 |
|---|---|
| ★ `Shift+Tab` | 循环切换权限模式：default → accept edits → **plan** |
| ★ `Esc` | 打断当前回复或工具调用，已做的部分保留，可以接着改方向 |
| ★ `Esc` `Esc` | 输入框有字：清空并存进历史；输入框为空：rewind，回到之前某条消息 |
| ★ `@path` | 引用文件（带自动补全） |
| ★ `!cmd` | shell 模式：跑命令，输出进入上下文，Claude 会接着回应 |
| `/` | 命令：`/clear` `/compact` `/context` `/resume` `/init` `/model`；Abnormal 的 VP of AI Shrivu Shankar 的建议："run /context mid coding session at least once" |
| ★ `\` + `Enter` 或 `Ctrl+J` | 换行（任何终端都能用）；iTerm2 / Ghostty 里也可以 `Shift+Enter` |
| ★ `Ctrl+G` | 在编辑器里写长提示（多行、粘贴代码时用） |
| `Ctrl+R` | 搜索历史提示 |
| `Ctrl+S` | 暂存当前输入；在空输入框再按一次恢复 |
| `Ctrl+O` | 打开或关闭 transcript（看完整的工具调用过程） |
| `Ctrl+B` | 把正在跑的 Bash 命令或 agent 放到后台 |
| `Ctrl+T` | 显示或隐藏 Claude 的任务清单 |
| `Ctrl+L` | 重绘屏幕（显示乱了时用） |
| `Ctrl+C` | 打断；没有在运行时清空输入，连按两次退出 |
| `Ctrl+_` | 撤销输入框里的上一次编辑 |
| `Option+P` | 不清空输入，直接切换模型 |
| `?`（空输入框） | 快捷键帮助 |

提示输入框也支持下面 §2 的行编辑键（`Ctrl+A/E/K/U/W/Y`）。

## 2. 终端行编辑（readline / zsh emacs 模式；终端和 Claude Code 输入框通用）

| 键 | 作用 |
|---|---|
| ★ `Ctrl+A` / `Ctrl+E` | 跳到行首 / 行尾 |
| ★ `Ctrl+W` | 删除光标前一个"词"（到前一个空白） |
| ★ `Ctrl+U` / `Ctrl+K` | 删除到行首 / 删除到行尾 |
| `Ctrl+Y` | 粘贴刚才删掉的内容 |
| `Alt+B` / `Alt+F` | 按词后退 / 前进 |
| `Alt+D` | 删除到词尾 |
| ★ `Ctrl+R` | 反向搜索命令历史（再按一次跳到更早的匹配） |
| `Ctrl+L` | 清屏 |
| `Ctrl+X Ctrl+E` | 在 `$EDITOR` 里编辑当前命令 |
| `Ctrl+Z` → `fg` | 挂起进程，再切回来 |
| `!!` / `!$` / `Alt+.` | 上一条命令 / 上一条命令的最后一个参数 / 逐个插入之前命令的最后参数 |
| `cd -` | 回到上一个目录 |

## 3. VS Code

| 键 | 作用 |
|---|---|
| ★ `Cmd+P` | 按文件名快速打开（`Cmd+P` 后输入 `@` 跳符号，输入 `:` 跳行号） |
| ★ `Cmd+Shift+P` | 命令面板 |
| ★ `Cmd+Shift+F` | 全局搜索 |
| ★ `F12` / `Cmd+点击` | 跳到定义 |
| ★ `Shift+F12` | 查找所有引用 |
| `Ctrl+-` / `Ctrl+Shift+-` | 跳转历史后退 / 前进 |
| ★ `Cmd+Shift+O` | 当前文件里的符号列表 |
| `` Ctrl+` `` / `` Ctrl+Shift+` `` | 显示或隐藏终端 / 新建终端 |
| `Cmd+\` | 拆分编辑器 |
| `Cmd+B` / `Cmd+J` | 显示或隐藏侧边栏 / 面板 |
| `Ctrl+Shift+G` | Source Control（看 diff） |
| `Cmd+D` / `Cmd+Shift+L` | 选中下一个相同词 / 选中全部相同词 |
| `F2` | 重命名符号 |
| `Option+↑/↓` / `Shift+Option+↓` | 移动当前行 / 复制当前行 |
| `Cmd+/` | 切换注释 |
| `Ctrl+G` | 跳到指定行 |
| `Cmd+.` | Quick fix |

## 4. 终端分屏

| 动作 | iTerm2 | Ghostty |
|---|---|---|
| 左右分屏 | `Cmd+D` | `Cmd+D` |
| 上下分屏 | `Cmd+Shift+D` | `Cmd+Shift+D` |
| 切换分屏 | `Cmd+[` / `Cmd+]` | `Cmd+[` / `Cmd+]` |
| 最大化当前分屏 | `Cmd+Shift+Enter` | `Cmd+Shift+Enter` |
| 新标签 | `Cmd+T` | `Cmd+T` |
| 清空回滚缓冲 | `Cmd+K` | `Cmd+K` |
| 查找 | `Cmd+F` | `Cmd+F` |

面试布局：左边 Claude Code，右边跑 `pytest` 和真实入口命令（T11 证据就在右边）。

## 5. 高频命令（右边终端）

```bash
pytest -q                      # 全量
pytest tests/test_x.py -q      # 单文件（T7 每片之后跑）
pytest -x --lf                 # 遇到第一个失败就停；只重跑上次失败的
pytest -k "suppress and not slow" -vv
pytest -s                      # 显示 print；配合 breakpoint() 进 pdb
rg -n "register_" sentinel/    # 找扩展点；rg --files | rg config 找文件
git status -sb && git diff --stat
git diff -- path/              # 只看某个目录的改动
git restore -p path            # 逐块撤掉 AI 的顺手改动（T9）
git stash -u && git stash pop  # 临时收起改动
git add -A && git commit -m "M1: ..."   # 每个里程碑一个提交，方便回滚（HI：commit frequently）
python -m <pkg> --help         # 真实入口
```

用法原则：手熟体现在**不停顿**，不是按键多。每个键在练习时用到自然，面试时就不会去想它。
