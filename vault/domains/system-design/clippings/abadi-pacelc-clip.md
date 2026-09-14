---
title: Problems with CAP, and Yahoo’s little known NoSQL system
source: https://dbmsmusings.blogspot.com/2010/04/problems-with-cap-and-yahoos-little.html
author: Daniel Abadi
published: '2010-04-23'
site: dbmsmusings.blogspot.com
clipped: '2026-08-15'
---

# Problems with CAP, and Yahoo’s little known NoSQL system

Over the past few weeks, in my advanced database system implementation class I teach at Yale, I’ve been covering the CAP theorem, its implications, and various scalable NoSQL systems that would appear to be influenced in their design by the constraints of CAP. Over the course of my coverage of this topic, I am convinced that CAP falls far short of giving a complete picture of the engineering tradeoffs behind building scalable, distributed systems.

**My problems with CAP**

CAP is generally described as the following: when you build a distributed system, of three desirable properties you want in your system: consistency, availability, and tolerance of network partitions, you can only choose two.

Already there is a problem, since this implies that there are three types of distributed systems one can build: CA (consistent and available, but not tolerant of partitions), CP (consistent and tolerant of network partitions, but not available), and AP (available and tolerant of network partitions, but not consistent).  The definition of CP looks a little strange --- “consistent and tolerant of network partitions, but not available” --- the way that this is written makes it look like such as system is never available --- a clearly useless system. Of course, this is not really the case; rather, availability is only sacrificed when there is a network partition. In practice, this means that the roles of the A and C in CAP are asymmetric. Systems that sacrifice consistency (AP systems) tend to do so **all the time**, not just when there is a network partition (the reason for this will become clear by the end of this post). The potential confusion caused by the asymmetry of A and C is my first problem.

