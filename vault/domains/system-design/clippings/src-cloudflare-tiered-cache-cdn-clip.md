---
title: Tiered Cache Smart Topology
source: https://blog.cloudflare.com/tiered-cache-smart-topology/
published: '2021-02-18'
site: Cloudflare Blog
clipped: '2026-09-20'
---

# Tiered Cache Smart Topology

# Tiered Cache Smart Topology

A few years ago, we released [Argo](/argo/) to help make the Internet faster and more efficient. Argo observes network conditions and finds the optimal route across the Internet for origin server requests, avoiding congestion along the way.

Tiered Cache is an Argo feature that reduces the number of data centers responsible for requesting assets from the origin. With Tiered Cache active, a request in South Africa won’t go directly to an origin in North America, but, instead, look in a large, nearby data center to see if the data requested is cached there first. The number and location of the data centers used by Tiered Cache is controlled by a piece of configuration called the topology. By default, we use a generic topology for every customer that strikes a balance between cache hit ratios and latency that is suitable for most users.

Today we’re introducing Smart Topology, which maximizes cache hit ratios by building on Argo’s internal infrastructure to identify the single best data center for making requests to the origin.

## Standard Cache

The standard method for caching assets is to let each data center be a reverse proxy for the origin server. In this scheme, a miss in any data center causes a request to the origin for an asset. A request to the origin for one asset could be made as many times as there are data centers.

A cache miss in any data center will result in a request being sent to the origin server even if the asset is cached in some other data center. This is because the data centers are completely oblivious of each other.

Theoretically, a request for the asset would have to be sent to every data center in order to reduce the cache misses to the minimum possible. However, sending every request to every data center is not practical.

The minimum possible cache hit latency is achieved if the asset is moved into the nearest cache before the request for it is made, but this kind of prediction is generally not possible. Instead, a good heuristic is to move the asset into the nearest cache after the first cache miss.

However, the asset has to be copied from somewhere and it isn’t possible to know where in the network it might be without querying each data center.

To avoid querying each data center, a copy of the asset has to be stored in a known location after the first cache miss so it is available to other data centers. This is precisely what Tiered Cache does.

## Tiered Cache

Tiered Cache improves cache hit ratios by allowing some data centers to serve as caches for others, before the latter has to make a request to the origin. With Tiered Cache, certain data centers are reverse proxies to the origin for other data centers.

If the proxied data centers make requests for the same asset, the asset will already be cached in the proxying data center and can be retrieved from there rather than from the origin. Fewer requests to the origin are made overall.

## Custom Topology

In Tiered Cache, the topology describes which data center should serve as a proxy for others.

For customers, devising an optimal topology is a challenge requiring optimization and continuous maintenance. The best topology is a configuration based on information that is privately held by the customer and other information held only by Cloudflare.

For instance, knowing the desired balance of latency versus cache hit ratio is information only the customer has, but how to best make use of the Internet is something we would know. Enterprise customers usually have dedicated infrastructure teams that work with our solutions engineers to manually optimize and maintain their tiered cache topology.

Not every customer would want to personalize their topology. For this reason a generic topology exists.

## Generic Topology

The generic topology is designed to achieve good latency and cache efficiency for any origin, regardless of location. A balance is struck between two constraints — cache efficiency and latency.

The generic topology has multiple proxying data centers that are distributed around the world in order to ensure that requests that result in a cache miss do not take a very long detour before going to the origin. There is a balance between the number of proxying data centers and the cache hit ratio, because the proxying data centers are oblivious to each other.

If a proxying data center is taken offline, the proxied data centers either use a fallback (if the fallback is online) or revert to behaving like Tiered Cache is disabled.

To achieve the best balance for general usage, the generic topology instructs the smaller data centers to be proxied by the larger data centers in the same geographic region.

## Smart Topology

Smart Topology assumes the origin is in one place and then automatically configures itself to be optimal once the customer just flips a switch in the dashboard. In order to actually do this, Cloudflare needs to be able to determine which data center has the lowest latency to the origin without making the customer tell Cloudflare where the origin is.

### Methods for Latency Determination

There are a few ways to determine which data center has the lowest latency with respect to the origin.

**IP geolocation**Physical distance can be used as an approximation for latency, but Smart Topology was not built this way for a couple of reasons. First, even the best commercial IP geo database doesn’t have the required coverage and accuracy. Second, even with perfect accuracy, physical distance is a questionable approximation of Internet latency.

