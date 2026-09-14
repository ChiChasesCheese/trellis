---
id: cc-round-submit-final-sweep
node: round.submission
type: cloze
---
The last-five-minutes sweep, in order: {{c1::no debug output on stdout}}; run each part against its worked example and {{c2::diff the bytes}}; run every part on {{c3::empty input}} to prove it exits cleanly instead of crashing; confirm nothing is left half-refactored; and re-read the output spec's sentinel and separator one final time. Four of the five find defects that fail *every* test in a part, which is why the sweep outranks any remaining feature.

## zh
最后五分钟的扫查，按顺序：{{c1::stdout 上没有调试输出}}；用样例跑每一部分并 {{c2::逐字节 diff}}；对每一部分跑一次 {{c3::空输入}}，证明它干净退出而不是崩溃；确认没有留下重构到一半的东西；最后再读一遍输出规格里的 sentinel 和分隔符。五项里有四项能抓出让某一部分**全部**测试失败的缺陷 —— 这就是扫查优先于任何剩余功能的原因。
