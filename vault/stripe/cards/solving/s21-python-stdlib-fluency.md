---
id: s21-python-stdlib-fluency
node: stripe.solving
type: qa
---

## Q
Stripe OA 60 分钟限时里，为什么工程师公开建议不要用 Java？哪些 Python 标准库必须闭着眼睛写出来？

## A
见 `03-python-cheatsheet.md`。Stripe 的工程师公开建议**不要用 Java**做这个 OA ——
不是因为 Java 不好，是因为 60 分钟里你输不起打字的时间。

必须闭着眼睛写出来的：`defaultdict` / `Counter` / `heapq.heappush,heappop` /
`bisect_left,bisect_right` / `sorted(key=)` / `deque` / `Decimal(...).quantize` /
`datetime.strptime` / `csv.DictReader` / `json.loads` / `functools.cmp_to_key`。
