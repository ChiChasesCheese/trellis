---
title: 'Browser APIs and Protocols: WebSocket - High Performance Browser Networking
  (O''Reilly)'
source: https://hpbn.co/websocket/
author: Ilya Grigorik
published: '2013-10-15'
site: High Performance Browser Networking
clipped: '2026-08-15'
---

# Browser APIs and Protocols: WebSocket - High Performance Browser Networking (O'Reilly)

## Introduction

WebSocket enables bidirectional, message-oriented streaming of text and binary data between client and server. It is the closest API to a raw network socket in the browser. Except a WebSocket connection is also much more than a network socket, as the browser abstracts all the complexity behind a simple API and provides a number of additional services:

- 
          Connection negotiation and same-origin policy enforcement
- 
          Interoperability with existing HTTP infrastructure
- 
          Message-oriented communication and efficient message framing
- 
          Subprotocol negotiation and extensibility

WebSocket is one of the most versatile and flexible transports available in the browser. The simple and minimal API enables us to layer and deliver arbitrary application protocols between client and server—anything from simple JSON payloads to custom binary message formats—in a streaming fashion, where either side can send data at any time.

However, the trade-off with custom protocols is that they are, well, custom. The application must account for missing state management, compression, caching, and other services otherwise provided by the browser. There are always design constraints and performance trade-offs, and leveraging WebSocket is no exception. In short, WebSocket is not a replacement for HTTP, XHR, or SSE, and for best performance it is critical that we leverage the strengths of each transport.

WebSocket is a set of multiple standards: the WebSocket API is defined by the W3C, and the WebSocket protocol (RFC 6455) and its extensions are defined by the HyBi Working Group (IETF).

## [§](#websocket-api)WebSocket API

      The WebSocket API provided by the browser is remarkably small and simple. Once again, all the low-level details of connection management and message processing are taken care of by the browser. To initiate a new connection, we need the URL of a WebSocket resource and a few application callbacks:

```
var ws = new WebSocket('wss://example.com/socket'); 
```
        1. 
            Open a new secure WebSocket connection (wss)
2. 
            Optional callback, invoked if a connection error has occurred
3. 
            Optional callback, invoked when the connection is terminated
4. 
            Optional callback, invoked when a WebSocket connection is established
5. 
            Client-initiated message to the server
6. 
            A callback function invoked for each new message from the server
7. 
            Invoke binary or text processing logic for the received message

