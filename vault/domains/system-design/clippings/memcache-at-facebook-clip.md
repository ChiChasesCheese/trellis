---
title: Scaling Memcache at Facebook
source: https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala
author: Rajesh Nishtala; Hans Fugal; Steven Grimm; Marc Kwiatkowski; Herman Lee; Harry
  C Li; Ryan McElroy; Mike Paleczny; Daniel Peek; Paul Saab; David Stafford; Tony
  Tung; Venkateshwaran Venkataramani
published: '2024-11-01'
site: usenix.org
clipped: '2026-08-15'
---

# Scaling Memcache at Facebook

## sponsors

# Scaling Memcache at Facebook

Rajesh Nishtala, Hans Fugal, Steven Grimm, Marc Kwiatkowski, Herman Lee, Harry C. Li, Ryan McElroy, Mike Paleczny, Daniel Peek, Paul Saab, David Stafford, Tony Tung, and Venkateshwaran Venkataramani, *Facebook Inc.*

Memcached is a well known, simple, in memory caching solution. This paper describes how Facebook leverages memcached as a building block to construct and scale a distributed key-value store that supports the world’s largest social network. Our system handles billions of requests per second and holds trillions of items to deliver a rich experience for over a billion users around the world.

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

author = {Rajesh Nishtala and Hans Fugal and Steven Grimm and Marc Kwiatkowski and Herman Lee and Harry C. Li and Ryan McElroy and Mike Paleczny and Daniel Peek and Paul Saab and David Stafford and Tony Tung and Venkateshwaran Venkataramani},

title = {Scaling Memcache at Facebook},

booktitle = {10th USENIX Symposium on Networked Systems Design and Implementation (NSDI 13)},

year = {2013},

isbn = {978-1-931971-00-3},

address = {Lombard, IL},

pages = {385--398},

url = {https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala},

publisher = {USENIX Association},

month = apr

}

## Presentation Video 
  
      

#### Presentation Audio

*by Michael Piatek*

Responsiveness is essential for web services. Speed drives user engagement, which drives revenue. To reduce response latency, modern web services are architected to serve as much as possible from in-memory caches. The structure is familiar: a database is split among servers with caches for scaling reads.

This is a common evolution path with common pitfalls. Consistency, failure handling, replication, and load balancing are all complicated by relying on soft-state caches as the de-facto storage system. This paper describes how Facebook has engineered their caching layer, based on memcached, to cope with these issues.

The techniques described provide a valuable roadmap for scaling the typical sharded SQL stack: improvements to the software implementation, coordination between the caching layer and the database to manage consistency and replication, as well as failover handling tuned to the operational needs of a billion-user system. Most of these techniques are reusable, making this a must-read paper for anyone building large-scale web services today.

While the ensemble of techniques described by the authors has proven remarkably scalable, the semantics of the system as a whole are difficult to state precisely. Memcached may lose or evict data without notice. Replication and cache invalidation are not transactional, providing no consistency guarantees. Isolation is limited and failurehandling is workload dependent. Won't such an imprecise system be incomprehensible to developers and impossible to operate?

For those who believe that strong semantics are essential for building large-scale services, this paper provides a compelling counter-example. In practice, performance, availability, and simplicity often outweigh the benefits of precise semantics, at leastfor one very large-scale web service.
