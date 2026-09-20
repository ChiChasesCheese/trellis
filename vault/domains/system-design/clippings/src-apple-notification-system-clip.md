---
title: How helpful is this document?
source: https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html
published: '2018-06-04'
site: developer.apple.com
clipped: '2026-09-20'
---

# How helpful is this document?

## Communicating with APNs

The APNs provider API lets you send remote notification requests to APNs. APNs then conveys notifications to your app on iOS, tvOS, and macOS devices, and to Apple Watch via iOS.

The provider API is based on the HTTP/2 network protocol. Each interaction starts with a POST request, from your provider, that contains a JSON payload and a device token. APNs forwards the notification payload to your app on the specific user device identified by the request’s included device token.

  A *provider* is a server, that you deploy and manage, that you configure to work with APNs.

### Provider Authentication Tokens

To securely connect to APNs, you can use provider authentication tokens or provider certificates. This section describes connections using tokens.

  The provider API supports the JSON Web Token (JWT) specification, letting you pass statements and metadata, called *claims*, to APNs, along with each push notification. For details, refer to the specification at [https://tools.ietf.org/html/rfc7519](https://tools.ietf.org/html/rfc7519). For additional information about JWT, along with a list of available libraries for generating signed JWTs, see [https://jwt.io](https://jwt.io)

A provider authentication token is a JSON object that you construct, whose header must include:

- The encryption algorithm ( `alg` ) you use to encrypt the token
- A 10-character *key identifier* (`kid` ) key, obtained from[your developer account](https://developer.apple.com/account/)

The claims payload of the token must include:

- The *issuer* (`iss` ) registered claim key, whose value is your 10-character Team ID, obtained from[your developer account](https://developer.apple.com/account/)
- The *issued at* (`iat` ) registered claim key, whose value indicates the time at which the token was generated, in terms of the number of seconds since Epoch, in UTC

  After you create the token, you must sign it with a private key. You must then encrypt the token using the Elliptic Curve Digital Signature Algorithm (ECDSA) with the P-256 curve and the SHA-256 hash algorithm. Specify the value `ES256` in the algorithm header key (`alg`). For information on how to configure your token, see “[Configure push notifications](http://help.apple.com/xcode/mac/current/#/dev11b059073)” in Xcode Help.

A decoded JWT provider authentication token for APNs has the following format:

1. `{`
2.     `"alg": "ES256",`
3.     `"kid": "ABC123DEFG"`
4. `}`
5. `{`
6.     `"iss": "DEF123GHIJ",`
7.     `"iat": 1437179036`
8.  `}`

  To ensure security, APNs requires new tokens to be generated periodically. A new token has an updated *issued at* claim key, whose value indicates the time the token was generated. If the timestamp for token issue is not within the last hour, APNs rejects subsequent push messages, returning an `ExpiredProviderToken` (`403`) error.

  If you suspect your provider token signing key is compromised, you can revoke it from [your developer account](https://developer.apple.com/account/). You can issue a new key pair and can then generate new tokens with the new private key. For maximum security, close all your connections to APNs that had been using tokens signed with the now-revoked key, and reconnect before using tokens signed with the new key.

### APNs Provider Certificates

  Your APNs provider certificate, which you obtain as explained in “[Configure push notifications](http://help.apple.com/xcode/mac/current/#/dev11b059073)” in Xcode Help, enables connection to both the APNs Production and Development environments.

  You can use your APNs certificate to send notifications to your primary app, as identified by its bundle ID, as well as to any Apple Watch complications or backgrounded VoIP services associated with that app. Use the `( 1.2.840.113635.100.6.3.6 )` extension in the certificate to identify the topics for your push notifications. For example, if you provide an app with the bundle ID `com.yourcompany.yourexampleapp`, you can specify the following topics in the certificate:

1. `Extension ( 1.2.840.113635.100.6.3.6 )`
2. `Critical NO`
3. `Data com.yourcompany.yourexampleapp`
4. `Data app`
5. `Data com.yourcompany.yourexampleapp.voip`
6. `Data voip`
7. `Data com.yourcompany.yourexampleapp.complication`
8. `Data complication`

### APNs Connections

The first step in sending a remote notification is to establish a connection with the appropriate APNs server:

- **Development server:**`api.development.push.apple.com:443`
- **Production server:**`api.push.apple.com:443`

  Your provider must support TLS 1.2 or higher when connecting to APNs. You can use the provider client certificate which you obtain from [your developer account](https://developer.apple.com/account/), as described in Creating a Universal Push Notification Client SSL Certificate.

  To connect without an APNs provider certificate, you must instead create a provider authentication token, signed with the key provisioned through [your developer account](https://developer.apple.com/account/) (see “[Configure push notifications](http://help.apple.com/xcode/mac/current/#/dev11b059073)” in Xcode Help). After you have this token, you can start to send push messages. You must then periodically update the token; each APNs provider authentication token has validity interval of one hour.

APNs allows multiple concurrent streams for each connection. The exact number of streams differs based on your use of a provider certificate or an authentication token, and also differs based on server load. Do not assume a specific number of streams.

  When establishing a connection to APNs using a token rather than a certificate, only one stream is allowed on the connection until you send a push message with valid provider authentication token. APNs ignores `HTTP/2 PRIORITY` frames, so do not send them on your streams.

### Best Practices for Managing Connections

Keep your connections with APNs open across multiple notifications; do not repeatedly open and close connections. APNs treats rapid connection and disconnection as a denial-of-service attack. You should leave a connection open unless you know it will be idle for an extended period of time—for example, if you only send notifications to your users once a day, it is acceptable practice to use a new connection each day.

Do not generate a new provider authentication token for each push request that you send. After you obtain a token, continue to use it for all your push requests during the token’s period of validity, which is one full hour.

You can establish multiple connections to APNs servers to improve performance. When you send a large number of remote notifications, distribute them across connections to several server endpoints. This improves performance, compared to using a single connection, by letting you send remote notifications faster and by letting APNs deliver them faster.

If your provider certificate is revoked, or if the key you are using to sign provider tokens is revoked, close all existing connections to APNs and then open new connections.

  You can check the health of your connection using an HTTP/2 `PING` frame. 

### Terminating an APNs Connection

  If APNs decides to terminate an established HTTP/2 connection, it sends a `GOAWAY` frame. The `GOAWAY` frame includes JSON data in its payload with a `reason` key, whose value indicates the reason for the connection termination. For a list of possible values for the `reason` key, see [Table 8-6](#//apple_ref/doc/uid/TP40008194-CH11-SW17). 

Normal request failures do not result in termination of a connection.

### APNs Notification API

  The APNs Provider API consists of a request and a response that you configure and send using an HTTP/2 `POST` command. You use the request to send a push notification to the APNs server and use the response to determine the results of that request. 

### HTTP/2 Request to APNs

Use a request to send a notification to a specific user device.

  For the *<device-token>* parameter, specify the hexadecimal bytes of the device token for the target device. 

APNs requires the use of HPACK (header compression for HTTP/2), which prevents repeated header keys and values. APNs maintains a small dynamic table for HPACK. To help avoid filling up the APNs HPACK table and necessitating the discarding of table data, encode headers in the following way—especially when sending a large number of streams:

- The `:path` value should be encoded as a literal header field without indexing
- The `authorization` request header, if present, should be encoded as a literal header field without indexing
- The appropriate encoding to employ for the `apns-id` ,`apns-expiration` , and`apns-collapse-id` request headers differs depending on whether it is part of the initial or a subsequent POST operation, as follows:
  - The first time you send these headers, encode them with *incremental indexing* to allow the header names to be added to the dynamic table
  - Subsequent times you send these headers, encode them as *literal header fields without indexing*

  Encode all other headers as literal header fields with incremental indexing. For specifics on header encoding, see [tools.ietf.org/html/rfc7541#section-6.2.1](http://tools.ietf.org/html/rfc7541#section-6.2.1) and [tools.ietf.org/html/rfc7541#section-6.2.2](http://tools.ietf.org/html/rfc7541#section-6.2.2).

APNs ignores request headers other than the ones listed in Table 8-2.

| Table 8-2 APNs request headers |  | 
|---|---|
| Header | Description | 
|---|---|
|    `authorization` |    The provider token that authorizes APNs to send push notifications for the specified topics. The token is in Base64URL-encoded JWT format, specified as `bearer <provider token>` . When the provider certificate is used to establish a connection, this request header is ignored. | 
|    `apns-id` | A canonical UUID that identifies the notification. If there is an error sending the notification, APNs uses this value to identify the notification to your server. The canonical form is 32 lowercase hexadecimal digits, displayed in five groups separated by hyphens in the form 8-4-4-4-12. An example UUID is as follows:    `123e4567-e89b-12d3-a456-42665544000` If you omit this header, a new UUID is created by APNs and returned in the response. | 
|    `apns-expiration` | A UNIX epoch date expressed in seconds (UTC). This header identifies the date when the notification is no longer valid and can be discarded.    If this value is nonzero, APNs stores the notification and tries to deliver it at least once, repeating the attempt as needed if it is unable to deliver the notification the first time. If the value is `0` , APNs treats the notification as if it expires immediately and does not store the notification or attempt to redeliver it. | 
|    `apns-priority` | The priority of the notification. Specify one of the following values:     If you omit this header, the APNs server sets the priority to `10` . | 
|    `apns-topic` | The topic of the remote notification, which is typically the bundle ID for your app. The certificate you create in your developer account must include the capability for this topic. If your certificate includes multiple topics, you must specify a value for this header. If you omit this request header and your APNs certificate does not specify multiple topics, the APNs server uses the certificate’s Subject as the default topic. If you are using a provider token instead of a certificate, you must specify a value for this request header. The topic you provide should be provisioned for the your team named in your developer account. | 
|    `apns-collapse-id` |    Multiple notifications with the same collapse identifier are displayed to the user as a single notification. The value of this key must not exceed 64 bytes. For more information, see [Quality of Service, Store-and-Forward, and Coalesced Notifications](APNSOverview.html#//apple_ref/doc/uid/TP40008194-CH8-SW5) . | 

**Table 8-2**APNs request headers

  The body content of your message is the JSON dictionary object for your notification’s payload. The body data must not be compressed and its maximum size is 4KB (4096 bytes). For a Voice over Internet Protocol (VoIP) notification, the body data maximum size is 5KB (5120 bytes). For information about the keys and values to include in the body content, see [Payload Key Reference](PayloadKeyReference.html#//apple_ref/doc/uid/TP40008194-CH17-SW1). 

### HTTP/2 Response from APNs

The response to a request has the format listed in Table 8-3.

| Table 8-3 APNs response headers |  | 
|---|---|
| Header name | Value | 
|---|---|
|    `apns-id` |    The `apns-id` value from the request. If no value was included in the request, the server creates a new UUID and returns it in this header. | 
|    `:status` |    The HTTP status code. For a list of possible status codes, see [Table 8-4](#//apple_ref/doc/uid/TP40008194-CH11-SW15) . | 

**Table 8-3**APNs response headers

  Table 8-4 lists the possible status codes for a request. These values are included in the `:status` header of the response.

| Table 8-4 Status codes for an APNs response |  | 
|---|---|
| Status code | Description | 
|---|---|
| 200 | Success | 
| 400 | Bad request | 
| 403 | There was an error with the certificate or with the provider authentication token | 
| 405 |    The request used a bad `:method` value. Only`POST` requests are supported. | 
| 410 | The device token is no longer active for the topic. | 
| 413 | The notification payload was too large. | 
| 429 | The server received too many requests for the same device token. | 
| 500 | Internal server error | 
| 503 | The server is shutting down and unavailable. | 

**Table 8-4**Status codes for an APNs response

  For a successful request, the body of the response is empty. On failure, the response body contains a JSON dictionary with the keys listed in Table 8-5. This JSON data might also be included in the `GOAWAY` frame when a connection is terminated.

| Table 8-5 APNs JSON data keys |  | 
|---|---|
| Key | Description | 
|---|---|
|    `reason` |    The error indicating the reason for the failure. The error code is specified as a string. For a list of possible values, see [Table 8-6](#//apple_ref/doc/uid/TP40008194-CH11-SW17) . | 
|    `timestamp` |    If the value in the `:status` header is`410` , the value of this key is the last time at which APNs confirmed that the device token was no longer valid for the topic. Stop pushing notifications until the device registers a token with a later timestamp with your provider. | 

**Table 8-5**APNs JSON data keys

  Table 8-6 lists the possible error codes included in the `reason` key of a response’s JSON payload.

| Table 8-6 Values for the APNs JSON  reason  key |  |  | 
|---|---|---|
| Status code | Error string | Description | 
|---|---|---|
|    `400` |    `BadCollapseId` | The collapse identifier exceeds the maximum allowed size | 
|    `400` |    `BadDeviceToken` | The specified device token was bad. Verify that the request contains a valid token and that the token matches the environment. | 
|    `400` |    `BadExpirationDate` |    The `apns-expiration` value is bad. | 
|    `400` |    `BadMessageId` |    The `apns-id` value is bad. | 
|    `400` |    `BadPriority` |    The `apns-priority` value is bad. | 
|    `400` |    `BadTopic` |    The `apns-topic` was invalid. | 
|    `400` |    `DeviceTokenNotForTopic` | The device token does not match the specified topic. | 
|    `400` |    `DuplicateHeaders` | One or more headers were repeated. | 
|    `400` |    `IdleTimeout` | Idle time out. | 
|    `400` |    `MissingDeviceToken` |    The device token is not specified in the request `:path` . Verify that the`:path` header contains the device token. | 
|    `400` |    `MissingTopic` |    The `apns-topic` header of the request was not specified and was required. The apns-topic header is mandatory when the client is connected using a certificate that supports multiple topics. | 
|    `400` |    `PayloadEmpty` | The message payload was empty. | 
|    `400` |    `TopicDisallowed` | Pushing to this topic is not allowed. | 
|    `403` |    `BadCertificate` | The certificate was bad. | 
|    `403` |    `BadCertificateEnvironment` | The client certificate was for the wrong environment. | 
|    `403` |    `ExpiredProviderToken` | The provider token is stale and a new token should be generated. | 
|    `403` |    `Forbidden` | The specified action is not allowed. | 
|    `403` |    `InvalidProviderToken` | The provider token is not valid or the token signature could not be verified. | 
|    `403` |    `MissingProviderToken` | No provider certificate was used to connect to APNs and Authorization header was missing or no provider token was specified. | 
|    `404` |    `BadPath` |    The request contained a bad `:path` value. | 
|    `405` |    `MethodNotAllowed` |    The specified `:method` was not`POST` . | 
|    `410` |    `Unregistered` | The device token is inactive for the specified topic.    Expected HTTP/2 status code is `410` ; see[Table 8-4](#//apple_ref/doc/uid/TP40008194-CH11-SW15) . | 
|    `413` |    `PayloadTooLarge` |    The message payload was too large. See [Creating the Remote Notification Payload](CreatingtheNotificationPayload.html#//apple_ref/doc/uid/TP40008194-CH10-SW1) for details on maximum payload size. | 
|    `429` |    `TooManyProviderTokenUpdates` | The provider token is being updated too often. | 
|    `429` |    `TooManyRequests` | Too many requests were made consecutively to the same device token. | 
|    `500` |    `InternalServerError` | An internal server error occurred. | 
|    `503` |    `ServiceUnavailable` | The service is unavailable. | 
|    `503` |    `Shutdown` | The server is shutting down. | 

**Table 8-6**Values for the APNs JSON

`reason` key

### HTTP/2 Request/Response Examples for APNs

Listing 8-1 shows a sample request constructed for a provider certificate.

1. `HEADERS`
2.   `- END_STREAM`
3.   `+ END_HEADERS`
4.   `:method = POST`
5.   `:scheme = https`
6.   `:path = /3/device/00fc13adff785122b4ad28809a3420982341241421348097878e577c991de8f0`
7.   `host = api.development.push.apple.com`
8.   `apns-id = eabeae54-14a8-11e5-b60b-1697f925ec7b`
9.   `apns-expiration = 0`
10.   `apns-priority = 10`
11. `DATA`
12.   `+ END_STREAM`
13.     `{ "aps" : { "alert" : "Hello" } }`

Listing 8-2 shows a sample request constructed for a provider authentication token.

1. `HEADERS`
2.   `- END_STREAM`
3.   `+ END_HEADERS`
4.   `:method = POST`
5.   `:scheme = https`
6.   `:path = /3/device/00fc13adff785122b4ad28809a3420982341241421348097878e577c991de8f0`
7.   `host = api.development.push.apple.com`
8. ```
  authorization = bearer eyAia2lkIjogIjhZTDNHM1JSWDciIH0.eyAiaXNzIjogIkM4Nk5WOUpYM0QiLCAiaWF0I
 jogIjE0NTkxNDM1ODA2NTAiIH0.MEYCIQDzqyahmH1rz1s-LFNkylXEa2lZ_aOCX4daxxTZkVEGzwIhALvkClnx5m5eAT6
 Lxw7LZtEQcH6JENhJTMArwLf3sXwi
```
9.   `apns-id = eabeae54-14a8-11e5-b60b-1697f925ec7b`
10.   `apns-expiration = 0`
11.   `apns-priority = 10`
12.   `apns-topic = <MyAppTopic>`
13. `DATA`
14.   `+ END_STREAM`
15.     `{ "aps" : { "alert" : "Hello" } }`

Listing 8-3 shows a sample request constructed for a certificate that contains multiple topics.

1. `HEADERS`
2.   `- END_STREAM`
3.   `+ END_HEADERS`
4.   `:method = POST`
5.   `:scheme = https`
6.   `:path = /3/device/00fc13adff785122b4ad28809a3420982341241421348097878e577c991de8f0`
7.   `host = api.development.push.apple.com`
8.   `apns-id = eabeae54-14a8-11e5-b60b-1697f925ec7b`
9.   `apns-expiration = 0`
10.   `apns-priority = 10`
11.   `apns-topic = <MyAppTopic>` 
12. `DATA`
13.   `+ END_STREAM`
14.     `{ "aps" : { "alert" : "Hello" } }`

Listing 8-4 shows a sample response for a successful push request.

1. `HEADERS`
2.   `+ END_STREAM`
3.   `+ END_HEADERS`
4.   `apns-id = eabeae54-14a8-11e5-b60b-1697f925ec7b`
5.   `:status = 200`

Listing 8-5 shows a sample response when an error occurs.

1. `HEADERS`
2.   `- END_STREAM`
3.   `+ END_HEADERS`
4.   `:status = 400`
5.   `content-type = application/json`
6.     `apns-id: <a_UUID>`
7. `DATA`
8.   `+ END_STREAM`
9.   `{ "reason" : "BadDeviceToken" }`

[Creating the Remote Notification Payload](CreatingtheNotificationPayload.html#//apple_ref/doc/uid/TP40008194-CH10-SW1)

Copyright © 2018 Apple Inc. All rights reserved. 
  [Terms of Use](http://www.apple.com/legal/terms/site.html) | 
  [Privacy Policy](http://www.apple.com/privacy/) | 
  [Updated: 2018-06-04](RevisionHistory.html#//apple_ref/doc/uid/TP40008194-CH99-SW1)