**Probing**Latency to an IP address can be determined exactly by probing that address. The probe can just be the time required to perform the TCP handshake. Each data center probes the origin so that the latencies can be directly measured and the minimum can be found. Except for edge cases involving Anycast and TCP termination, we can assume that the latency to an IP address is the same as the latency to the origin server behind that IP address.

### Topology Selection Algorithm

The goal of the topology selection algorithm is to minimize cache misses and latency. The topology chooses a single proxying data center in order to maximize the cache hit ratio. The proxying data center is chosen to be close to the origin so that the latencies of cache misses in the proxied data centers are not much worse than they would be with tiered cache turned off.

The choice should eventually become stable. Stability is important because each time the choice changes, cache misses in proxied data centers are likely to cause cache misses in the new proxying data center. Capacity is important because when a data center goes offline, it can cause a large number of cache misses. Minimizing latency to the origin is important to ensure that the network is used efficiently.

The data center selection algorithm is rather like a leaderboard of the fastest data center for each origin. As data is collected, a faster data center can knock others off a given origin’s leaderboard. This competition is based on the 24 hour median latency and is held each hour. Only a subset of data centers deemed large enough are permitted to compete.

Eventually, the choice for proxying data centers becomes stable. Over time, data centers produce competing records for each origin and less competitive records in the leaderboard are replaced as necessary. Thus, latencies for any origin on the leaderboard can only monotonically decrease. There are always physical limits in the real world, so eventually the ideal data center will set a record that is too good to beat.

Also, the leaderboard actually includes both the lowest latency data center and the second lowest latency data center. The second lowest latency data center serves as a fallback if the preferred data center is taken offline for maintenance.

**Anycast Networks**We are measuring the latency to the origin IP address and assuming that it represents the latency to the origin server, but this can break down in certain cases. A few cloud providers other than Cloudflare also use Anycast technology to provide their services. In Anycast, multiple machines can share an IP address regardless of where they are connected to the Internet, and the Internet will typically route packets destined for that address to the closest machine. If an Anycast network is used to proxy an origin server, then the apparent latency to the IP address for the origin server is actually the latency to the edge of the Anycast network rather than the latency to the origin server. The real latency to the origin server cannot be determined by probing.

The algorithm would fail to select the single best proxying data center if the latencies are not representative of the actual latency between data center and origin. Selecting the wrong data center would adversely affect latencies for requests to the origin, and could be expensive.

For instance, imagine a cloud provider provides an IP address that actually routes to multiple data centers all over the world. Packets are routed through private infrastructure to the correct destination once they enter the network. The lowest latency data center to this Anycast IP address could potentially even be on a different continent than the actual origin server. Therefore, the apparent latency cannot actually be trusted as a true measure of actual latency to the origin.

The data center selection algorithm assumes that the origin is in a single geographic location and can be probed to determine latency from each data center. These networks break one or both of these assumptions, so a procedure had to be developed in order to detect them. First, it is assumed that the IP appears in a single geographic location and is not proxied by such a network. The latency to the origin is bounded by the speed of light through fiber. Although the distance between any data center and the origin server is not known, the distances between data centers is known by Cloudflare.

Imagine putting the origin server as a pitstop in that journey. Then, the theoretical minimum possible observable pair of latencies between the origin server and any two data centers can be computed. We have the latency probe data from both of these data centers and the origin, so we can check to see whether the observed latency is lower than what is possible.

The original assumption was that the origin IP address identifies an origin server that is in one location and the latency to that IP address is the latency to the origin server. If the observed latencies are faster than light then clearly the assumption is false. Smart Topology falls back to the generic topology when the original assumption does not hold. To be extra sure, we check this constraint on a bunch of data centers around the world and fall back if there is even a single physically impossible observation.

### The Big Picture

When Smart Topology is enabled many Cloudflare systems work together to ensure the correct data center is eventually used to request assets from the origin.

When the customer enables Tiered Cache Smart Topology, one of a few things can happen from the perspective of the origin. If a proxying data center has already been assigned to the CIDR block that encompasses the origin IP, the preferred or fallback data center is used to request assets from the origin. Otherwise, the generic topology is used to determine which proxying data centers to use to pull assets from the origin. The latency to the proxying data center should only decrease as the choice for proxying data center is updated over time.

## Conclusion

Developing this technology offered a lot of opportunities to exercise great engineering and build an impactful product. It was not done in a vacuum; we used infrastructure that Cloudflare had already built, and we moved along that exponential gradient of using existing progress to make more progress. Building this framework opens a lot of doors to future progress too; for instance, in the future, we can explore ways to select the ideal proxying data center even for origins behind Anycast networks that hide the true latency to the origin.
