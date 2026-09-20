%% trellis:begin %%
# Message Queues
*Async & Streaming*

Queues vs pub-sub, backpressure, consumer scaling, and when async is the wrong call.

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/system-design/map/correctness.outbox|Dual Writes & Outbox]], [[domains/system-design/map/problems.foundations.job-scheduler|Distributed Job Scheduler]], [[domains/system-design/map/problems.social.chat-messaging|Chat & Messaging (WhatsApp)]], [[domains/system-design/map/problems.social.news-feed|News Feed & Timeline (Twitter/Facebook)]], [[domains/system-design/map/problems.social.notification-system|Notification System]], [[domains/system-design/map/problems.search.web-crawler|Web Crawler]], [[domains/system-design/map/problems.search.news-aggregator|News Aggregator (Google News)]], [[domains/system-design/map/problems.realtime.online-judge|Online Judge (LeetCode)]]

## Readings
- [[aws-queue-backlogs|Avoiding insurmountable queue backlogs (AWS Builders' Library)]]
- [[queues-dont-fix-overload|Queues Don't Fix Overload (Fred Hébert)]]

## Drills
- [[design-chat-messaging|Drill: Design a chat and messaging system (WhatsApp-style)]]
- [[design-job-scheduler|Drill: Design a distributed job scheduler like a cron-as-a-service platform]]
- [[design-news-aggregator|Drill: Design a news aggregator (Google News)]]
- [[design-news-feed|Drill: Design a news feed / timeline like Twitter or Facebook]]
- [[design-notification-system|Drill: Design a multi-channel notification system]]
- [[design-online-judge|Drill: Design an online judge like LeetCode or Codeforces]]
- [[design-web-crawler|Drill: Design a polite, distributed web crawler]]

## Cards (6)
1. [[async-queue-vs-pubsub]]
2. [[async-broker-selection]]
3. [[async-competing-consumers-ordering]]
4. [[async-queue-backpressure]]
5. [[async-retry-delay-implementation]]
6. [[async-when-async-is-wrong]]
%% trellis:end %%

## Notes
