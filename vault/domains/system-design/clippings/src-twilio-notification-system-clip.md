---
title: Understanding Twilio Rate Limits and Message Queues
source: https://support.twilio.com/hc/en-us/articles/115002943027-Understanding-Twilio-Rate-Limits-and-Message-Queues
published: '2024-02-27'
site: Twilio Support
clipped: '2026-09-20'
---

# Understanding Twilio Rate Limits and Message Queues

## Overview

There are limits to how quickly messages can be sent to wireless carrier networks. This guide explains how Twilio processes your message requests, and limitations for each phone number type.

**Notice**: You can send messages to Twilio at a rapid rate, as long as the requests do not max out your Twilio account's REST API concurrency limit.  When this concurrency limit is reached, Twilio will begin responding to your requests with `HTTP 429`, or [Error code 20429](https://www.twilio.com/docs/api/errors/20429). For more information, see [Twilio API response Error 429 "Too Many Requests"](https://support.twilio.com/hc/en-us/articles/360044308153-Twilio-API-response-Error-429-Too-Many-Requests-).

## What You Need To Know

### API Request Queuing

When Twilio receives message requests from your application, these requests are queued for delivery in the order we receive them.

Historically, all messaging through Twilio was queued at a per-sender level. As of October 2021, Twilio has begun transitioning toward different messaging throughput and queuing behaviors in some cases.

### Per-sender vs. Per-account or Campaign Queuing

