---
id: nr-amz-s9-senior-1
node: amazon.followups
type: qa
step: 42
---
## Q
<p class="title">Amex 出款延迟事故<span class="meta">03 senior 追问</span></p>

*"How would you communicate with the merchant while the incident was still open?"*

## A
<span class="label">面试官在探</span> 面试官在探：你有没有把客户沟通放在事故处置的前面，而不只是修 bug。

<span class="label">回答框架</span>

- 先给商户一个诚实的状态：是预期延迟还是真问题，现在哪些已确认、哪些还没确认
- 给出下一次更新的时间，而不是等到修好才说话
- 说清楚影响金额和预计到账窗口，不夸大也不回避
- 沟通由事故指挥或客户侧负责人统一出口，我提供技术事实

<span class="label">为什么这是最佳实践</span>

商户盯的是钱什么时候到，所以第一件事是让他知道这是延迟而不是丢失。先把事实边界说清，再约定更新节奏，商户的焦虑才会下降；统一出口则避免多个 owner 给出互相矛盾的说法。我会把自己能核对的部分（SLA、结算时序）提供给负责沟通的人，而不是自己越界对外承诺。

<div class="sources"><b>表达 · business English</b><br>• <b><i>single source of truth</i></b> — 唯一可信的信息源<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d keep one status page as the single source of truth for the merchant.”</span><br>• <b><i>set expectations</i></b> — 管理预期<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The first update should set expectations on when the money lands.”</span></div>
