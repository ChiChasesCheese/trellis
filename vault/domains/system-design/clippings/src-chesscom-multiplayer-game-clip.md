---
title: An Update Regarding Our Server
source: https://www.chess.com/blog/CHESScom/an-update-regarding-our-server
author: Chess com Team
published: '2023-02-06'
site: Chess.com
clipped: '2026-09-20'
---

# An Update Regarding Our Server

# An Update Regarding Our Server

Dear Chess.com community,

On January 23rd, we shared an [update](https://www.chess.com/blog/CHESScom/chess-is-booming-and-our-servers-are-struggling) regarding how much and how quickly chess has grown and how challenging that has been for our company, especially our "Live Server" on which games are played. Growth has only increased since then.

On Friday, February 3, we had a record 403,000 new members register on Chess.com. That's mind-boggling and exciting. It's also painful. We want to be fully celebrating this chess boom, but to be honest, we have felt more pain than joy as our services have struggled to manage traffic during peak hours. We are very, very sorry for the issues so many of you have experienced in recent weeks.

Fortunately, we do feel we see the light at the end of this tunnel, and we want to provide a new update on what we have done in the past two weeks and what we have achieved. That said, we are not yet at the level of stability to which we aspire. This is very much a work in progress.

**What has happened?**

- Chess.com's traffic has more than doubled over the last several months. In January alone, traffic increased from 7 million daily users to more than 11 million daily users.
- This happened for many reasons, including being highly ranked (even #1) in app stores, having lots of great events, the amazing chess community sharing their enthusiasm on social media, chess creators making amazing content, and Mittens.
- This traffic has caused our servers and infrastructure to struggle significantly. Two primary issues many have experienced are 502 errors, which occur when our database is overloaded, and live server disconnections, which occur when our server is overloaded.

**What have we been doing?**

Addressing this level of traffic increase is not as simple as identifying one bottleneck and removing it. There are numerous hardware and cloud infrastructure components that need to be scaled as well as various optimizations that must be made. Here are some of the things we have done in the last two weeks.

- We purchased ~$2 million in hardware (web servers, database servers, new live chess server, load balancers, and additional services machines). The most vital hardware has now been installed, but more will be installed in the coming week. Although $2 million sounds like a lot, it would be a [lot more](https://dev.37signals.com/our-cloud-spend-in-2022/) (unaffordably so) if Chess.com were hosted entirely in the cloud.
- We have been sharding and decoupling our database infrastructure as quickly as possible. There has been a lot of progress here as many MySQL tables have been split out, and our code has been refactored to point to those new tables.
- We pinpointed and fixed many software bottlenecks which weren’t apparent before we hit this scale.
- We discovered that one of the uplinks between our data center and one of our cloud providers (We do use cloud for appropriate cases!) has reached capacity and seems to be dropping packets when we are experiencing peak traffic.
- We applied a cap to the number of non-premium members able to access our live server during peak hours. We have been rolling this cap back as metrics improve and expect the cap to be fully lifted soon.

- Throughout this process, every possible engineer at Chess.com who can contribute is working on these issues.

**What have we achieved?**

This is not a "Mission Accomplished" update. We are very much still working to achieve the level of performance to which we aspire. That said, we've made measurable improvements that we want to share.

- We have reduced our 502 “database overload” errors by more than 90%.
- We have also reduced the frequency of disconnections from the Live Server by more than 90% and made reconnection easier in the event of disconnection.

**What do we still have to do?**

In the coming months, we will continue to make many improvements both large and small to our servers that we hope will continue to make a positive impact for our members. Here are some of the changes we can share.

- We are installing all of the hardware that is yet to be delivered to continue to expand capacity.
- Our entire engineering team remains absolutely focused on solving all of the remaining issues including further database work, optimizing queries, breaking off pieces of the monolithic application, and moving to more services.
- We will be working with our datacenter and cloud provider to address their constraints.
- We are in the process of re-writing our Live Server so that we can move from a single server to a distributed service that could scale horizontally across numerous servers. We currently run only a small amount of games on this service (games by guests and most unrated games) as we test, tune, and develop the features. However, this week we are starting to test rated games on this service as well, and we hope that soon we will be hosting the majority of Chess.com games from a distributed, scalable service rather than one mega server.

**What are we doing to make this right?**

We know that many of you, including premium members, have lost games due to disconnection or have not been able to access a service for which you are paying. We want to make that right.

- This week we will be implementing automated rating refunds for games lost due to server instability. This will be a short-term relief plan for those impacted while we address the core issues.
- We are making Puzzle Battles free for all members for the remainder of February.

- For our premium members, this month we will add premium courses by GMs [Magnus Carlsen](https://www.chess.com/players/magnus-carlsen) ,[Peter Svidler](https://www.chess.com/players/peter-svidler) ,[Hou Yifan](https://www.chess.com/players/hou-yifan) , and more from Chess24's content library to the Chess.com Lessons library.

In the words of our CEO Erik (wait, that’s me… I wrote this article…), “I feel three things incredibly deeply every day: 1. heartbroken every time I see the frustration our members feel when the service is unstable, 2. proud of our team for everything they have done in this short amount of time given the unpredictability, and 3. hopeful and confident that we will be in a much, much better place very soon.”
