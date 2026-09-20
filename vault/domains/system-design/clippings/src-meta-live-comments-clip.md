---
title: 'Live Commenting: Behind the Scenes'
source: https://engineering.fb.com/2011/02/07/core-infra/live-commenting-behind-the-scenes/
author: Ken Deeter; Changigi
published: '2011-02-07'
site: Engineering at Meta
clipped: '2026-09-20'
---

# Live Commenting: Behind the Scenes

Commenting on Facebook content has been an asynchronous form of communication. Until now. Live commenting, which we rolled out to all of our users a couple weeks ago, creates opportunities for spontaneous online conversations to take place in real time, leading to serendipitous connections that may not have ever happened otherwise.

While conceptually simple, it took several attempts by different teams of engineers before we finally settled on the right design. This wasn’t a small challenge: every minute, we serve over 100 million pieces of content that may receive comments. In that same minute, users submit around 650,000 comments that need to get routed to the correct viewers. To make this feature work, we needed to invent new systems to handle load patterns that we had never dealt with before.

## Pushing vs. Polling Data

Initially we investigated a poll-based approach. For every page that had comment-able content, the page would periodically send a request to check whether new comments had arrived. By increasing the polling frequency, we could approximate a real-time feel. Unfortunately, simple experimentation led us to quickly conclude that this approach would not scale. Because humans are so sensitive to latency in real-time communications, creating a truly serendipitous commenting experience requires comments to arrive as quickly as humanly and electronically possible. In a poll-based approach this would mean a polling interval of less than five seconds (and that would still feel slow!), which would very easily overload our servers.

So we needed a push-based approach. To be able to push information about comments to viewers, we need to know who may be viewing the piece of content that each new comment pertains to. Because we serve 100 million pieces of content per minute, we needed a system that could keep track of this “who’s looking at what” information, but also handle the incredible rate at which this information changed.

## Write Locally, Read Globally

Storing these one-to-one, viewer-to-content associations in a database is relatively easy. Keeping up with 16 million new associations per second is not. Up until this point, Facebook engineering had built up infrastructure optimized for many more reads than writes. But now we had flipped the game. Every page load now requires multiple writes (one for each piece of content being displayed). Each write of a comment requires a read (to figure out the recipients of an update). We realized that we were building something that was fundamentally backwards from most of our other systems.

At Facebook, traditionally, writes are applied to one database and asynchronously replicated to databases across all regions. This makes sense as the write rate is normally much lower than the read rate (users consume content much more than they produce). A good way to think of this approach is “read locally, write globally”.

Because of our unique situation, we settled on the completely opposite approach: “write locally, read globally.” This meant deploying distributed storage tiers that only handled writes locally, then less frequently collecting information from across all of our data centers to produce the final result. For example, when a user loads his News Feed through a request to our data center in Virginia, the system writes to a storage tier in the same data center, recording the fact that the user is now viewing certain pieces of content so that we can push them new comments. When someone enters a comment, we fetch the viewership information from all of our data centers across the country, combine the information, then push the updates out. In practice, this means we have to perform multiple cross-country reads for every comment produced. But it works because our commenting rate is significantly lower than our viewing rate. Reading globally saves us from having to replicate a high volume of writes across data centers, saving expensive, long-distance bandwidth.

Building this new system required constant coordination between front-end and back-end engineers. Contributions from [Prasad Chakka](http://www.facebook.com/Prasad), [Adam Hupp](http://www.facebook.com/AHupp), [Elliot Lynde](http://www.facebook.com/elynde), [Chris Piro](http://www.facebook.com/cpiro), [Tom Occhino](http://www.facebook.com/tomo), and [Tom Whitnah](http://www.facebook.com/tomw) were all instrumental to our success. Like many others, this effort started at a Hackathon, and grew into a full, site-wide feature. This story is just another example of a small team of engineers working closely to identify and build innovative solutions that operate at immense scale.