My second problem is that, as far as I can tell, there is no practical difference between CA systems and CP systems. As noted above, CP systems give up availability only when there is a network partition. CA systems are “[not tolerant of network partitions](http://cacm.acm.org/blogs/blog-cacm/83396-errors-in-database-systems-eventual-consistency-and-the-cap-theorem/fulltext)”. But what if there is a network partition? What does “not tolerant” mean? In practice, it means that they lose availability if there is a partition. Hence CP and CA are essentially  identical. So in reality, there are only two types of systems: CP/CA and AP. I.e., if there is a partition, does the system give up availability or consistency? Having three letters in CAP and saying you can pick any two does nothing but confuse this point.

But my main problem with CAP is that it focuses everyone on a consistency/availability tradeoff, resulting in a perception that the reason why NoSQL systems give up consistency is to get availability. But this is far from the case. A good example of this is Yahoo’s little known NoSQL system called PNUTS (in the academic community) or Sherpa (to everyone else).

 (Note, readers from the academic community might wonder why I’m calling PNUTS “little known”. It turns out, however, that outside the academic community, PNUTS/Sherpa is almost never mentioned in the NoSQL discussion --- in fact, as of April 2010, it’s not even categorized in the list of 35+ NoSQL systems at the [nosql-database.org](http://nosql-database.org/) Website).

**PNUTS and CAP**

If you examine PNUTS through the lens of CAP, it would seem that the designers have no idea what they are doing (I assure you this is not the case). Rather than giving up just one of consistency or availability, the system gives up both! It relaxes consistency by only guaranteeing “timeline consistency” where replicas may not be consistent with each other but updates are guaranteed to be applied in the same order at all replicas. However, they also give up availability --- if the master replica for a particular data item is unreachable, that item becomes unavailable for updates (note, there are other configurations of the system with availability guarantees similar to Dynamo/Cassandra, I’m focusing in this post on the default system described in the original PNUTS paper). Why would anyone want to give up both consistency and availability? CAP says you only have to give up just one!

The reason is that CAP is missing a very important letter: L. PNUTS gives up consistency not for the goal of improving availability. Instead, it is to lower latency. Keeping replicas consistent over a wide area network requires at least one message to be sent over the WAN in the critical path to perform the write (some think that 2PC is necessary, but my student Alex Thomson has some research showing that this is not the case --- more on this in a future post). Unfortunately, a message over a WAN significantly increases the latency of a transaction (on the order of hundreds of milliseconds), a cost too large for many Web applications that businesses like Amazon and Yahoo need to implement. Consequently, in order to reduce latency, replication must be performed asynchronously. This reduces consistency ([by definition](http://portal.acm.org/citation.cfm?id=564585.564601)). In Yahoo’s case, their method of reducing consistency (timeline consistency) enables an application developer to rely on some guarantees when reasoning about how this consistency is reduced. But consistency is nonetheless reduced.

**Conclusion: Replace CAP with PACELC**

In thinking about CAP the past few weeks, I feel that it has become overrated as a tool for explaining the design of modern scalable, distributed systems. Not only is the asymmetry of the contributions of C, A, and P confusing, but the lack of latency considerations in CAP significantly reduces its utility.

To me, CAP should really be PACELC --- if there is a partition (P) how does the system tradeoff between availability and consistency (A and C); else (E) when the system is running as normal in the absence of partitions, how does the system tradeoff between latency (L) and consistency (C)?

Systems that tend to give up consistency for availability when there is a partition also tend to give up consistency for latency when there is no partition. This is the source of the asymmetry of the C and A in CAP. However, this confusion is not present in PACELC.

For example, Amazon’s Dynamo (and related systems like Cassandra and SimpleDB) are PA/EL in PACELC --- upon a partition, they give up consistency for availability; and under normal operation they give up consistency for lower latency. Giving up C in both parts of PACELC makes the design simpler --- once the application is configured to be able to handle inconsistencies, it makes sense to give up consistency for both availability and lower latency.

Fully ACID systems are PC/EC in PACELC. They refuse to give up consistency, and will pay the availability and latency costs to achieve it.

However, there are some interesting counterexamples where the C’s of PACELC are not correlated. One such example is PNUTS, which is PC/EL in PACELC. In normal operation they give up consistency for latency; however, upon a partition they don’t give up any additional consistency (rather they give up availability).

In conclusion, rewriting CAP as PACELC removes some confusing asymmetry in CAP, and, in my opinion, comes closer to explaining the design of NoSQL systems.

(A quick plug to conclude this post: the PNUTS guys are presenting a new [benchmark for cloud data serving](http://research.yahoo.com/files/ycsb.pdf) which compares PNUTS vs. other NoSQL systems at the first annual [ACM Symposium on Cloud Computing 2010](http://research.microsoft.com/en-us/um/redmond/events/socc2010/) (ACM SOCC 2010) in Indianapolis on June 10th and 11th. SOCC 2010 is held in conjunction with SIGMOD 2010 and the [recently released program](http://research.microsoft.com/en-us/um/redmond/events/socc2010/program.htm) looks amazing.)

Great point about asymmetry between A and C. For such systems, which have lower utility cost of loosing transactions, PNUTS way of relaxing a fixed amount of consistency for latency makes absolute sense, at which point some incremental availability can be sacrificed.

ReplyDelete
Interesting post, Dan. Systems that are distributed across datacenters really have to tradeoff several different things. And some things (like consistency) really are more of a spectrum than a binary yes/no decision. Your classification seems to capture some of these issues quite well.

ReplyDelete
Great point on asymmetry of CAP. I think CAP is asymmetrical in the probabilities of different failures. Complete network partitioning is very very rare in current days system with redundant network switches. It would be nice to redefine PACELC with some of chances of failure information too.

ReplyDelete
Let me 'splain, no time for that, let me sum up: you can have CaP, where it is somewhat available, or AP....c where it is eventually consistent, but we're ignoring Latency. Adding latency results in the CLAP theory, as evidenced by PNUTS (versus CLAP as evidenced by peeing razor blades, after sleeping with some yahoo, which can be resolved with few doses of penicillin).

ReplyDelete
Great post Daniel. Have you had a chance to read about how MongoDB's design for distributing data? Their distribution model seems similar to PNUTS. MongoDB's auto-sharding / replicas are still in alpha, but I hear the team is shooting for a July production release.

ReplyDelete
Great article Daniel -- thanks for mentioning Sherpa.

ReplyDelete
It's worth pointing out that since the PNUTS paper was written, we've added the ability to slide the consistency tradeoff even further down to get to more availability.

Our goal is be a general purpose distributed datastore, and as such we need to provide our users with the ability to make the right tradeoffs for their application.

interesting that you bring latency into the game... it's surely a valid concern but I don't know too many people that are using the larger systems (hbase, vertica (although, I've def. done 30-40k requests/second w/vertica) ) for live reporting like you'd do for msyql, now some of the smaller systems using key-value storage such as redis out-perform against sql day in and day out..

ReplyDelete
Thanks for the feedback (to everyone who has commented above). Peter, I heard Mike Dirolf talk about MongoDB at New England Database Summit back in January, but I haven’t had a chance to play with it yet. MongoDB has been getting a lot of buzz recently though.

ReplyDelete
Toby, do you have a sense of what percentage of your users within Yahoo prefer the timeline consistency option, what percentage prefer to tradeoff additional consistency for availability?

Excellent! I guess that GenieDB is a PA/EC system - in a non-partitioned environment we're immediately consistent (although the intrepid yet latency-hungry can optionally turn that off on a per-operation basis to get PA/EL); yet if the network partitions, we drop the consistency to remain available (reads and writes can proceed, but writes may not show up for a while, and writes from the other side of the partition of course can't show up until communications are restored).

ReplyDelete
For more info, see our white paper on the matter at http://blog.geniedb.com/2010/04/17/whitepaper-beating-the-cap-thereom/

The price of even 2PC across 2 or more Yahoo-Google or MS data centers is not that high as the author thinks: it is the order of several ms - not hundreds ms. Usually, these data centers are connected by multiple GBs links with minimum number of intermediate routers - so the only limit is the speed of light.

ReplyDelete
Hi Daniel,

ReplyDelete
About 30% of our users choose consistency over availability -- this is definitely a surprise.

We suspect this might be skewed by people porting applications that were originally written for single-mastered mysql.

-Toby

CAP is a frequent source of confusion for me.

ReplyDelete
The CAP paper from Lynch et al provides definitions for availability and partition tolerance. Are you using the traditional meanings for these terms rather than what is defined in the paper? See http://mysqlha.blogspot.com/2010/04/cap-theorem.html.

I remember the difference between CA and CP using the content from Brewer's slides -- XA provides CA, majority protocol provides CP. But in that case, I then end up thinking that CP is a superset of CA, so my understanding is a work in progress.

A cross country round trip is much closer to 100ms than hundreds of ms.

Optimized Paxos can do commit in one round trip, not two (see http://en.wikipedia.org/wiki/Paxos_algorithm#Multi-Paxos). Many web services can tolerate that latency assuming transactions are structured with that in mind (VoltDB has similar constraints for high-performance OLTP).

Alaric, I'm pleased to see that PACELC can be applied to GenieDB :)

ReplyDelete
Toby, thanks for the data.

3a4ot, I think you overestimate the speed of light.

Mark,

Whether you use traditional definitions or the definitions from the Gilbert and Lynch paper (which I linked to when alluding to the definition of consistency in the PNUTS and CAP section), the difference between CA and CP are are either minor or nonexistent when it comes to building a distributed system. The difference between CA and CP hasn't affected the design of any system that I know of. All the action and decision making is regarding CA/CP vs AP.

I strongly agree that 2PC is not necessary for consistency in general (which I think I mentioned in the original post). I also agree that some systems would rather pay a single round trip latency rather than give up consistency in the absence of failures or partitions. PA/EC systems (and even PC/EC systems) certainly have practical applications in the real world.

The differences between CA and CP are significant to me.

ReplyDelete
Protocols like XA provide CA and protocols like Paxos provide CP. CP & CA systems are running in production today but most of the R&D is on CP.

See page 4 from Brewer's keynote for examples of each - http://www.cs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf

Excellent. I had the same feeling when I blogged about classifying systems by CAP. I too found myself struggling to understand the true difference between a CA and a CP system. It always felt like the difference boiled down to the system itself - how it handled the partition so I introduced a fudge factor I called recovery - how does the system recover from the missing CAP. Your solution is better.

ReplyDelete
However I think there may be a missing dimension - causal vs non causal C. It sounds like PNUTS provides ordered C but there are ways to provide causaul updates while relaxing L.

Well written, and good post. For the lesser intellects like me, this smoothly presents why developing the current buzz nosql dbs easy

ReplyDelete
Hmmm... PACELC has an E for "else" but no I for "if" which makes me have to re-interpret the abbreviation every time i look at it. Perhaps this would be more immediately interpretable if it was

ReplyDelete
P?(A|C):(L|C)

;-)

---

ReplyDelete
The difference between CA and CP hasn't affected the design of any system that I know of.

---

I agree with pretty much everything else you said, but I don't agree with this one. If you assume that the network link never partitions, there are simplified system designs you can choose. For example: most EMC storage arrays I know of are 2 node systems at the frontend with a shared SAS network at the backend to get to the actual data on disk, with an extra link between them for private communication. But the 2 nodes don't really worry so much about partition (presumably because it's the same chassis etc). To me, this is a distributed system that chose CA, and not worry about P at all, and I can see how the array design is simplified because of that.

But your point is valid, and you can teach a CP system to be CA system with a bit of extra work and no semantic difference w.r.t the client of the system.

One approach in a split-brain situation is (assuming at least three datacentres) to use a quorum approach where the service can continue as long as one of the service partitions holds a majority (defined as more than half) of the service. Increasing numbers of data-centres and maintaining an odd number increases the availability to the point where availability would only be compromised in an extremely improbable circumstance.

ReplyDelete
Only where the largest group of service-partitions cannot form a quorum would the service become unavailable. With large (five or more) globally distributed data-centres then if there is no group of three that can communicate then this would suggest some sort of extreme failure that perhaps it's best that the service does not continue.

So, it would seem to me that the trade-off in this scenario is one of performance - i.e. in all likely scenarios there will be no loss of consistency nor availability, but simply one of the aggregate performance of the service.

Good post. I think CAP, like ACID and BASE, is a bit contrived. It seems to me that there's a bit of stretch to make the acronyms pronounceable and "catchy". I think it confuses people (self included) because of that. IMHO, CAP, ACID, BASE are all still good for providing context and shouldn't be taken quite so literally. However, I am starting to like PACELC now as well. :-)

ReplyDelete
I really liked the PACELC model much better than the CAP explanations I have seen so far. I used it in my recent summary of a Paxos variant for WANs. http://muratbuffalo.blogspot.com/2010/10/mencius-building-efficient-replicated.html

ReplyDelete
Thanks Dan. Great post.

CAP seems, to me, to mean that you need to trade-off the three dimensions, not that you need to only choose two of the three. The latter view is too simplistic. In reality, each pair of the three can be traded off against each other. (In the triangle model, approaching any of the vertices makes you more distant from the other two.)

ReplyDelete
More generally, "A" in CAP stands for operational availability, which can subsume how well (according to latency, throughput, etc. metrics) a system is available for operations.

ReplyDelete
Hi Daniel,

ReplyDelete
I just found out about your blog post. I think you are right. I guess that part of the confusion around the CAP theorem comes from an unclear understanding of what C, A, and P actually mean.

Imho, it does not make much sense to talk about consistency without a specific application or system architecture in mind. For example, in the case of a relational database, consistency usually equals integrity constraints & atomic transactions; in the case of Dynamo/Cassandra it is specified by the N,R,W configuration of the quorum protocol (or hard-wired consistency level); et cetera.

In a similar sense, when defining availability, there should be a time constraint (e.g. if the ping does not return after 2 secs, the app is down). Everything in between [0, 2] is the "availability spectrum", aka latency. Apparently, it is again application specific what the upper bound should be and when we talk about latency as opposed to availability.

I agree that from a client perspective there is no difference between unavailability due to server failure and unavailability due to network partition. However, different repair mechanisms will be used in either case so it might make sense to differentiate when looking from a system perspective (?)

Thoughts?

Thank you,

Markus

This was so interesting that I wrote a blog entry about it. See http://danweinreb.org/blog/improving-the-pacelc-taxonomy

ReplyDelete
Markus, using integrity constraints is not the right way to think of it. Just because the DBMS's integrity constraints are met does not mean that the data is correct.

On integrity vs. correctness: at a former employer of mine, an internal study estimated that about 50% of all non-financial entries in the company's various data sources (conventional and relational DBMSs, spreadsheets, etc.) were incorrect: misspelled names, obsolete addresses, etc.

ReplyDelete
It's good to see the discussion pick up again. Markus, I agree that consistency can mean different things for different applications, and this can cause confusion. Dan, I added a comment to your post.

ReplyDelete
Yet another paper summary/review where I had to resort to the PACELC model.

ReplyDelete
http://muratbuffalo.blogspot.com/2011/01/lessons-from-giant-scale-services.html

I'll never stop to learn from you Dr.Abadi. Thanks,

ReplyDelete
Great post. However, latency and availability are also correlated. One could argue that loss of availability is merely high latency. Thus, PACELC can be reduced to PACEAC. This new formulation calls out what I see as the central contribution in your argument, which is that systems do not have to mindlessly couple the behavior they exhibit when the network is partitioned with the behavior they exhibit when it is not partitioned. The trade off made by PNUTS in decoupling the two is interesting, but what I would most like to see is PAEC - a system that provides consistency when the network is not partitioned, and only relaxes consistency when and as needed to deal with network partition. In other words, I would like a system that makes an effort to achieve consistency at the expense of some latency, but then falls back when it detects that the network is down and deals with any inconsistencies introduced through conflict resolution later on. With this behavior, the system takes advantage of the opportunity to avoid inconsistency whenever possible, and only pays the price of inconsistency when forced to do so to provide availability, i.e., to provide reasonable latency.

ReplyDelete
I must've misunderstood the point, but isn't latency the reason why we need distributed systems in the first place?

ReplyDelete
“consistent and tolerant of network partitions, but not available” is not strange at all. When there is strict consistency, your data is not available unless your data is replicated in a distributed system. This is the case. There is nothing strange about it and several entities are using this model, take banks and financial industry. Amazon used to favor this as well. Perhaps, you have a misunderstanding of this model.

ReplyDelete
As I understand it, you're saying PNUTS is PA/EL for reading, but PC/EC for writing?

ReplyDelete
Thus, going back to CP or AP, it's AP for reading and CP for writing. (with the implication that dropping C can give L - as is done for reading).

Am I right in thinking that PNUTS can give low latency reads when partitioned? That's not obvious from saying it's PA/EL, which suggests low latency is only achieved when not partitioned, as it's only in the Else clause.

I really liked this post. It made me reflect more about the CAP theorem which I always saw as something with a restricted practical usefulness. That's because the tradeoff points in any solution, or more specifically their consequences, depend on the required usage scenarios and on the concrete system design. Still it was great food for thought, and it is true that this is about a pattern, which has a predefined set of tradeoffs that need to be considered. I posted myself on this subject:

ReplyDelete
http://architectedsystems.blogspot.de/2012/12/cap-and-other-tradeoffs.html

PNUTS doesn't even have a homepage, with downloads, docs, a forum or a mailing list, or anything like it. Small wonder, then, that it's almost unknown.

ReplyDelete
True Network Partitions are a joke problem, but the P in the CAP theorem really stands for "Bad networking", i.e. "arbitrary message loss or failure" or unreliable latency, etc.

ReplyDelete
True partitions are a joke because:

If clients are partitioned from your servers, then CAP will not help you; you have no service for those clients. If clients are partitioned from some servers they should use the ones they can access (but access protocol needs to enforce that).

The first soluble problem case is when servers are partitioned in two (Quorum/SubQuorum) classes, but clients can see all servers. If sub-quorum servers refuse service, and clients try multiple servers before giving up, then CAP (but not L) is maintained.

And so it goes. But my point is that unreliable messaging is the actual meaning of P in Brewer's theorem, and by my standards two server clusters communicating over WAN between continents are in a Permanent state of Partition.

Which means that in a way I agree with Mr Abadi, though I conceptualize it more like this:

There is a more fundamental theorem(^*) that two databases cannot be reliably synchronized across an unreliable messaging network (aka IP). In practice this means that any DB-network can be rendered non-C through (malicious, generally) P. I.e. the entire CAP theorem is a sick joke.

However, all is not lost, because we ignore the "proof" case and recall Stephen J Gould's definition of Scientific Fact. It is in fact possible to factually synchronize DBs to any level of certainty by trading in latency (except in the face of malicious P).

Not to go all real-world on you, but if you are selling the Mona-Lisa online, you have no choice but to have a single point of failure for completing the final transaction. There are strategies to move that single point, but doing so automatically without human intervention will have at least one failure mode. (with human intervention doesn't guarantee success, but does make it not-analyzable).

(*) [ IIRC: given DBs A & B, both known to be in state S0: A transitions to S1; A&B communicate with unreliable messages (either unknown arrival or unknown latency) in order for B to transition to S1. It is impossible for B to "know" that A knows that B has transitioned to S1 (i.e. knowledge of synchrony is actually forbidden).

Imagine a (two-phase commit) protocol such that A&B serve S only so long as they are synchronized; when unsynchronized they queue requests and await synchronization. A receives update, begins queueing requests, communicates update to B; when they are synchronized again, they process their queues. Such a protocol can never be "honestly" implemented. ]

This article and comments are very interesting. You are discussing synching Distributed DBs using the PACELC protocol theory. This is all understandable when the DB nodes are all interconnected by very high speed transmission lines directly connected and you have maybe 50 to 100 nodes. But is this scalable to 100,000 nodes? Some how I am not sure.

ReplyDelete
What I am curious about is a completely Decentralized Network Database that uses a common Internet Wi-Fi connection speed of 15 to 20 MB/s. Does the theory work with say 500 million nodes?

Just wondering...

Lloyd
