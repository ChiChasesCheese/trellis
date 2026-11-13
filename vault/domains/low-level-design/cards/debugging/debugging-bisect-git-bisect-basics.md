---
id: debugging-bisect-git-bisect-basics
node: debugging.bisect
type: qa
step: 1
---
## Q
上周五的版本是好的，今天主干上的版本坏了，中间有 1,000 个提交。`git bisect` 怎么用？最多要测几次？它成立的前提是什么？

## A
**二分查找提交历史：告诉 git 一个好的提交和一个坏的提交，它每次检出中间那个让你测，你回答好或坏，范围就减半。1,000 个提交最多约 10 次（2^10 = 1024）。**

```bash
git bisect start
git bisect bad HEAD                 # 当前是坏的
git bisect good v2.3.0              # 这个标签是好的
# git 检出中间的提交，你构建、测试，然后回答：
git bisect good                     # 或 git bisect bad
git bisect skip                     # 这个提交编译不过、没法判断
# ... 重复，直到 git 打印 "<sha> is the first 'bad' commit"
git bisect log > bisect.log         # 记录过程，可用 git bisect replay 重放
git bisect reset                    # 回到开始前的分支
```

- **前提一：好坏是单调的。** 在好提交之后某一刻变坏，之后一直坏。如果 bug 出现、消失、又出现，二分会给出一个误导性的答案。
- **前提二：每一步的判断可靠。** 一次答错就会把你带进错误的那一半，后面再怎么测都找不回来。偶发失败的测试必须在每一步重复多次再下结论。
- **前提三：每个提交都能构建和测试。** 编译不过的提交用 `git bisect skip` 跳过；跳过太多，最后只能给出一个「在这几个提交之间」的范围。
- **不只用于 bug：** 性能变慢、输出变了也能二分。用 `git bisect start --term-old=fast --term-new=slow`，回答 `git bisect fast` / `slow`，比硬套 good/bad 不容易答反。
- **合并多的历史：** `git bisect start --first-parent` 只沿主干的合并提交走，先找出是哪次合并引入的，再进那个分支里细分。
