---
id: problems-web-crawler-crawl-delay-not-standardized
node: problems.search.web-crawler
type: qa
step: 5
tags: [grown]
---
## Q
Why shouldn't a polite web crawler treat a site's declared `Crawl-delay` value in robots.txt as its sole or authoritative throttling signal, even though it fully honors the `Disallow`/`Allow` directives in the same file?

## A
RFC 9309, the IETF standard that formalized robots.txt in 2022, standardized `Disallow`/`Allow` but explicitly left `Crawl-delay` out of the standard because there was no consistent real-world behavior to codify — in practice, major crawlers disagree on whether to honor it at all. A crawler that treats an unstandardized, inconsistently-supported field as its primary throttle is relying on something with no guaranteed meaning; a more robust design honors the mandatory disallow rules strictly but derives its actual request rate from its own adaptive signal, such as observed response latency and error rate with exponential backoff, treating any declared crawl-delay only as a lower-bound hint.

## Q zh
为什么一个礼貌的网络爬虫不应该把站点在 robots.txt 里声明的 `Crawl-delay` 值当作唯一或权威的节流信号，即使它完全遵守同一文件里的 `Disallow`/`Allow` 指令？

## A zh
把 robots.txt 正式标准化的 IETF 标准 RFC 9309（2022 年）标准化了 `Disallow`/`Allow`，但明确没有把 `Crawl-delay` 纳入标准，理由是这个字段在真实世界里没有一致的行为可以规范——现实中主流爬虫对是否遵守它的做法并不一致。把一个未被标准化、支持程度不一致的字段当作主要节流依据，等于依赖一个没有确定含义保证的东西；更稳健的做法是严格遵守强制性的 disallow 规则，但用自己的自适应信号（例如观测到的响应延迟和错误率，配合指数退避）来决定实际请求速率，把站点声明的 crawl-delay（如果有）只当作一个下限参考。
