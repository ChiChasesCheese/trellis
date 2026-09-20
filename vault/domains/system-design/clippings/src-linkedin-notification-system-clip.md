---
title: 'Air Traffic Controller: Member-First Notifications at LinkedIn'
source: https://www.linkedin.com/blog/engineering/messaging-notifications/air-traffic-controller-member-first-notifications-at-linkedin
author: Changji Shi Engineer March 1
published: '2018-03-01'
site: Linkedin
clipped: '2026-09-20'
---

# Air Traffic Controller: Member-First Notifications at LinkedIn

# Air Traffic Controller: Member-First Notifications at LinkedIn

*Co-authors: [Changji Shi](https://www.linkedin.com/in/changji-shi-a480459/) and [Adriel Fuad](https://www.linkedin.com/in/adrielfuad/)*

LinkedIn’s mission is to connect the world's professionals to make them more productive and successful. Notifications are a powerful way to realize this mission by helping members never miss a conversation or opportunity that matters to them, whether that’s recommendations on jobs, a daily rundown of trending news, or updates on activity happening in their network.

However, repetitive, excessive and low-quality notifications can create a bad experience for members, lead members to file complaints and disable notifications, and make members less likely to use the LinkedIn app. Based on member feedback and dissatisfaction with excessive notifications, we decided to unify all LinkedIn notifications under one platform to optimize for and provide the best experience for our members. This platform became [Air Traffic Controller](https://www.slideshare.net/EdYakabosky/air-traffic-controller-streams-processing-meetup) (ATC)—the ultimate decision maker for notifications sent to our members.

In this post, we’ll discuss why ATC is important to LinkedIn, the technology ATC is built on, the ATC platform, and features, as well as the challenges and lessons learned building a scalable and high throughput platform.

## Notifications at LinkedIn

Notifications are a central part of how members engage with each other on the LinkedIn platform and of how LinkedIn delivers professional opportunities to its members. Some examples of notifications at LinkedIn include member-to-member connection invites, job recommendations, a daily news digest, job anniversaries, and recruiter-to-member or member-to-member messaging.

*Notifications at LinkedIn*

 Notification channels include email, SMS, desktop notifications, in-app notifications, and push notifications. An in-app notification is a notification delivered within the LinkedIn app. This notification is visible to the member on the notification tab with a red dot that may have a notification counter in it. It’s a gentle way to remind the member about their current and relevant opportunities and conversations on LinkedIn. A push notification—an example for iOS is shown in the image above—is a type of message sent to a mobile device appearing as an alert-like message on the home screen (on iOS) or in the notification area (on Android), and normally comes along with a ringtone or vibration.

A couple of years ago, each LinkedIn application team was allowed to decide for itself when and how it should notify members with updates. One team’s business logic about how often or to whom to send notifications would have been isolated to that team, and not shared with other teams. This resulted in a fragmented and inconsistent tech stack across LinkedIn that led to a non-regulated, excessive, and low-quality member notification experience.

To solve this problem, we created Air Traffic Controller (ATC). Almost all notifications at LinkedIn are now sent through ATC, which acts as the gateway for notifications, managing each member’s experience across these possible notifications. Thus, ATC is built to optimize for members. Rather than being notifications-centric and focusing solely on delivering notifications, ATC optimizes and personalizes the portfolio of notifications sent to each member. ATC has what we call the "5 Rights" in mind for every notification it processes and delivers to members: getting the right message to the right member through the right channel at the right time with the right frequency—all with the goal of helping members make informed decisions about where to spend their time advancing their career.

## Platform

ATC is built on top of [Samza](https://engineering.linkedin.com/data-streams/apache-samza-linkedins-real-time-stream-processing-framework), an open source stream processing framework originally developed at LinkedIn. ATC also leverages other technologies from LinkedIn, including [Kafka](https://engineering.linkedin.com/blog/2016/04/kafka-ecosystem-at-linkedin), [Brooklin](https://engineering.linkedin.com/blog/2017/10/streaming-data-pipelines-with-brooklin), [RestLi](https://engineering.linkedin.com/architecture/restli-restful-service-architecture-scale), and [ParSeq](https://engineering.linkedin.com/blog/2017/11/parseq--asynchronous-java-made-easier). To deliver the best member experience, ATC needs to be a member state-aware machine in order to make personalized decisions for each member. ATC uses [RocksDB](http://rocksdb.org/) (a persistent key-value store developed by Facebook), which is embedded inside Samza, to maintain state. The various states ATC stores in RocksDB include: tracking events from other LinkedIn services (e.g., when a member clicks a push notification), relevance signals pushed from offline relevance batch jobs (e.g., the preferred time in a day to deliver notifications for each member), member notification settings, and the member’s historical notifications profile, which describes all previously sent notifications.  

The image below shows the high-level architecture for ATC and the processing steps each notification goes through. Note that ATC is not the service that sends the email or push notification, but is the service that makes the decision as to which channel the notification should be sent through.

*Steps a notification goes through in ATC*

 **Request decoration** One of the first steps in the ATC process is getting the metadata needed to make a notification decision. This metadata may include the member’s historical notification profile, the devices they have the LinkedIn app installed on, and their notification settings. ATC gets this information from multiple local stores (RocksDB) and from external services. ATC will also log the current notification request to help continue to build the member’s historical notification profile.

**Channel selection**

 As mentioned previously, LinkedIn can notify members through multiple channels: email, SMS, desktop notification, in-app notification, and push notification. While most members use the LinkedIn app, LinkedIn also has a number of other apps in its mobile ecosystem (e.g., LinkedIn Lite, LinkedIn Sales Navigator, etc.). ATC ensures the notification gets sent through the best channel and app to create the best possible member experience. This decision is made based on various factors, including business logic, member settings, and relevance models predicting a member’s click and notification disable rate on the fly. For example, if a member has the app installed and enables push for “Updates about your network,” ATC will begin to send push notifications instead of emails for notifications about their network activity.

**Aggregation**

 Receiving excessive notifications is annoying. No one wants to open their email and see hundreds of individual emails from LinkedIn. Based on a member’s historical notification profile, ATC can delay specific notifications, place them in a notifications queue via RocksDB, and then send a group of notifications together as one notification at a later time. For example, if ATC schedules a number of member-to-member invitation reminders to be sent in a week, ATC will group these reminders together and send them in one email. Aggregation rules can be defined via business logic, relevance scores, and member settings (e.g., weekly digest emails). In addition, within the aggregated notifications, we are able to rank these notifications and surface the most relevant or important ones to the top by leveraging relevance signals, which ATC stores from offline push jobs.

**Delivery time optimization (DTO)**

 When requests are placed in the notification queue, we can optimize for when the best time to deliver this notification is. ATC leverages the member locale information and will send the notification at a time when the member is most likely to engage with it. For example, we don’t want to send a member a notification about who’s viewed their profile while they are sleeping, but we may want members to have the Daily Rundown first thing in the morning or during their commute to work.  

**Reminder**

 At times, we may want to remind a member about a new job opportunity or important connection request. If the member hasn’t clicked on the notification or item in LinkedIn, ATC may send a reminder notification at a later time to remind the member about this opportunity.

**Filtering**

 Filtering is the guardrail for a member’s notification experience. To provide our members with the best possible experience when interacting with LinkedIn, we may want to prevent some notifications from being sent. A couple of reasons we might block a notification from being sent to a member include:

- Member has already interacted (e.g., liked, commented, etc.) with the content on-site.
- A duplicate notification is being processed.
- The content of the notification has expired.
- To prevent a member from being overloaded with notifications. ATC will rate-limit upstream applications to prevent them from accidentally spamming members.

**Relevance-based decision making**

 Initially, ATC made decisions for each of the previously mentioned features using business rules. However, to deliver more personalized notifications for our members, we embed machine learning models into multiple stages of processing. For example, for several types of notifications, ATC scores the notification based on the recipient member’s historical notifications and historical actions to predict the likelihood that this member will act on or disable the notification. With this score, ATC can choose in real time whether to drop the notification, only send the notification as an in-app notification, or send both an in-app and push notification. Similarly, ATC uses relevance to optimize a member’s notification portfolio. Since ATC knows about all the notifications that can potentially be sent a member, ATC does a holistic optimization for the notifications sent to a member, selecting a unique set of notifications for a member based on their interests and dropping less relevant ones.

## Challenges and design decisions

To best leverage notifications and provide LinkedIn’s more than 546 million members with the best-possible member experience, ATC must be a scalable, redundant, and low-latency platform. Here are some of the challenges we faced when creating ATC and the design decisions we made.

**Partitioning requests by recipient**

 ATC is a member-centric notifications system. The ATC platform is optimized to make personalized decisions for the recipient about each notification. In ATC, we accomplish this by [partitioning](https://kafka.apache.org/documentation/#introduction) the input streams consumed by ATC, which contain notification requests, tracking signals, member settings, etc, by member id. Partitioning all requests and signals by recipient ensure that all notifications for a specific recipient are routed to the same host and more specifically, the same Samza [task](https://samza.apache.org/learn/documentation/0.7.0/introduction/concepts.html#tasks). Since all the data for the member is available on the same host, data lookups are fast. If the data either cannot be partitioned by the recipient (e.g., spammer check for sender) or ATC needs additional information about the sender of the notification (e.g., a member’s connection or a recruiter), ATC will make a small number of remote calls to the necessary external services.

**Storing external signals in local store**

 ATC consumes member tracking events, member mobile device information, and relevance scores pushed from offline jobs and puts this data into the RocksDB instance residing on the SSD of the processing host. The main reason for using this local RocksDB instance is to reduce the latency to retrieve this data and increase the throughput. Reads to RocksDB only take a couple of milliseconds to compete, while remote calls can take from 10ms to 100ms. Because of the partitioning by member id, all data for one member are accessible from the same host with low latency.

**Scalability, fault tolerance, and redundancy**

 ATC is built on Samza, which provides scalability, fault tolerance, durability, and resource management. Within the data center, ATC redundancy is achieved by sending all local states to Kafka. If the job needs to be rescheduled on a new host, the stateful machine will be rebuilt by consuming the stored states from Kafka. ATC also has cross-data-center redundancy by running a copy of the job in additional data centers. If the job in one data center goes down, traffic can be shifted to another data center.  

**Traffic patterns, latency, and throughput** ATC processes many types of notifications. Each notification type may have drastically different traffic patterns and latency requirements. For example, a daily offline job like the Daily Rundown may have a daily batch of a hundred million requests and can tolerate a latency of a couple hours; however, member-to-member messaging has a steady QPS and requires the latency to be less than a second. For the Daily Rundown, we’ll spread the requests over a range of time using aggregation and delivery time optimization. For messaging, we use high-priority Kafka topics to prioritize member messages.

One way to decrease latency and increase performance is to increase the throughput in ATC. ATC aggressively makes use of thread parallelism to handle remote calls via the [Samza Async API](https://engineering.linkedin.com/blog/2017/01/asynchronous-processing-and-multithreading-in-apache-samza--part). This helps bring down the 90th percentile (P90) end-to-end latency for member-to-member messaging push notifications from about 12 seconds to about 1.5 seconds.  

However, the tradeoff for parallelizing the request processing is that requests might be processed out of order. [Checkpointing](https://samza.apache.org/learn/documentation/0.14/container/checkpointing.html) in Samza is sequentially increased; therefore, if a request is processed, but the ATC Samza job restarts before the checkpoint is set for that request, the request will be processed again. ATC handles the duplicated requests by dropping any request it has already processed, but is okay if the requests are sent slightly out of order.

**Range query** Every time a notification is processed in ATC, ATC needs to read from various local RocksDB stores. To increase performance, it needs to read multiple items from a single store at one time (e.g., all notifications delivered to a member for the previous X days). ATC uses 

[range query](<https://en.wikipedia.org/wiki/Range_query_(database)>)to take advantage of data locality in-disk. Also, range query allows us to make queries when we don't know the full key, for example, the total number of requests scheduled in a certain time period. One alternative could be storing everything as a list in a single entry. In some ways, this is better than a range query (e.g. read query time since you only read one key-value pair). However, it has disadvantages like updating a list requires a DB transaction, data retention is harder, and storage entries can be very large.

RocksDB is based on a log-structured merge-tree and the keys are sorted by serialized bytes. Therefore, we designed our keys leading with the member’s ID, so that items belonging to one member are always located continuously together on disk. For items that need to be accessed by a scheduled time, the keys also include this timestamp, such that ATC can easily do a time range query.

*Example RocksDB store for a range query*

## Conclusion

ATC is a key component of the overall member experience for LinkedIn, shaping interactions on and off the site and ensuring members never miss a conversation or opportunity that matters. ATC performs effectively at a massive scale and currently processes over a billion requests per day. With ATC, we’ve been able to cut member complaints in half and create double digit increases in member engagement site-wide. As ATC continues to grow in scale, we look forward to how we can continue to personalize the notifications sent to members and send professional opportunities in a way that members are best able to leverage them.

## Acknowledgements

The ATC platform was built with thoughtful design and hard work by the ATC team—[Joshua Hartman](https://www.linkedin.com/in/joshuahartman/), [Carl Cummings](https://www.linkedin.com/in/carlc/), [Rishi Jobanputra](https://www.linkedin.com/in/rishij/), [Cameron Lee](https://www.linkedin.com/in/cameron-lee-3846b840/), [Shubanshu Nagar](https://www.linkedin.com/in/shubhanshunagar/), [Tyler Elliott](https://www.linkedin.com/in/tylercal/), [Changji Shi](https://www.linkedin.com/in/changji-shi-a480459/), [Brad Ciraulo](https://www.linkedin.com/in/bradciraulo/), [Haoyu Wang](https://www.linkedin.com/search/results/index/?keywords=Haoyu%20Wang&origin=GLOBAL_SEARCH_HEADER), [Eric Brownrout](https://www.linkedin.com/in/ebrownrout/), [Yingkai Hu](https://www.linkedin.com/in/yingkaihu/), [Zhongen Tao](https://www.linkedin.com/in/zhongen-tao/), [Sandor Nyako](https://www.linkedin.com/in/sandornyako/), [My Trinh](https://www.linkedin.com/in/mytrinh/), [Adriel Fuad](https://www.linkedin.com/in/adrielfuad/), [Ryan Fu](https://www.linkedin.com/in/ryanfu1/), [Ryan Oblak](https://www.linkedin.com/in/ryan-oblak/), and [Timothy Brown](https://www.linkedin.com/in/timbrownatlinkedin/)— as well as LinkedIn’s communications relevance team: [Shaunak Chatterjee](https://www.linkedin.com/in/shaunakchatterjee/), [Yan Gao](https://www.linkedin.com/in/gaoyan19790000/), [Jinyun Yan](https://www.linkedin.com/in/jinyunyan/), [Ajith Muralidharan](https://www.linkedin.com/in/ajithmuralidharan/), [Viral Gupta](https://www.linkedin.com/in/viral-gupta/), [Shipeng Yu](https://www.linkedin.com/in/shipengyu/), [Romer Rosales](https://www.linkedin.com/in/romerrosales/), [Hsiao-Ping Tseng](https://www.linkedin.com/in/hsiao-ping-tseng-a7802544/), and [Xiaoyu Chen](https://www.linkedin.com/in/xiaoyu-chen-14743780/).
