---
title: How we built rate limiting capable of scaling to millions of domains
source: https://blog.cloudflare.com/counting-things-a-lot-of-different-things/
published: '2017-06-07'
site: Cloudflare Blog
clipped: '2026-09-20'
---

# How we built rate limiting capable of scaling to millions of domains

# How we built rate limiting capable of scaling to millions of domains

Back in April we announced [Rate Limiting](/rate-limiting/) of requests for every Cloudflare customer. Being able to rate limit at the edge of the network has many advantages: it’s easier for customers to set up and operate, their origin servers are not bothered by excessive traffic or layer 7 attacks, the performance and memory cost of rate limiting is offloaded to the edge, and more.

In a nutshell, [rate limiting](https://www.cloudflare.com/learning/bots/what-is-rate-limiting/) works like this:

- Customers can define one or more rate limit rules that match particular HTTP requests (failed login attempts, expensive API calls, etc.)
- Every request that matches the rule is counted per client IP address
- Once that counter exceeds a threshold, further requests are not allowed to reach the origin server and an error page is returned to the client instead

This is a simple yet effective protection against brute force attacks on login pages and other sorts of abusive traffic like [L7 DoS attacks](https://www.cloudflare.com/learning/ddos/application-layer-ddos-attack/).

Doing this with possibly millions of domains and even more millions of rules immediately becomes a bit more complicated. This article is a look at how we implemented a rate limiter able to run quickly and accurately at the edge of the network which is able to cope with the colossal volume of traffic we see at Cloudflare.

### Let’s just do this locally!

As the Cloudflare edge servers are running NGINX, let’s first see how the stock [rate limiting](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html) module works:

```
http {
    limit_req_zone $binary_remote_addr zone=ratelimitzone:10m rate=15r/m;
    ...
    server {
        ...
        location /api/expensive_endpoint {
            limit_req zone=ratelimitzone;
        }
    }
}
```
This module works great: it is reasonably simple to use (but requires a config reload for each change), and very efficient. The only problem is that if the incoming requests are spread across a large number of servers, this doesn’t work any more. The obvious alternative is to use some kind of centralized data store. Thanks to NGINX’s Lua scripting module, that we already use extensively, we could easily implement similar logic using any kind of central data backend.

But then another problem arises: how to make this fast and efficient?

### All roads lead to Rome? Not with anycast!

Since Cloudflare has a vast and diverse network, reporting all counters to a single central point is not a realistic solution as the latency is far too high and guaranteeing the availability of the central service causes more challenges.

First let’s take a look at how the traffic is routed in the Cloudflare network. All the traffic going to our edge servers is [anycast](https://en.wikipedia.org/wiki/Anycast) traffic. This means that we announce the same IP address for a given web application, site or API worldwide, and traffic will be automatically and consistently routed to the closest live data center.

This property is extremely valuable: we are sure that, under normal conditions[\[1\]](#fn1), the traffic from a single IP address will always reach the same PoP. Unfortunately each new TCP connection might hit a different server inside that PoP. But we can still narrow down our problem: we can actually create an isolated counting system inside each PoP. This mostly solves the latency problem and greatly improves the availability as well.

### Storing counters

At Cloudflare, each server in our edge network is as independent as possible to make their administration simple. Unfortunately for rate limiting, we saw that we do need to share data across many different servers.

We actually had a similar problem in the past with [SSL session IDs](https://en.wikipedia.org/wiki/Transport_Layer_Security#Session_IDs): each server needed to fetch TLS connection data about past connections. To solve that problem we created a [Twemproxy](https://github.com/twitter/twemproxy) cluster inside each of our PoPs: this allows us to split a memcache[\[2\]](#fn2) database across many servers. A [consistent hashing](https://en.wikipedia.org/wiki/Consistent_hashing) algorithm ensures that when the cluster is resized, only a few number of keys are hashed differently.

In our architecture, each server hosts a shard of the database. As we already had experience with this system, we wanted to leverage it for the rate limit as well.

### Algorithms

Now let’s take a deeper look at how the different rate limit algorithms work. What we call the *sampling period* in the next paragraph is the reference unit of time for the counter (1 second for a 10 req/sec rule, 1 minute for a 600 req/min rule, ...).

The most naive implementation is to simply increment a counter that we reset at the start of each sampling period. This works but is not terribly accurate as the counter will be arbitrarily reset at regular intervals, allowing regular traffic spikes to go through the rate limiter. This can be a problem for resource intensive endpoints.

Another solution is to store the timestamp of every request and count how many were received during the last sampling period. This is more accurate, but has huge processing and memory requirements as checking the state of the counter require reading and processing a lot of data, especially if you want to rate limit over long period of time (for instance 5,000 req per hour).

The [leaky bucket](https://en.wikipedia.org/wiki/Leaky_bucket) algorithm allows a great level of accuracy while being nicer on resources (this is what the stock NGINX module is using). Conceptually, it works by incrementing a counter when each request comes in. That same counter is also decremented over time based on the allowed rate of requests until it reaches zero. The capacity of the bucket is what you are ready to accept as “burst” traffic (important given that legitimate traffic is not always perfectly regular). If the bucket is full despite its decay, further requests are mitigated.

However, in our case, this approach has two drawbacks:

- It has two parameters (average rate and burst) that are not always easy to tune properly
- We were constrained to use the memcached protocol and this algorithm requires multiple distinct operations that we cannot do atomically[\[3\]](#fn3)

So the situation was that the only operations available were `GET`, `SET` and `INCR` (atomic increment).

### Sliding windows to the rescue

[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) [image](https://www.flickr.com/photos/halfrain/14247536929/) by [halfrain](https://www.flickr.com/photos/halfrain/)

The naive fixed window algorithm is actually not that bad: we just have to solve the problem of completely resetting the counter for each sampling period. But actually, can’t we just use the information from the previous counter in order to extrapolate an accurate approximation of the request rate?

Let’s say I set a limit of 50 requests per minute on an API endpoint. The counter can be thought of like this:

In this situation, I did 18 requests during the current minute, which started 15 seconds ago, and 42 requests during the entire previous minute. Based on this information, the rate approximation is calculated like this:

```
rate = 42 * ((60-15)/60) + 18
     = 42 * 0.75 + 18
     = 49.5 requests
```
One more request during the next second and the rate limiter will start being very angry!

This algorithm assumes a constant rate of requests during the previous sampling period (which can be any time span), this is why the result is only an approximation of the actual rate. This algorithm can be improved, but in practice it proved to be good enough:

- It smoothes the traffic spike issue that the fixed window method has
- It very easy to understand and configure: no average vs. burst traffic, longer sampling periods can be used to achieve the same effect
- It is still very accurate, as an analysis on 400 million requests from 270,000 distinct sources shown:
  - 0.003% of requests have been wrongly allowed or rate limited
  - An average difference of 6% between real rate and the approximate rate
  - 3 sources have been allowed despite generating traffic slightly above the threshold (false negatives), the actual rate was less than 15% above the threshold rate
  - None of the mitigated sources was below the threshold (false positives)

Moreover, it offers interesting properties in our case:

- Tiny memory usage: only two numbers per counter
- Incrementing a counter can be done by sending a single `INCR` command
- Calculating the rate is reasonably easy: one GET command[\[4\]](#fn4) and some very simple, fast math

So here we are: we can finally implement a good counting system using only a few memcache primitives and without much contention. Still we were not happy with that: it requires a memcached query to get the rate. At Cloudflare we’ve seen a few of the largest L7 attacks ever. We knew that large scale attacks would have crushed the memcached cluster like this. More importantly, such operations would slow down legitimate requests a little, even under normal conditions. This is not acceptable.

This is why the increment jobs are run asynchronously without slowing down the requests. If the request rate is above the threshold, another piece of data is stored asking all servers in the PoP to start applying the mitigation for that client. Only this bit of information is checked during request processing.

Even more interesting: once a mitigation has started, we know exactly when it will end. This means that we can cache that information in the server memory itself. Once a server starts to mitigate a client, it will not even run another query for the subsequent requests it might see from that source!

This last tweak allowed us to efficiently mitigate large L7 attacks without noticeably penalizing legitimate requests.

### Conclusion

Despite being a young product, the rate limiter is already being used by many customers to control the rate of requests that their origin servers receive. The rate limiter already handles several billion requests per day and we recently mitigated attacks with as many as 400,000 requests per second to a single domain without degrading service for legitimate users.

We just started to explore how we can efficiently protect our customers with this new tool. We are looking into more advanced optimizations and create new features on the top of the existing work.

Interested in working on high-performance code running on thousands of servers at the edge of the network? Consider [applying](https://www.cloudflare.com/careers/) to one of our open positions!

1. The inner workings of anycast route changes are outside of the scope of this article, but we can assume that they are rare enough in this case. [↩︎](#fnref1)
2. Twemproxy also supports Redis, but our existing infrastructure was backed by [Twemcache](https://github.com/twitter/twemcache) (a Memcached fork)[↩︎](#fnref2)
3. Memcache does support [CAS](https://github.com/memcached/memcached/wiki/Commands#cas) (Compare-And-Set) operations and so optimistic transactions are possible, but it is hard to use in our case: during attacks, we will have a lot of requests, creating a lot of contention, in turn resulting in a lot of CAS transactions failing.[↩︎](#fnref3)
4. The counters for the previous and current minute can be retrieved with a single GET command [↩︎](#fnref4)