As of October 2021, Twilio is beginning to transition toward account-level messaging throughput, and (in the case of A2P 10DLC messaging to the US) Campaign-level throughput. Some Twilio customers have already received email communications about being given early access to account-level throughput; please see our [Account-Based Throughput Overview](https://www.twilio.com/docs/messaging/guides/account-based-throughput-overview) for details.

In general, each of your Twilio phone numbers has a separate queue, and each queue can hold up to 10 hours' worth of [message segments](https://www.twilio.com/blog/2017/03/what-the-heck-is-a-segment.html) based on the sending rate for a phone number type. For example, a local phone number from the US or Canada has a full queue of 36,000 message segments.

 

Note: The size of a message segment can vary depending on the type of characters included in the message body. This guide explains segment sizes and encoding: [How Twilio Encodes your Messages](https://www.twilio.com/docs/glossary/what-is-gsm-7-character-encoding). We also provide a free tool [Segment Calculator](https://twiliodeved.github.io/message-segment-calculator/) to help identify the type of encoding detected for a message and the number of message segments it will send in. This should help provide the best estimate for true MPS and queueing based on the table below.

For account- and Campaign-level queuing, those queues can also hold up to 10 hours' worth of message segments, based on the MPS sending rate allocated to that sender type or Campaign.

 

### Twilio Message Request Processing - SMS

The rate at which Twilio dequeues messages varies depending on the origination and destination in the message requests. Below is a quick summary of the default dequeue rate.

**Note on Daily Account Limits:** The MPS rates below reflect the technical throughput speed of each sender type. However, if your account is a net new upgrade without an approved Business Primary Customer Profile, your total combined sending across all sender types is capped at **20,000 messages per day** until business verification is complete.

|                **From** |                **To** |                **Message Segments per Second (MPS)** |                **Maximum Queue Length (Message Segments)** | 
| Twilio SMS-capable local, mobile or Hosted SMS number | Canada | 1 | 36,000 | 
| Twilio US & CA Toll Free number | US and Canada |                3****** |                108,000****** | 
| Any Twilio SMS-capable number or Alphanumeric sender ID | Other international countries | 10 | 360,000 | 
| Registered A2P 10DLC Campaign* | US mobile users |                [Varies](https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US) | Campaign MPS * 10 hours (example: 40 MPS * 10 hours = 1,440,000) | 
| Registered A2P 10DLC Special* Campaign with per-number throughput (e.g. Agents/Franchise) | US mobile users |                [Varies](https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US) | Campaign per-number MPS * number of phone numbers * 10 hours | 
|                Twilio [Short Code](https://help.twilio.com/articles/223182068-What-is-a-Messaging-Short-Code-) | US, Canada or UK |                100****** |                3,600,000****** | 
| RCS Sender (Text and Media) | All Countries | 100 Messages Per Second | NA | 
| WhatsApp Sender (Text and Media) | All Countries | 80 Messages Per Second | NA | 

Sending unregistered traffic to users in the US is not possible. See [What is A2P 10DLC](https://help.twilio.com/articles/1260800720410-What-is-A2P-10DLC-) for more information.******[Contact Sales](https://www.twilio.com/help/sales) for more. [See here](https://help.twilio.com/articles/4411046744987-Toll-Free-SMS-and-MMS-messaging-throughput-MPS-) for details about Toll-Free message throughput.

Note: the dequeue rate mentioned above is a rough estimate, and not an SLA for delivery speed. Multiple factors, such as traffic congestion or carrier issues may impact the actual delivery rate.

## Frequently Asked Questions

### 
What if I need higher message throughput (MPS)?

 

#### **Sending to Non-US Countries with Non-Local Numbers**

When sending 1-way SMS to many non-US/Canada countries using a non-local number, it is usually acceptable to simply buy additional Twilio numbers to achieve higher throughput.

For example, imagine you are sending 1-way notification messages toward users in Germany using a single Twilio UK phone number. With that one UK Twilio number, you will be able to send 10 message segments per second (MPS) to your recipients. (You can see this sending rate in the third row of the table above). If your service began seeing heavy utilization and 10 MPS was not enough to deliver the messages in a timely manner, you could buy an additional Twilio number and double your throughput to 20 MPS.

Twilio highly recommends using [Messaging Services](https://support.twilio.com/hc/en-us/articles/223181308-Getting-started-with-Messaging-Services) to help manage multiple phone numbers.

#### **Sending to Non-US countries with Local Numbers**

The rules may vary when using Twilio numbers from a specific country to send in-country messages. Please consult the [SMS Guidelines](https://www.twilio.com/guidelines/sms) page for the country in question for any specific compliance considerations.

#### **Sending to the United States and Canada**

US and Canada carrier rules discourage using additional phone numbers solely to achieve higher messaging throughput. This practice is referred to as "snowshoeing."

It is acceptable to use multiple numbers to send the same messaging traffic when there is a specific business justification (for example, a restaurant with 20 locations, or a car dealership where each sales and service agent has their own number).

**Toll-Free Messaging**

If you need higher MPS sending rate on a Toll-Free number, you can [talk to Sales](https://www.twilio.com/help/sales) about our Traffic Optimization Engine. For more information, navigate [here](https://www.twilio.com/docs/messaging/features/traffic-optimization-engine).

**Long Code (10DLC) Messaging**

The new [A2P 10DLC](https://support.twilio.com/hc/en-us/articles/1260800720410-What-is-A2P-10DLC-) system introduced by US carriers in 2021 will soon make per-number MPS obsolete by enforcing MPS limits at a Campaign (use case) level, rather than at the level of individual phone numbers. See [Message throughput (MPS) and Trust Scores for A2P 10DLC in the US](https://support.twilio.com/hc/en-us/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US) for details.

#### **Twilio Message Request Processing - MMS**

Note: Twilio supports MMS messaging in the United States and Canada only.

| **Sender type** | **MMS MPS Limit** | **Notes** | 
| Long code (10DLC) | [Varies](https://help.twilio.com/articles/1260803225669-Message-throughput-MPS-and-Trust-Scores-for-A2P-10DLC-in-the-US#h_01FAKRH9GPW151AZCA0P49DSV1) ; 50 MMS/sec per Twilio Parent Account | This limit is fixed and cannot be increased. | 
| Toll-Free | 25 MMS/sec per Twilio Parent Account | Separate account-level limit from long code MMS. Cannot be increased. | 
| Short code | 40 MMS/second | Cannot be increased. | 

For further details, see [Twilio Multimedia Messaging (MMS) Account Rate Limits](https://support.twilio.com/hc/en-us/articles/360034954613-Twilio-Multimedia-Messaging-MMS-Account-Rate-Limits).

### Why is MMS Throughput Lower Than SMS?

MMS throughput is lower than SMS, due to reduced capacity in the carrier ecosystem for MMS compared to SMS.

Carriers have had an incentive to increase the reliability of SMS messages as these are often business critical. MMS, however, lends itself more towards marketing, and as such they haven’t made the same investments in it.

#### **Inbound Messages**

Inbound messages are queued at 500 messages per second for each Twilio destination. Twilio will make an HTTP request to the request URL for each message received at your number. Therefore, please make sure your server is capable of handling the load if you are expecting a large amount of concurrent inbound traffic.

If you have further questions regarding message queue lengths and latency, please [Contact Twilio Support](https://help.twilio.com/).
