---
id: problems-flash-sale-lottery-vs-first-come-first-served
node: problems.commerce.flash-sale
type: qa
step: 3
tags: [grown]
---
## Q
When a flash sale's supply-to-demand ratio is extremely lopsided (e.g. 1,000 units against 1,000,000 buyers), why might a short collection-window-then-lottery admission scheme be preferred over pure first-come-first-served rate limiting?

## A
First-come-first-served systematically favors whichever participant has the lowest network latency and the fastest automated submission — a structural advantage that benefits scripted/bot traffic over ordinary users. A lottery instead collects all admission requests submitted within a short fixed window, then randomly selects the winners from that pool after the window closes — removing speed as the deciding factor entirely. The trade-off is a small fixed delay (waiting for the collection window to close) and the fact that a lottery still needs separate defenses against an attacker submitting many entries from many fake accounts, since it protects against a speed advantage, not a volume advantage.

## Q zh
当秒杀的供需比极端悬殊（比如 1,000 件库存对 100 万买家）时，为什么「先收集一个短窗口内的请求、窗口结束后抽签」的准入方案有时会优于纯粹的先到先得限流？

## A zh
先到先得系统性地利好网络延迟最低、自动提交最快的参与者——这对脚本/自动化流量是一种结构性优势，对普通真人用户不利。抽签改为在一个固定的短窗口内收集全部准入请求，窗口结束后再从这个池子里随机选出中签者——彻底去掉了「手速」这个决定因素。代价是要多等一个固定的收集窗口延迟，而且抽签仍然需要单独的手段防御「用大量虚假账号批量占多个抽签名额」这种攻击，因为它防的是速度优势，不是数量优势。
