---
title: Set the lifespan of a message | Firebase Cloud Messaging
source: https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-lifespan
published: '2026-09-17'
site: Firebase
clipped: '2026-09-20'
---

# Set the lifespan of a message | Firebase Cloud Messaging

FCM typically delivers messages immediately after they are sent. However, this might not always be possible. For example, the device could be unavailable or FCM might intentionally delay messages to prevent an app from consuming excessive resources and negatively affecting battery life.

In these cases, FCM stores the message and delivers it as soon as possible. While this is fine in most cases, there are some apps that require notifications to be sent without delay. For example, a notification for an incoming call or an invitation to an event.

On Android and Web, you can specify the maximum lifespan of a message. The value must be a duration from 0 to 2,419,200 seconds (28 days), and it corresponds to the maximum period of time that FCM stores and attempts to deliver the message. By default, requests that don't contain this field, last for a maximum period of four weeks.

On iOS, you can set the `apns-expiration` header in the
[ApnsConfig](/docs/reference/fcm/rest/v1/projects.messages?_gl=1*1ei2w2u*_up*MQ..*_ga*MTYwNjE2ODQwOC4xNzU4MTM1Mzk1*_ga_CW55HF8NVT*czE3NTgxMzUzOTUkbzEkZzAkdDE3NTgxMzUzOTUkajYwJGwwJGgw#apnsconfig)
object. For more details, refer to Apple's documentation on [Sending
notification requests to
APNs](https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns).

Here are some possible uses for this feature:

- Video chat incoming calls
- Expiring invitation events
- Calendar events

Another advantage of specifying the lifespan of a message is that
  FCM doesn't apply collapsible message throttling to messages with a
 time to live value of 0 seconds. Keep in mind that a `ttl` value of 0 means
 messages that can't be delivered immediately are discarded. However, because
 such messages are never stored, this provides the best latency for sending
 notification messages.

Here is an example of a request that includes ttl:

```
{
  "message":{
    "token":"bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1...",
    "data":{
      "Nick" : "Mario",
      "body" : "great match!",
      "Room" : "PortugalVSDenmark"
    },
    "apns":{
      "headers":{
        "apns-expiration":"1604750400"
      }
    },
    "android":{
      "ttl":"4500s"
    },
    "webpush":{
      "headers":{
        "TTL":"4500"
      }
    }
  }
}
```
## Lifetime of a message

When an app server posts a message to FCM and receives a message ID back, it doesn't mean that the message was already delivered to the device. Instead, it means that it was accepted for delivery. When the message is delivered depends on many factors.

If the device is connected but in Doze, a low priority message is stored by
FCM until the device is out of Doze. If the `collapse_key` is set, and
there's an existing message with the same [collapse
key](/docs/cloud-messaging/customize-messages/collapsible-message-types) and
registration token waiting for delivery, the old message is discarded and then
new message takes its place. However, if the collapse key is not set, both the
new and old messages are stored for future delivery.

If the device isn't connected to FCM, the message is stored until a
connection is established. When a connection is established, FCM
delivers all pending messages to the device. If the device never gets connected
again, the message eventually times out and is discarded from FCM
storage. The default timeout is four weeks, unless the `ttl` flag is set. If the
app has been uninstalled when FCM attempts to deliver a message to the
device, FCM discards that message right away and invalidates the
registration token. Future attempts to send a message to that device results in
a `NotRegistered` error.

For Android devices, if the device hasn't connected to FCM for more
than one month, FCM still accepts the message but immediately discards
it. If the device connects within four weeks of the last data message you sent
to it, your client app receives the
[`onDeletedMessages()`](</docs/reference/android/com/google/firebase/messaging/FirebaseMessagingService#onDeletedMessages()>)
callback.

To get more insight into the delivery of messages on Android or Apple platforms,
you can use the [FCM reporting
dashboard](https://console.firebase.google.com/project/_/notification/reporting),
which records the number of messages sent and opened on Apple and Android
devices, along with data for impressions for Android apps.
