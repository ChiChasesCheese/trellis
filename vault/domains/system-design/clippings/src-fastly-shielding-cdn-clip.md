---
title: 'Let the edge work for you: How shielding improves performance | Fastly'
source: https://www.fastly.com/blog/let-the-edge-work-for-you-how-shielding-improves-performance
author: Travis Sanders
published: '2024-12-06'
site: Fastly
clipped: '2026-09-20'
---

# Let the edge work for you: How shielding improves performance | Fastly

### **What is an origin shield?**

No matter how simple or complex your architecture may be, shielding guarantees optimal performance and availability during your busiest periods.

In the most basic form, the origin shield is a mid-tier caching layer between your origin server(s) and your CDN edge servers (POPs). An origin shield is a protective measure that protects your origin server(s) from overloading and allows you to unlock high availability and performance while realizing cost reduction.

A complete outage is one of the scariest experiences for any company that does digital business. A complete outage may not be a concern for modern, cloud-native architectures. However, your digital presence could still experience a degradation in service during high-traffic events with unpredictable spikes. For this reason, most companies implement some level of a tiered distribution caching strategy to reduce their server requirements and benefit from the performance gains that caching offers. An origin shield will always reduce the load on your origin server(s) and improve your end users' experience.

Correctly implemented, caching provides an added layer of protection and security, while shielding provides a crucial layer of midgress cache protection to ensure these outages don't happen.

### **How does it work?**

An origin shield reduces the number of requests to your origin server by designating an edge node point-of-presence (POP) as the aggregation point for incoming uncached requests. The selected shield POP is an added layer of defense that protects your origin server from thousands or millions of incoming requests. Your origin server can then be locked down from the outside internet, only allowing requests from the shield POP you designate in your configuration. Directing the uncached requests through a shield POP before origin increases your cache hit ratio – enabling you to serve content faster, more efficiently, and without downtime at your origin.

The same applies if you are using multiple CDNs. One of the caching POPs you've configured as a shield can act as the primary CDN within the multi-CDN configuration and will only send a single request to the origin for any content not currently in the cache. This shield shares that response with the other CDNs inside your configuration.

### **What are the benefits?**

On average, customers that use Fastly's shielding technology see upwards of 99% of requests handled at the Fastly edge. Not only does this improve their users' experience by reducing latency, but it also saves high costs by reducing origin scale and egress bandwidth.

Here are some benefits and what Fastly customers are saying about them:

Protection of the origin against traffic overloads, maintaining availability and redundancy. A [__thundering herd__](https://en.wikipedia.org/wiki/Thundering_herd_problem) is when your web property gets so many requests within a set window that your response time degrades, impacting user experience.

“*A leading platform saw a traffic surge of a constant 120,000 requests per second. Fastly’s edge network* __served all but 54 requests__*.”*

Additional coverage during intentional and unintentional DDOS-style attacks; shielding provides a built-in insurance policy against accidental purges and site updates.

*“Origin Shield has been extremely helpful.  Updates are our biggest use of bandwidth, and now we have a* __99% hit ratio__ *for our updates traffic, so that’s saved us a ton on infrastructure costs.”*

Enhanced content delivery and increased cache efficiency; shielding yields a higher cache hit ratio for your content served from the edge.

*“It’s pretty amazing that we have a* __98% hit rate__ *when delivering sports data.”*

Increased security, performance, and resiliency; an extra layer of protection at no cost; reducing the egress footprint translates into a smaller attack surface to your origin servers. This design applies to both single CDN and multi-CDN architectures.

*“Fastly’s shielding feature helps protect our origins from large traffic spikes,* __cutting costs by 60% monthly.__*”*

### **Armor up with Shielding**

Whether you're redesigning your CDN architecture or looking to build a new solution, Origin shielding is a component that deserves serious thought. Focusing on user experience is essential in high-performance use cases where users expect or even guarantee a certain level of service. As the multi-CDN configuration quickly becomes the norm in performance-critical use cases (live video, gaming, etc.), origin shielding goes from a *"nice to have"* to a *"critical"* component within the architectural design pattern. All design components must be performance-ready. Therefore, other CDNs within the multi-CDN configuration must be prepared to absorb traffic for underperforming CDNs immediately.  

For current CDN customers, please get in touch with your account manager to discuss how shielding can benefit your use case. If you're not yet a Fastly customer, [__reach out__](/contact-sales), and we will be happy to show you how our solution can fit into your environment.