The API speaks for itself. In fact, it should look very similar to the
      EventSource API we saw in the preceding chapter. This is intentional, as
      WebSocket offers similar and extended functionality. Having said that,
      there are a number of important differences as well. Let’s take a look at
      them one by one.
      
       The WebSocket resource URL uses its own custom scheme:  The primary use case for the WebSocket protocol is to provide an
        optimized, bi-directional communication channel between applications
        running in the browser and the server. However, the WebSocket wire
        protocol can be used outside the browser and could be negotiated via a
        non-HTTP exchange. As a result, the HyBi Working Group chose to adopt a
        custom URL scheme.
         Despite the non-HTTP negotiation option enabled by the custom
          scheme, in practice there are no existing standards for alternative
          handshake mechanisms for establishing a WebSocket session.
         WebSocket communication consists of messages and application code
        and does not need to worry about buffering, parsing, and reconstructing
        received data. For example, if the server sends a 1 MB payload, the
        application’s  Further, the WebSocket protocol makes no assumptions and places no
        constraints on the application payload: both text and binary data are
        fair game. Internally, the protocol tracks only two pieces of
        information about the message: the length of payload as a
        variable-length field and the type of payload to distinguish UTF-8 from
        binary transfers.
         When a new message is received by the browser, it is automatically
        converted to a DOMString object for text-based data, or a Blob object
        for binary data, and then passed directly to the application. The only
        other option, which acts as performance hint and optimization for the
        client, is to tell the browser to convert the received binary data to
        an ArrayBuffer instead of Blob:
         User agents can use this as a hint for how to handle incoming
          binary data: if the attribute is set to "blob", it is safe to spool
          it to disk, and if it is set to "arraybuffer", it is likely more
          efficient to keep the data in memory. Naturally, user agents are
          encouraged to use more subtle heuristics to decide whether to keep
          incoming data in memory or not…
           The WebSocket API, W3C Candidate
          Recommendation
         A Blob object represents a file-like object of immutable, raw data.
        If you do not need to modify the data and do not need to slice it into
        smaller chunks, then it is the optimal format—e.g., you can pass the
        entire Blob object to an image tag (see the example in  Once a WebSocket connection is established, the client can send and
        receive UTF-8 and binary messages at will. WebSocket offers a
        bidirectional communication channel, which allows message delivery in
        both directions over the same TCP connection:
         The WebSocket API accepts a DOMString object, which is encoded as
        UTF-8 on the wire, or one of ArrayBuffer, ArrayBufferView, or Blob
        objects for binary transfers. However, note that the latter binary
        options are simply an API convenience: on the wire, a WebSocket frame
        is either marked as binary or text via a single bit. Hence, if the
        application, or the server, need other content-type information about
        the payload, then they must use an additional mechanism to communicate
        this data.
         The  The preceding example attempts to send application updates to the
        server, but only if the previous messages have been drained from the
        client’s buffer. Why bother with such checks? All WebSocket messages
        are delivered in the exact order in which they are queued by the
        client. As a result, a large backlog of queued messages, or even a
        single large message, will delay delivery of messages queued behind
        it—head-of-line blocking!
         To work around this problem, the application can split large
        messages into smaller chunks, monitor the  Many applications generate multiple classes of messages:
          high-priority updates, such as control traffic, and low-priority
          updates, such as background transfers. To optimize delivery, the
          application should pay close attention to how and when each type of
          message is queued on the socket!
         WebSocket protocol makes no assumptions about the format of each
        message: a single bit tracks whether the message contains text or
        binary data, such that it can be efficiently decoded by the client and
        server, but otherwise the message contents are opaque.
         Further, unlike HTTP or XHR requests, which communicate additional
        metadata via HTTP headers of each request and response, there is no
        such equivalent mechanism for a WebSocket message. As a result, if
        additional metadata about the message is required, then the client and
        server must agree to implement their own subprotocol to communicate
        this data:
         The client and server can agree on a fixed message format
            upfront—e.g., all communication will be done via JSON-encoded
            messages or a custom binary format, and necessary message metadata
            will be part of the encoded structure.
           If the client and server need to transfer different data types,
            then they can agree on a consistent message header, which can be
            used to communicate the instructions to decode the remainder of the
            payload.
           A mix of text and binary messages can be used to communicate the
            payload and metadata information—e.g., a text message can
            communicate an equivalent of HTTP headers, followed by a binary
            message with the application payload.
         This list is just a small sample of possible strategies. The
        flexibility and low overhead of a WebSocket message come at the cost of
        extra application logic. However, message serialization and management
        of metadata are only part of the problem! Once we determine the
        serialization format for our messages, how do we ensure that both
        client and server understand each other, and how do we keep them in
        sync?
         Thankfully, WebSocket provides a simple and convenient
         As the preceding example illustrates, the WebSocket constructor
        accepts an optional array of subprotocol names, which allows the client
        to advertise the list of protocols it understands or is willing to use
        for this connection. The specified list is sent to the server, and the
        server is allowed to pick one of the protocols advertised by the
        client.
         If the subprotocol negotiation is successful, then the
         The subprotocol names are defined by the application and are sent
          as specified to the server during the initial HTTP handshake. Other
          then that, the specified subprotocol has no effect on the core
          WebSocket API.
        [§](#ws-and-wss-url-schemes)WS and WSS URL Schemes*ws*
        for plain-text communication (e.g., *ws://example.com/socket*),
        and *wss* when an encrypted channel (TCP+TLS) is required. Why
        the custom scheme, instead of the familiar *http*?
        [§](#receiving-text-and-binary-data)Receiving Text
        and Binary Data`onmessage` callback will be called only when
        the entire message is available on the client.
        ```
var ws = new WebSocket('wss://example.com/socket');
ws.binaryType = "arraybuffer"; 
```
          
        
[ws.onmessage = function(msg) {
  if(msg.data instanceof ArrayBuffer) {
    processArrayBuffer(msg.data);
  } else {
    processText(msg.data);
  }
}](#wsab)
          

        [Downloading
        Data with XHR](/xmlhttprequest/#downloading-data-with-xhr)). On the other hand, if you need to perform
        additional processing on the binary data, then ArrayBuffer is likely
        the better fit.
        
      [§](#sending-text-and-binary-data)Sending Text and
        Binary Data```
var ws = new WebSocket('wss://example.com/socket');
ws.onopen = function () {
  socket.send("Hello server!"); 
```
          
        
  [socket.send(JSON.stringify({'msg': 'payload'}));](#wstext) 
  [var buffer = new ArrayBuffer(128);
  socket.send(buffer);](#json) 
  [var intview = new Uint32Array(buffer);
  socket.send(intview);](#arraybuffer) 
  [var blob = new Blob(\[buffer\]);
  socket.send(blob);](#aview) 
[}](#wsblob)
*send()* method is asynchronous: the provided data is
        queued by the client, and the function returns immediately. As a
        result, especially when transferring large payloads, do not mistake the
        fast return for a signal that the data has been sent! To monitor the
        amount of data queued by the browser, the application can query the
        `bufferedAmount` attribute on the socket:
        ```
var ws = new WebSocket('wss://example.com/socket');
ws.onopen = function () {
  subscribeToApplicationUpdates(function(evt) { 
```
          
        
    [if (ws.bufferedAmount == 0)](#appupdate) 
      [ws.send(evt.data);](#buffer) 
  [});
};](#send)
`bufferedAmount`
        value carefully to avoid head-of-line blocking, and even implement its
        own priority queue for pending messages instead of blindly queuing them
        all on the socket.
        [§](#subprotocol-negotiation)Subprotocol Negotiation

*subprotocol negotiation* API to address the second problem. The
        client can advertise which protocols it supports to the server as part
        of its initial connection handshake:
        ```
var ws = new WebSocket('wss://example.com/socket',
                       ['appProtocol', 'appProtocol-v2']); 
```
          
        
[ws.onopen = function () {
  if (ws.protocol == 'appProtocol-v2') {](#subproto) 
    [...
  } else {
    ...
  }
}](#proto)
`onopen` callback is fired on the client, and the
        application can query the `protocol` attribute on the
        WebSocket object to determine the chosen protocol. On the other hand,
        if the server does not support any of the client protocols advertised
        by the client, then the WebSocket handshake is incomplete: the
        `onerror` callback is invoked, and the connection is
        terminated.
        

## [§](#websocket-protocol)WebSocket Protocol

      The WebSocket wire protocol (RFC 6455) developed by the HyBi Working Group consists of two high-level components: the opening HTTP handshake used to negotiate the parameters of the connection and a binary message framing mechanism to allow for low overhead, message-based delivery of both text and binary data.

        The WebSocket Protocol attempts to address the goals of existing bidirectional HTTP technologies in the context of the existing HTTP infrastructure; as such, it is designed to work over HTTP ports 80 and 443… However, the design does not limit WebSocket to HTTP, and future implementations could use a simpler handshake over a dedicated port without reinventing the entire protocol.

WebSocket Protocol, RFC 6455

WebSocket protocol is a fully functional, standalone protocol that can
      be used outside the browser. Having said that, its primary application is
      as a bidirectional transport for browser-based applications.
       Client and server WebSocket applications communicate via a
        message-oriented API: the sender provides an arbitrary UTF-8 or binary
        payload, and the receiver is notified of its delivery when the entire
        message is available. To enable this, WebSocket uses a custom binary
        framing format ( The smallest unit of communication, each containing a
            variable-length frame header and a payload that may carry all or
            part of the application message.
           A complete sequence of frames that map to a logical application
            message.
         The decision to fragment an application message into multiple frames
        is made by the underlying implementation of the client and server
        framing code. Hence, the applications remain blissfully unaware of the
        individual WebSocket frames or how the framing is performed. Having
        said that, it is still useful to understand the highlights of how each
        WebSocket frame is represented on the wire:
         The first bit of each frame (FIN) indicates whether the frame is
            a final fragment of a message. A message may consist of just a
            single frame.
           The opcode (4 bits) indicates type of transferred frame: text
            (1) or binary (2) for transferring application data or a control
            frame such as connection close (8), ping (9), and pong (10) for
            connection liveness checks.
           The mask bit indicates whether the payload is masked (for
            messages sent from the client to the server only).
           Payload length is represented as a variable-length field:
             If 0–125, then that is the payload length.
               If 126, then the following 2 bytes represent a 16-bit
                unsigned integer indicating the frame length.
               If 127, then the following 8 bytes represent a 64-bit
                unsigned integer indicating the frame length.
             Masking key contains a 32-bit value used to mask the payload.
           Payload contains the application data and custom extension data
            if the client and server negotiated an extension when the
            connection was established.
         The payload of all client-initiated frames is  As a result, each server-sent WebSocket frame incurs 2–10 bytes of
        framing overhead. The client must also send a masking key, which adds
        an extra 4 bytes to the header, resulting in 6–14 bytes over overhead.
        No other metadata, such as header fields or other information about the
        payload, is available: all WebSocket communication is performed by
        exchanging frames that treat the payload as an opaque blob of
        application data.
        
       WebSocket specification allows for protocol extensions: the wire
        format and the semantics of the WebSocket protocol can be extended with
        new opcodes and data fields. While somewhat unusual, this is a very
        powerful feature, as it allows the client and server to implement
        additional functionality on top of the base WebSocket framing layer
        without requiring any intervention or cooperation from the application
        code.
         What are some examples of WebSocket protocol extensions? The HyBi
        Working Group, which is responsible for the development of the
        WebSocket specification, lists two official extensions in development:
         This extension provides a way for separate logical WebSocket
            connections to share an underlying transport connection.
           A framework for creating WebSocket extensions that add
            compression functionality to the WebSocket Protocol.
         As we noted earlier, each WebSocket connection requires a dedicated
        TCP connection, which is inefficient. Multiplexing extension addresses
        this problem by extending each WebSocket frame with an additional
        "channel ID" to allow multiple virtual WebSocket channels to share a
        single TCP connection.
         Similarly, the base WebSocket specification provides no mechanism or
        provisions for compression of transferred data: each frame carries
        payload data as provided by the application. As a result, while this
        may not be a problem for optimized binary data structures, this can
        result in high byte transfer overhead unless the application implements
        its own data compression and decompression logic. In effect,
        compression extension enables an equivalent of transfer-encoding
        negotiation provided by HTTP.
         To enable one or more extensions, the client must advertise them in
        the initial Upgrade handshake, and the server must select and
        acknowledge the extensions that will be used for the lifetime of the
        negotiated connection. For a hands-on example, let’s now take a closer
        look at the Upgrade sequence.
        
       The WebSocket protocol delivers a lot of powerful features:
        message-oriented communication, its own binary framing layer,
        subprotocol negotiation, optional protocol extensions, and more. As a
        result, before any messages can be exchanged, the client and server
        must negotiate the appropriate parameters to establish the connection.
         Leveraging HTTP to perform the handshake offers several advantages.
        First, it makes WebSockets compatible with existing HTTP
        infrastructure: WebSocket servers can run on port 80 and 443, which are
        frequently the only open ports for the client. Second, it allows us to
        reuse and extend the HTTP Upgrade flow with custom WebSocket headers to
        perform the negotiation:
         Sent by the client to indicate version ("13" for RFC6455) of the
            WebSocket protocol it wants to use. If the server does not support
            the client version, then it must reply with a list of supported
            versions.
           An auto-generated key sent by the client, which acts as a
            "challenge" to the server to prove that the server supports the
            requested version of the protocol.
           Server response that contains signed value of Sec-WebSocket-Key,
            proving that it understands the requested protocol version.
           Used to negotiate the application subprotocol: client advertises
            the list of supported protocols; server must reply with a single
            protocol name.
           Used to negotiate WebSocket extensions to be used for this
            connection: client advertises supported extensions, and the server
            confirms one or more extensions by returning the same header.
         With that, we now have all the necessary pieces to perform an HTTP
        Upgrade and negotiate a new WebSocket connection between the client and
        server:
         Just like any other client-initiated connection in the browser,
        WebSocket requests are subject to the same-origin policy: the browser
        automatically appends the Origin header to the upgrade handshake, and
        the remote server can use CORS to accept or deny the cross origin
        request; see  All RFC6455-compatible WebSocket servers use the same algorithm to
          compute the answer to the client challenge: the contents of the
           At a minimum, a successful WebSocket handshake must contain the
        protocol version and an auto-generated challenge value sent by the
        client, followed by a 101 HTTP response code (Switching Protocols) from
        the server with a hashed challenge-response to confirm the selected
        protocol version:
         Client must send  Server must confirm the protocol by returning
             Client may send a list of application subprotocols via
             Server must select one of the advertised subprotocols and return
            it via  Client may send a list of protocol extensions in
             Server may confirm one or more selected extensions via
             Finally, once the preceding handshake is complete, and if the
        handshake is successful, the connection can now be used as a two-way
        communication channel for exchanging WebSocket messages. From here on,
        there is no other explicit HTTP communication between the client and
        server, and the WebSocket protocol takes over.
        
      [§](#binary-framing-layer)Binary Framing Layer[Figure 17-1](#websocket-frame)), which splits each application
        message into one or more *frames*, transports them to the
        destination, reassembles them, and finally notifies the receiver once
        the entire message has been received.
        
        

*masked*
          using the value specified in the frame header: this prevents
          malicious scripts executing on the client from performing a cache
          poisoning attack against intermediaries that may not understand the
          WebSocket protocol. For full details of this attack, refer to
          ["Talking to
          Yourself for Fun and Proﬁt"](http://w2spconf.com/2011/papers/websocket.pdf), presented at W2SP 2011.
        [§](#protocol-extensions)Protocol Extensions

[§](#http-upgrade-negotiation)HTTP Upgrade Negotiation

`Sec-WebSocket-Version`
          `Sec-WebSocket-Key`
          `Sec-WebSocket-Accept`
          `Sec-WebSocket-Protocol`
          `Sec-WebSocket-Extensions`
          
GET /socket HTTP/1.1
Host: thirdparty.com
Origin: http://example.com
Connection: Upgrade
Upgrade: websocket 

          
        
[Sec-WebSocket-Version: 13](#wsupgrade) 
[Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==](#wsversion) 
[Sec-WebSocket-Protocol: appProtocol, appProtocol-v2](#wskey) 
[Sec-WebSocket-Extensions: x-webkit-deflate-message, x-custom-extension](#subprotocol) 
[Cross-Origin
        Resource Sharing (CORS)](/xmlhttprequest/#cross-origin-resource-sharing-cors). To complete the handshake, the server must
        return a successful "Switching Protocols" response and confirm the
        selected options advertised by the client:
        
HTTP/1.1 101 Switching Protocols 

          
        
[Upgrade: websocket
Connection: Upgrade
Access-Control-Allow-Origin: http://example.com](#upgraded) 
[Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=](#wsorigin) 
[Sec-WebSocket-Protocol: appProtocol-v2](#wsaccept) 
[Sec-WebSocket-Extensions: x-custom-extension](#wssp) 
`Sec-WebSocket-Key` are concatenated with a unique GUID
          string defined in the standard, a SHA1 hash is computed, and the
          resulting string is base-64 encoded and sent back to the client.
        

`Sec-WebSocket-Version` and
            `Sec-WebSocket-Key`.
          `Sec-WebSocket-Accept`.
          `Sec-WebSocket-Protocol`.
          `Sec-WebSocket-Protocol`. If the server does not
            support any, then the connection is aborted.
          `Sec-WebSocket-Extensions`.
          `Sec-WebSocket-Extensions`. If no extensions are
            provided, then the connection proceeds without them.
        

## [§](#websocket-use-cases-and-performance)WebSocket Use
      Cases and Performance

      WebSocket API provides a simple interface for bidirectional, message-oriented streaming of text and binary data between client and server: pass in a WebSocket URL to the constructor, set up a few JavaScript callback functions, and we are up and running—the rest is handled by the browser. Add to that the WebSocket protocol, which offers binary framing, extensibility, and subprotocol negotiation, and WebSocket becomes a perfect fit for delivering custom application protocols in the browser.

However, just as with any discussion on performance, while the implementation complexity of the WebSocket protocol is hidden from the application, it nonetheless has important performance implications for how and when WebSocket should be used. WebSocket is not a replacement for XHR or SSE, and for best performance it is critical that we leverage the strengths of each transport!

Refer to [XHR Use Cases and
        Performance](/xmlhttprequest/#xhr-use-cases-and-performance) and [SSE Use Cases
        and Performance](/server-sent-events-sse/#sse-use-cases-and-performance) for a review of the performance characteristics of
        each transport.
      

### [§](#request-and-response-streaming)Request and
        Response Streaming

        WebSocket is the only transport that allows bidirectional
        communication over the same TCP connection ([Figure 17-2](#transport-flow)): the client and server can
        exchange messages at will. As a result, WebSocket provides low latency
        delivery of text and binary application data in both directions.
        
        

- 
            XHR is optimized for "transactional" request-response communication: the client sends the full, well-formed HTTP request to the server, and the server responds with a full response. There is no support for request streaming, and until the Streams API is available, no reliable cross-browser response streaming API.
- 
            SSE enables efficient, low-latency server-to-client streaming of text-based data: the client initiates the SSE connection, and the server uses the event source protocol to stream updates to the client. The client can’t send any data to the server after the initial handshake.

### [§](#message-overhead)Message Overhead

        Once a WebSocket connection is established, the client and server exchange data via the WebSocket protocol: application messages are split into one or more frames, each of which adds from 2 to 14 bytes of overhead. Further, because the framing is done via a custom binary format, both UTF-8 and binary application data can be efficiently encoded via the same mechanism. How does that compare with XHR and SSE?

- 
            SSE adds as little as 5 bytes per message but is restricted to UTF-8 content only; see [Event Stream
            Protocol](/server-sent-events-sse/#event-stream-protocol) .
- 
            HTTP/1.x requests (XHR or otherwise) will carry an additional 500–800 bytes of HTTP metadata, plus cookies; see [Measuring
            and Controlling Protocol Overhead](/http1x/#measuring-and-controlling-protocol-overhead) .
- 
            HTTP/2 compresses the HTTP metadata, which significantly reduces the overhead; see [Header Compression](/http2/#header-compression) . In fact, if
            the headers do not change between requests, the overhead can be as
            low as 8 bytes!

Keep in mind that these overhead numbers do not include the
          overhead of IP, TCP, and TLS framing, which add 60–100 bytes of
          combined overhead per message, regardless of the application
          protocol; see [Optimize
          TLS Record Size](/transport-layer-security-tls/#optimize-tls-record-size).
        

### [§](#data-efficiency-and-compression)Data Efficiency
        and Compression

        Every XHR request can negotiate the optimal transfer encoding format (e.g., gzip for text-based data), via regular HTTP negotiation. Similarly, because SSE is restricted to UTF-8–only transfers, the event stream data can be efficiently compressed by applying gzip across the entire session.

With WebSocket, the situation is more complex: WebSocket can transfer both text and binary data, and as a result it doesn’t make sense to compress the entire session. The binary payloads may be compressed already! As a result, WebSocket must implement its own compression mechanism and selectively apply it to each message.

The good news is the HyBi working group is developing the
        per-message compression extension for the WebSocket protocol. However,
        it is not yet available in any of the browsers. As a result, unless the
        application implements its own compression logic by carefully
        optimizing its binary payloads (see [Decoding Binary Data with
        JavaScript](#decoding-binary-data-with-javascript)) and implementing its own compression logic for
        text-based messages, it may incur high byte overhead on the transferred
        data!
        

Chrome and some WebKit-based browsers support an older revision
          (per-frame compression) of the compression extension to the WebSocket
          protocol; see [WebSocket
          Multiplexing and Compression in the Wild](#websocket-multiplexing-and-compression-in-the-wild).
        

### [§](#custom-application-protocols)Custom Application
        Protocols

        The browser is optimized for HTTP data transfers: it understands the protocol, and it provides a wide array of services, such as authentication, caching, compression, and much more. As a result, XHR requests inherit all of this functionality for free.

By contrast, streaming allows us to deliver custom protocols between client and server, but at the cost of bypassing many of the services provided by the browser: the initial HTTP handshake may be able to perform some negotiation of the parameters of the connection, but once the session is established, all further data streamed between the client and server is opaque to the browser. As a result, the flexibility of delivering a custom protocol also has its downsides, and the application may have to implement its own logic to fill in the missing gaps: caching, state management, delivery of message metadata, and so on!

The initial HTTP Upgrade handshake does allow the server to leverage the existing HTTP cookie mechanism to validate the user. If the validation fails, the server can decline the WebSocket upgrade.

### [§](#deploying-websocket-infrastructure)Deploying
        WebSocket Infrastructure

        HTTP is optimized for short and bursty transfers. As a result, many of the servers, proxies, and other intermediaries are often configured to aggressively timeout idle HTTP connections, which, of course, is exactly what we don’t want to see for long-lived WebSocket sessions. To address this, there are three pieces to consider:

- 
            Routers, load-balancers, and proxies within own network
- 
            Transparent and explicit proxies in external network (e.g., ISP and carrier proxies)
- 
            Routers, firewalls, and proxies within the client’s network

We have no control over the policy of the client’s network. In fact, some networks may block WebSocket traffic entirely, which is why you may need a fallback strategy. Similarly, we don’t have control over the proxies on the external network. However, this is where TLS may help! By tunneling over a secure end-to-end connection, WebSocket traffic can bypass all the intermediate proxies.

Using TLS does not prevent the intermediary from timing out an idle TCP connection. However, in practice, it significantly increases the success rate of negotiating the WebSocket session and often also helps to extend the connection timeout intervals.

Finally, there is the infrastructure that we deploy and manage ourselves, which also often requires attention and tuning. As easy as it is to blame the client or external networks, all too often the problem is close to home. Each load-balancer, router, proxy, and web server in the serving path must be tuned to allow long-lived connections.

For example, Nginx 1.3.13+ can proxy WebSocket traffic, but defaults to aggressive 60-second timeouts! To increase the limit, we must explicitly define the longer timeouts:

```
location /websocket {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600; 
```
          
        Similarly, it is not uncommon to have a load balancer, such as HAProxy, in front of one or more Nginx servers. Not surprisingly, we need to apply similar explicit configuration here as well—e.g., for HAProxy:

The gotcha with the preceding example is the extra "tunnel" timeout.
        In HAProxy the `connect`, `client`, and
        `server` timeouts are applied only to the initial HTTP
        Upgrade handshake, but once the upgrade is complete, the timeout is
        controlled by the `tunnel` value.
        

Nginx and HAProxy are just two of hundreds of different servers, proxies, and load balancers running in our data centers. We can’t enumerate all the configuration possibilities in these pages. The previous examples are just an illustration that most infrastructure requires custom configuration to handle long-lived sessions. Hence, before implementing application keepalives, double-check your infrastructure first.

Long-lived and idle sessions occupy memory and socket resources on all the intermediate servers. Hence, short timeouts are often justified as a security, resource, and operational precaution. Deploying WebSocket, SSE, and HTTP/2, each of which relies on long-lived sessions, brings its own class of new operational challenges.

## [§](#performance-checklist)Performance Checklist

      Deploying a high-performance WebSocket service requires careful tuning and consideration, both on the client and on the server. A short list of criteria to put on the agenda:

- 
          Use secure WebSocket (WSS over TLS) for reliable deployments.
- 
          Pay close attention to polyfill performance (if necessary).
- 
          Leverage subprotocol negotiation to determine the application protocol.
- 
          Optimize binary payloads to minimize transfer size.
- 
          Consider compressing UTF-8 content to minimize transfer size.
- 
          Set the right binary type for received binary payloads.
- 
          Monitor the amount of buffered data on the client.
- 
          Split large application messages to avoid head-of-line blocking.
- 
          Leverage other transports where applicable.

Last, but definitely not least, optimize for mobile! Real-time push can be a costly performance anti-pattern on mobile handsets, where battery life is always at a premium. That’s not to say that WebSocket should not be used on mobile. To the contrary, it can be a highly efficient transport, but make sure to account for its requirements:
