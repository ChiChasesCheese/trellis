# Transcript: Design a Notification System

Source: state.json (no live recording: no per-minute shots, board history or audio)

[00:00] **system**: Interview started · 45 min
[00:00] **interviewer**: Hi, welcome. Today's problem is to design a notification system for a big consumer platform, covering push, email and SMS. Take a moment, ask me whatever you'd like about requirements, and sketch on the board as you go.
[00:29] **candidate (voice)**: okay great so now we are dealing with the notification system let me write down  everything that we need
[00:32] **interviewer**: Sure, take your time. Tell me what you're writing down as you go, so I can follow your thinking.
[00:47] **candidate (voice)**: so product team costed to send push email are
[00:50] **candidate (voice)**: let me see
[01:14] **candidate (voice)**: push email and  SMS notifications to users  either one at the time like a payment receipt or in large company a campaigns to millions of users  okay so we need to do it in streaming way
[01:18] **interviewer**: Okay, you're restating the problem, that's fine. When you say streaming, what do you mean exactly? And what would you like to ask me about scale or delivery guarantees before you design?
[01:43] **candidate (voice)**: by streaming I mean maybe sometime you need to send the payment invoices to some a small amount of users
[01:47] **interviewer**: Got it, so you mean low latency single sends versus big batch campaigns. Those two traffic types behave very differently, so keep that in mind. What questions do you have for me about scale, like how many users or notifications per day?
[02:30] **candidate (voice)**: yeah so our notification systems should serve for all of the payments are are say the products across our company right and we wanted to unified and send why our single systems hosted here so how many users per day and how many notifications we need to send out Ari per day I say
[02:34] **interviewer**: Good question. Assume about one hundred million monthly active users, and roughly five hundred million notifications a day on average, with campaign spikes of several million in a few minutes. Does that change how you'd shape the system?
[03:35] **candidate (voice)**: so we have one meeting users per month and $500 million  notifications per day for all of the users right and also the spikes can be  on several meetings  on in a few minutes so Sarah maintenance I say 5 minutes per minute per minute it's all right  Spike and on this 5 million per minute is in the number of the total notification sent  and I'm so if that is the case then
[03:39] **interviewer**: Okay, so five million per minute at peak. Can you turn that into notifications per second, both the daily average and the spike, and tell me what that implies for your design?
[03:41] **candidate (voice)**: we will
[03:58] **candidate (voice)**: so why many users per month let's say a month is
[04:09] **candidate (voice)**: 86400  seconds per day and then * 30 is about
[04:14] **candidate (voice)**: 300
[04:23] **candidate (voice)**: this 3 million  3 million
[04:26] **interviewer**: Quick nudge: the volume I gave you was per day, not per month. So what's the average per second from five hundred million a day, and how does that compare with the spike?
[04:27] **candidate (voice)**: users per month
[04:44] **candidate (voice)**: I mean we will have
[04:51] **candidate (voice)**: 500 /
[04:58] **candidate (voice)**: 10 * 10 ^ 5
[05:09] **candidate (voice)**: so that's $5, 000 notifications per second right in average and the also
[05:12] **interviewer**: About five to six thousand per second on average, yes. Now what's the peak per second, and what does that tell you about where the bottleneck will be?
[05:39] **candidate (voice)**: so it's on 10K per second we need to send out 10K per second notifications to the users  and it says I'm like 20  times  20 acts to the average right
[05:43] **interviewer**: Hold on, I pinned a note on your estimate. Five million per minute divided by sixty is what per second? Does that match the ten thousand you wrote?
[06:16] **candidate (voice)**: 5 million per second /
[06:22] **candidate (voice)**: 60  is about
[06:30] **candidate (voice)**: I mean  RC Nike  it's roughly about 10K right
[06:34] **interviewer**: It's closer to eighty thousand per second, so your peak is about eight times higher than ten thousand. Fix that on the board, then tell me which part of the system that peak stresses the most.
[06:35] **candidate (voice)**: or are 100K sorry
[06:58] **candidate (voice)**: I think the most pressure would come from this 100K per second notifications during the big time
[07:03] **interviewer**: Fair, though your ratio says two hundred to one and it looks closer to twenty to one, worth a glance. Let's move on: what would the API look like for a product team sending a single payment receipt?
[07:32] **candidate (voice)**: okay so we have a user  from outside and also we have our notification systems
[07:41] **candidate (voice)**: RSA the server here and we need to send the notifications
[07:48] **candidate (voice)**: from our server to the  to the user right
[07:52] **interviewer**: I see an arrow from App Server straight to the user. Where does the notification system sit in that picture, and what exactly does the product team send to it?
[08:03] **candidate (voice)**: API would look like  let me create a box here  the notifications
[08:13] **candidate (voice)**: notification API will be like
[08:26] **candidate (voice)**: so the first one is the post  notification
[08:33] **candidate (voice)**: no to vacations with the ID  or say
[08:48] **candidate (voice)**: a Visa the specific notification ID are generated air which can be also generated and also we have the request body in it
[08:51] **candidate (voice)**: request body
[08:52] **interviewer**: Interesting, a client-generated notification ID. What is that ID for, and what happens if the product team retries the same request twice?
[08:59] **candidate (voice)**: message about our notifications
[09:06] **candidate (voice)**: and so this one will respond with
[09:11] **candidate (voice)**: the weather ATV is success or not
[09:14] **interviewer**: So the response says success or not. At the moment of that response, has the notification actually been delivered to the phone, or something else? And who are the recipients in that request body?
[09:14] **candidate (voice)**: if success is $200
[10:03] **candidate (voice)**: no so this is something like a synchronous way because we have our app server or on the servers right we have our servers and the servers will reach out to our after or say a notification server and also our notification server will acknowledge this request and then  half of workers on and send the notifications back to the user
[10:07] **interviewer**: Okay, acknowledge first, then workers send it, that makes sense. What exactly happens between the two hundred and the actual send, and what if the notification server crashes right after it acknowledged?
[11:25] **candidate (voice)**: so if the so the 200 and actress and is you know encapsulated or rephrase the message about the notification messages in the request and got the redirected and sent to the user and then if the notification server crashes right after it acknowledged and get back to the services acknowledged then it will pick ups from some layers of you know the ongoing status and then do this send Behavior again so in order to achieve this we need some like a database here to store all the
[11:28] **candidate (voice)**: request
[11:30] **interviewer**: A durable store before acknowledging, good instinct. I pinned a question on the database: can it handle your hundred thousand writes per second at peak?
[11:49] **candidate (voice)**: so yeah so we have
[12:23] **candidate (voice)**: to our pressure is 100K per second right and a Henry per second is hard  in the right pressure to the normal sequel databases so in order to do this we need somehow to put it in  the cafe Q if that could be useful because there's a Henry K is in the peak pressure and in the normal days it will be just about 5k and that
[13:17] **candidate (voice)**: is totally acceptable this 5K comes from here we have 5 minutes a day which is roughly about 5,000 rights per second so in the normal days this secret database just works fine but when the spike comes then we need to somehow is this is the spike right so my design here isn't we can have a Kafka instead of Friday it's because Friday it's not durable enough so we will have the Kafka or see the event stream and  restore the topics of the notification topics here and then have a server to in our consumer to
[13:51] **candidate (voice)**: to reach the topic of the notifications  and then write it into the database so this is something like a synchronously so  in this way the status of the request will not disappear and  if there's something wrong with our failure or you know the notification server just shut down then we can just pick
[13:55] **interviewer**: I like the Kafka buffer. Now walk me through one message end to end: who calls Apple or Google push, the email provider and the SMS gateway, and what happens when one of those providers is slow or down?
[14:37] **candidate (voice)**: so for the Apple or Google push or email providers and SMS gateway we will just send this server to the different endpoints right and so where this user is kind of a actually different kind of
[14:50] **candidate (voice)**: services outside Services external services or say external apis let me do it here so they have the
[15:09] **candidate (voice)**: Apple notification  server or  Google or the email or the SMS so those are so those will work as a group
[15:18] **candidate (voice)**: and we will send our request from our server to this server and then
[15:52] **candidate (voice)**: let me let me repeat your question so what happens when one of those price of providers is slow or down so this means we are if we keep creating the request to them it will cause a precious to them and actually it will maybe like a DDOS attack to them so they need our rate limiter to control our rate as right so in order to do this we need to build some kind of the rate limiter
[15:57] **interviewer**: Good, a rate limiter in front of the providers makes sense. But if a provider is actually down, throttling alone isn't enough. What does the worker do with the messages that fail, and how do you avoid blocking the ones behind them?
[16:14] **candidate (voice)**: yeah
[17:10] **candidate (voice)**: so we will have our  you know we will read from our database and read all the pending notifications and then resend it to the servers right and then as soon as the service are ready then we will get prompt response from them and we have the real limited to make sure that only the we can control the overall traffic flow from our side to their side and also actually because we store all the requesting our database and we can have you know we can dive deeper into the how the database stores and messages because we have the request and we have the status and also we can have like last attempt  time
[17:14] **interviewer**: Okay, a retry sweep from the database with a last attempt time. But if Apple is down, how do your email and SMS messages in the same Kafka topic keep flowing, and how do you space out the retries?
[18:34] **candidate (voice)**: so  if we try to reach out to for example Apple server but we can get no response or 500 minutes and there's something wrong from the Apple then we will put the event back to the event stream or see the cat right and if this retry or say a less attention stamp and retries and if this retry field reach the you know a threshold then maybe we need to put it into another topic  which is some some kind of retry queue  and if this retry Q is also not going to work then may need to put it into the that letter Q to stop you know blocking other I'm going have come messages so that the other flows can just flow freely without being interfered by the repeating failures caused by some kind of the messages
[18:40] **interviewer**: Retry and dead letter topics, solid. Now the other traffic problem: a marketing campaign of millions is queued, and a payment receipt arrives. How does the receipt avoid waiting behind the campaign?
[19:14] **candidate (voice)**: okay so Market can paint off meetings is cute and the payment receipt arrives how does receive the weight waiting behind the campaign okay so I think this one is that we need somehow  track or
[19:24] **candidate (voice)**: differentiate the topics we can use some like a different partitions  here
[19:53] **candidate (voice)**: partitions are to Shard the  different types of messages and get them resolved by different consumers so they can be decoupled and the newest receipt payment receipt will only be consumed by a separate worker and the millions of campaigns a marketing campaigns can be consumed by another worker so they will not interfere with each other
[19:58] **interviewer**: Separate consumers help. But both flows still share the same Apple rate limit through your limiter. When the campaign is running flat out, how do you make sure receipts still get through?
[20:20] **candidate (voice)**: so we need to somehow you know make sure that
[20:55] **candidate (voice)**: we have some kind of great limiter to control the RCM the token bucket to control how to distribute the tokens across different types of messages right maybe for the for a specific topic like a for a specific type of message we all can only give it a threshold and the threshold are separated from the global threshold so the we can only take the top 10
[21:03] **candidate (voice)**: on the top of the first partition in the marketing campaign and also another top 10 from the
[21:11] **candidate (voice)**: the pricing what invoice  partition so that all of them can be
[21:15] **candidate (voice)**: consumed
[21:19] **interviewer**: Okay, reserved quota per message type, that works. Let's go back to the notification ID. A product team's request times out and they retry. How do you make sure the user doesn't get two payment receipts?
[21:52] **candidate (voice)**: so a product team request times out and they retry how to make sure the user doesn't give to  a payment receipt okay so this one makes
[22:27] **candidate (voice)**: us to guarantee some kind of Indemnity right and  so we have the notification ID here the request we have the notification ID  and  the product team request times out and they want to do the retry but maybe somehow the first three try out of the first and it got successful so in order to make sure everything works fine we need to
[22:33] **candidate (voice)**: let me think a bit please don't interrupt me
[22:49] **candidate (voice)**: to make sure the whole that the whole pipeline is independent the product team request time out and
[23:31] **candidate (voice)**: okay so each time we got from so so this is a server from the product team right and the product team  want to send the notification to us and they have to keep and make sure the requests are damaged so we can store the request from their team to our to our son and restore The Entity and also in this entity we can have the metadata like the original request payment  older ID and we only insert ones are saying the update once
[23:36] **interviewer**: Insert once makes sense. But where does that check happen? If it's a database lookup in the request path, you're back to a hundred thousand lookups per second at peak, and two identical retries can arrive at the same moment.
[24:14] **candidate (voice)**: so you mean maybe two requests can arrive at the two same request can arrive at the same time and be inserted concurrently right so for this thing maybe we need somehow to use like you things like the update
[24:20] **candidate (voice)**: update you in the
[24:36] **candidate (voice)**: last of the the payment order ID  is not so we can only insert once per time and then this payment order is
[25:05] **candidate (voice)**: locked somehow but I think the key issue here is the lock is not there because the road doesn't exist so for this we need some call to make sure the  in the the two request can be decoupled can be deduplicated in our notification server maybe we can just
[25:27] **candidate (voice)**: so if the payment are other ID is not already there are six secret database we need to duplicate in our server that we only insert one notification ID if it's one payment order ID per time so yeah that's pretty much about it
[25:32] **interviewer**: Here's a hint: you don't need a lock if the database enforces uniqueness on that ID, so the second insert simply fails atomically. Now a different angle, how does a campaign to ten million users actually fan out into individual notifications?
[26:11] **candidate (voice)**: that's exactly what I say because we have the payment ID already in our second database so the second one will just insert but got blocked because I'm the the the original payment already ID with the same number already there so the second one just returns 0 rows got it into our database
[26:26] **candidate (voice)**: and I'm so your second question is how does a campaign of to 10 million users actually fun out into  individual notifications
[26:30] **candidate (voice)**: so what does this mean
[26:33] **interviewer**: Fan out just means one campaign request, like send this promo to ten million users, has to become ten million separate messages. Where does that expansion happen in your design, and who stores the audience list?
[27:51] **candidate (voice)**: so we also have our audience stored in our database  and like you said we have five million audience right period per month or 1 million per month so maybe 10 million per year and this is totally acceptable in a single database and we need to find out this message to to the external apis right so first if we can fully relief if we can rely on the another robustness of the external apis then we can just send them this one single request and then it's totally acceptable if not then maybe we need to find out when read so which means something we can fetch once request with the notification IDs  and also the audience
[27:56] **interviewer**: So you'd read the audience in chunks. If that fan-out job dies after four million of ten million, how do you resume without messaging those first four million again?
[28:30] **candidate (voice)**: also and also  when we do things like an email Services maybe this email service is hosted by ourselves and we want to reduce the pressure then maybe we can do it in the batch and can show the overall traffic by our own it's like a long term period the works and we need to somehow segregate the working to a small works
[28:55] **candidate (voice)**: so this is basically like we only found out when read
[29:38] **candidate (voice)**: do you have any questions on this
[29:42] **interviewer**: Yes, one. I still don't hear what records progress. After the crash, what state tells the job it already handled the first four million, and where is it stored?
[30:41] **candidate (voice)**: okay so the first question about how the records progress so we have the requests and it request contains the list of the audiences with the you know a list of audience unique identifiers and then we need to send a huge bounce of notifications to others when we will just faster request and also fashion that maybe the unacceptable range of the audience IDs host story in our audience list and separate them by in patches and send out the email because it might be controlled by the limiter and each time we
[31:25] **candidate (voice)**: of we need to control how how soon the request can be sent and if this pressure is really huge then maybe we can just times at the outbound Kafka Q between the limiter and workers to make everything in a streaming way so that is my response to the last question and the next one is after the crash what state has job is already handled the first floor meeting and where it is where is the stores so I think for this one this means that may need to get the latest progress right so
[31:39] **candidate (voice)**: we should have some mechanisms to get the confirmation from the  external services to us so in order to achieve this we need
[32:25] **candidate (voice)**: a first we hope the external Services can have the web Hooks and they can use the web hooks to notify us  what's up which requests are completed and which are not and also when we got this request our web hooks updates then we can just update it back into our single database and I'm also we need a chronic coworkers maybe set up per hour to chronically fast the latest updates from for the most requests and the updated based on the request and also maybe we can have
[32:31] **interviewer**: Webhooks plus a reconciliation job, good. Last question: you said a single SQL database is fine, but your request table gets five hundred million rows a day. What does that table look like after a year, and what do you do about it?
[33:05] **candidate (voice)**: so we have $500 a day  I found them for the year so sorry so 500 minutes per day which means  maybe 2000 to
[33:18] **candidate (voice)**: 20K Millions per year and there's 20K Millions per year it means 20K + 10 power off
[33:28] **candidate (voice)**: sex and  his son to power a two-time two times 10 power of 10 right
[33:44] **candidate (voice)**: or else and so this means some if let's assume it's request a reach notification is 1 KB then maybe the total amount store of storage required per year is
[34:31] **candidate (voice)**: 20,000 GB are same  20 terabytes per year and if it's less for 3 years then maybe is some 60  terabytes per 3 ear and if we need replica to support highly availability then maybe three replicas are two replicas baseball Master is 200 terabytes per 3-year and this is for acceptable for the you know more than databases at least but we can do some optimize on it what do you think about it
[34:36] **interviewer**: Check your power of ten: five hundred million times three sixty five is about one point eight times ten to the eleven rows, so roughly one hundred eighty terabytes a year, ten times more. What optimizations would you apply to that table now?
[35:01] **candidate (voice)**: let me see
[35:47] **candidate (voice)**: attention oh yeah yeah I mean change this back so maybe $200 terabytes per year  and here is 600 terabytes per 3-year and  yeah so if this would be the case then we need somehow to split this database  by sharding if possible so that we can just have different groups of the records in different databases and how them separately right because I'm absolutely one single database cannot host them so many storage
[35:51] **interviewer**: Sharding makes sense. What would you shard on, and do you really need to keep every row for three years?
[37:01] **candidate (voice)**: oh no actually we can have our Chronicle jobs to remove to to to remove periodically the successful  request because there are no longer required somehow right and also if we want the traceability we can just remove the request body only and remain the notification ID or the intelligency here is a payment order ID so that we can notify the app server that time it is already there and also we can have the like the iceberg table to store the past data so are we only have the heart notifications store in our warm database and also by sharding we can just I'm sharp by different type of topics are observers or
[37:12] **interviewer**: Great, that's a good place to stop. Retention plus cold storage is exactly the right instinct. I'll put together honest feedback for you now.
[37:12] **system**: Interview ended — feedback is below.
