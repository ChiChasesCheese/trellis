---
title: 'RFC 8656: Traversal Using Relays around NAT (TURN): Relay Extensions to Session
  Traversal Utilities for NAT (STUN) | RFC Editor'
source: https://www.rfc-editor.org/rfc/rfc8656
author: T Reddy; A Johnston; P Matthews; J Rosenberg
published: '2020-02-21'
site: rfc-editor.org
clipped: '2026-09-20'
---

# RFC 8656: Traversal Using Relays around NAT (TURN): Relay Extensions to Session Traversal Utilities for NAT (STUN) | RFC Editor

- [Home](/)
- **RFC 8656**

# RFC 8656:      Traversal Using Relays around NAT (TURN): Relay Extensions to Session Traversal Utilities for NAT (STUN) 

- T. Reddy, Ed.,
- A. Johnston, Ed.,
- P. Matthews,
- J. Rosenberg

## [Abstract](#abstract)

If a host is located behind a NAT, it can be impossible for that host
      to communicate directly with other hosts (peers) in certain
      situations. In these situations, it is necessary for the host to use the
      services of an intermediate node that acts as a communication relay.
      This specification defines a protocol, called "Traversal Using Relays
      around NAT" (TURN), that allows the host to control the operation of the
      relay and to exchange packets with its peers using the relay. TURN
      differs from other relay control protocols in that it allows a client to
      communicate with multiple peers using a single relay address.[¶](#section-abstract-1)

The TURN protocol was designed to be used as part of the Interactive
      Connectivity Establishment (ICE) approach to NAT traversal,
      though it can also be used without ICE.[¶](#section-abstract-2)

This document obsoletes RFCs 5766 and 6156.[¶](#section-abstract-3)

## 
[Status of This Memo](#name-status-of-this-memo)
        

            This is an Internet Standards Track document.[¶](#section-boilerplate.1-1)

            This document is a product of the Internet Engineering Task Force
            (IETF).  It represents the consensus of the IETF community.  It has
            received public review and has been approved for publication by
            the Internet Engineering Steering Group (IESG).  Further
            information on Internet Standards is available in Section 2 of 
            RFC 7841.[¶](#section-boilerplate.1-2)

            Information about the current status of this document, any
            errata, and how to provide feedback on it may be obtained at
            [https://](/info/rfc8656).[¶](#section-boilerplate.1-3)

## 
[Copyright Notice](#name-copyright-notice)
        

            Copyright (c) 2020 IETF Trust and the persons identified as the
            document authors. All rights reserved.[¶](#section-boilerplate.2-1)

            This document is subject to BCP 78 and the IETF Trust's Legal
            Provisions Relating to IETF Documents
            ([https://](https://trustee.ietf.org/license-info)) in effect on the date of
            publication of this document. Please review these documents
            carefully, as they describe your rights and restrictions with
            respect to this document. Code Components extracted from this
            document must include Simplified BSD License text as described in
            Section 4.e of the Trust Legal Provisions and are provided without
            warranty as described in the Simplified BSD License.[¶](#section-boilerplate.2-2)

## 
[1.](#section-1) [Introduction](#name-introduction)
      

A host behind a NAT may wish to exchange packets with other hosts,
      some of which may also be behind NATs. To do this, the hosts involved
      can use "hole punching" techniques (see [[RFC5128](#RFC5128)])
      in an attempt to discover a direct communication path; that is, a
      communication path that goes from one host to another through
      intervening NATs and routers but does not traverse any relays.[¶](#section-1-1)

As described in [[RFC5128](#RFC5128)] and [[RFC4787](#RFC4787)], hole punching techniques will fail
      if both hosts are behind NATs that are not well behaved. For example, if
      both hosts are behind NATs that have a mapping behavior of
      "address-[Section 4.1](/info/rfc4787/#section-4.1) of [[RFC4787](#RFC4787)]), then
      hole punching techniques generally fail.[¶](#section-1-2)

When a direct communication path cannot be found, it is necessary to
      use the services of an intermediate host that acts as a relay for the
      packets. This relay typically sits in the public Internet and relays
      packets between two hosts that both sit behind NATs.[¶](#section-1-3)

In many enterprise networks, direct UDP transmissions are not
      permitted between clients on the internal networks and external IP
      addresses. To permit media sessions in such a situation to use UDP and
      avoid forcing them through TCP, an Enterprise Firewall can be configured
      to allow UDP traffic relayed through an Enterprise relay server. WebRTC
      requires support for this scenario (see [Section 2.3.5.1](/info/rfc7478/#section-2.3.5.1) of [[RFC7478](#RFC7478)]). Some users of SIP or WebRTC
      want IP location privacy from the remote peer. In this scenario, the
      client can select a relay server offering IP location privacy and only
      convey the relayed candidates to the peer for ICE connectivity checks
      (see [Section 4.2.4](https://tools.ietf.org/html/draft-ietf-rtcweb-security-12#section-4.2.4) of [[SEC-WEBRTC](#I-D.ietf-rtcweb-security)]).[¶](#section-1-4)

This specification defines a protocol, called "TURN", that allows a
      host behind a NAT (called the "TURN client") to request that another host
      (called the "TURN server") act as a relay.
      The client can arrange for the server to relay packets to and from
      certain other hosts (called "peers"), and the client can control aspects
      of how the relaying is done. The client does this by obtaining an IP
      address and port on the server, called the "relayed transport
      address". When a peer sends a packet to the relayed transport address,
      the server relays the transport protocol data from the packet to the
      client. The data encapsulated within a message header that allows the
      client to know the peer from which the transport protocol data was
      relayed by the server.
      If the server receives an ICMP error packet, the server also relays
      certain Layer 3 and 4 header fields from the ICMP header to the
      client. When the client sends a message to the server, the server
      identifies the remote peer from the message header and relays the
      message data to the intended peer.[¶](#section-1-5)

A client using TURN must have some way to communicate the relayed
      transport address to its peers and to learn each peer's IP address and
      port (more precisely, each peer's server-[Section 3](#sec-overview)). How this is done is out of the
      scope of the TURN protocol. One way this might be done is for the client
      and peers to exchange email messages. Another way is for the client and
      its peers to use a special-[RFC5128](#RFC5128)] for more details).[¶](#section-1-6)

If TURN is used with ICE [[RFC8445](#RFC8445)],
      then the relayed transport address and the IP addresses and ports of the
      peers are included in the ICE candidate information that the rendezvous
      protocol must carry. For example, if TURN and ICE are used as part of a
      multimedia solution using SIP [[RFC3261](#RFC3261)],
      then SIP serves the role of the rendezvous protocol, carrying the ICE
      candidate information inside the body of SIP messages [[SDP-ICE](#I-D.ietf-mmusic-ice-sip-sdp)]. If TURN and ICE are used with some
      other rendezvous protocol, then ICE provides guidance on the services
      the rendezvous protocol must perform.[¶](#section-1-7)

Though the use of a TURN server to enable communication between two
      hosts behind NATs is very likely to work, it comes at a high cost to the
      provider of the TURN server since the server typically needs a
      high-bandwidth connection to the Internet. As a consequence, it is best
      to use a TURN server only when a direct communication path cannot be
      found. When the client and a peer use ICE to determine the communication
      path, ICE will use hole punching techniques to search for a direct path
      first and only use a TURN server when a direct path cannot be found.[¶](#section-1-8)

TURN was originally invented to support multimedia sessions signaled
      using SIP. Since SIP supports forking, TURN supports multiple peers per
      relayed transport address; a feature not supported by other approaches
      (e.g., SOCKS [[RFC1928](#RFC1928)]). However, care has been
      taken to make sure that TURN is suitable for other types of
      applications.[¶](#section-1-9)

TURN was designed as one piece in the larger ICE approach to NAT
      traversal. Implementors of TURN are urged to investigate ICE and
      seriously consider using it for their application. However, it is
      possible to use TURN without ICE.[¶](#section-1-10)

TURN is an extension to the Session Traversal Utilities for NAT
      (STUN) protocol [[RFC8489](#RFC8489)]. Most, though
      not all, TURN messages are STUN-formatted messages. A reader of this
      document should be familiar with STUN.[¶](#section-1-11)

The TURN specification was originally published as [[RFC5766](#RFC5766)], which was updated by [[RFC6156](#RFC6156)] to add IPv6 support. This document supersedes
      and obsoletes both [[RFC5766](#RFC5766)] and [[RFC6156](#RFC6156)].[¶](#section-1-12)

## 
[2.](#section-2) [Terminology](#name-terminology)
      

    The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED",
    "MAY", and "OPTIONAL" in this document are to be interpreted as
    described in BCP 14 [[RFC2119](#RFC2119)] [[RFC8174](#RFC8174)] 
    when, and only when, they appear in all capitals, as shown here.[¶](#section-2-1)

Readers are expected to be familiar with [[RFC8489](#RFC8489)] and the terms defined there.[¶](#section-2-2)

The following terms are used in this document:[¶](#section-2-3)

- TURN:
- The protocol spoken between a TURN client and a
          TURN server. It is an extension to the STUN protocol [[RFC8489](#RFC8489) ]. The protocol allows a client
          to allocate and use a relayed transport address.[¶](#section-2-4.2)
- TURN client:
- A STUN client that implements this
          specification.[¶](#section-2-4.4)
- TURN server:
- A STUN server that implements this
          specification. It relays data between a TURN client and its
          peer(s).[¶](#section-2-4.6)
- Peer:
- A host with which the TURN client wishes to
          communicate. The TURN server relays traffic between the TURN client
          and its peer(s). The peer does not interact with the TURN server
          using the protocol defined in this document; rather, the peer
          receives data sent by the TURN server, and the peer sends data
          towards the TURN server.[¶](#section-2-4.8)
- Transport Address:
- The combination of an IP address
          and a port.[¶](#section-2-4.10)
- Host Transport Address:
- A transport address on a
          client or a peer.[¶](#section-2-4.12)
- Server-Reflexive Transport Address:
- A transport
          address on the "external side" of a NAT. This address is allocated
          by the NAT to correspond to a specific host transport address.[¶](#section-2-4.14)
- Relayed Transport Address:
- A transport address on the
          TURN server that is used for relaying packets between the client and
          a peer. A peer sends to this address on the TURN server, and the
          packet is then relayed to the client.[¶](#section-2-4.16)
- TURN Server Transport Address:
- A transport address on
          the TURN server that is used for sending TURN messages to the
          server. This is the transport address that the client uses to
          communicate with the server.[¶](#section-2-4.18)
- Peer Transport Address:
- The transport address of the
          peer as seen by the server. When the peer is behind a NAT, this is
          the peer's server-reflexive transport address. [¶](#section-2-4.20)
- Allocation:
- The relayed transport address granted to a
          client through an Allocate request, along with related state, such
          as permissions and expiration timers.[¶](#section-2-4.22)
- 5-tuple:
- The combination (client IP address and port, server IP address and
        port, and transport protocol (currently one of UDP, TCP, DTLS/UDP, or
        TLS/TCP)) used to communicate between the client and the server. The
        5-tuple uniquely identifies this communication stream. The 5-tuple
        also uniquely identifies the Allocation on the server.[¶](#section-2-4.24)
- Transport Protocol:
- The protocol above IP that carries TURN Requests, Responses, and
        Indications as well as providing identifiable flows using a
        5-tuple. In this specification, UDP and TCP are defined as transport
        protocols; this document also describes the use of UDP and TCP in
        combination with a security layer using DTLS and TLS,
        respectively.[¶](#section-2-4.26)
- Channel:
- A channel number and associated peer
          transport address. Once a channel number is bound to a peer's
          transport address, the client and server can use the more
          bandwidth-efficient ChannelData message to exchange data. [¶](#section-2-4.28)
- Permission:
- The IP address and transport protocol (but
          not the port) of a peer that is permitted to send traffic to the
          TURN server and have that traffic relayed to the TURN client. The
          TURN server will only forward traffic to its client from peers that
          match an existing permission.[¶](#section-2-4.30)
- Realm:
- A string used to describe the server or a
          context within the server. The realm tells the client which username
          and password combination to use to authenticate requests.[¶](#section-2-4.32)
- Nonce:
- A string chosen at random by the server and
          included in the server response. To prevent replay attacks, the
          server should change the nonce regularly.[¶](#section-2-4.34)
- (D)TLS:
- This term is used for statements that apply to
          both Transport Layer Security [[RFC8446](#RFC8446) ] and
          Datagram Transport Layer Security [[RFC6347](#RFC6347) ].[¶](#section-2-4.36)

## 
[3.](#section-3) [Overview of Operation](#name-overview-of-operation)
      

This section gives an overview of the operation of TURN. It is
      non-normative.[¶](#section-3-1)

In a typical configuration, a TURN client is connected to a private
      network [[RFC1918](#RFC1918)] and, through one or more
      NATs, to the public Internet. On the public Internet is a TURN
      server. Elsewhere in the Internet are one or more peers with which the
      TURN client wishes to communicate. These peers may or may not be behind
      one or more NATs.  The client uses the server as a relay to send packets
      to these peers and to receive packets from these peers.[¶](#section-3-2)

[Figure 1](#fig-turn-model) shows a typical deployment. In
      this figure, the TURN client and the TURN server are separated by a NAT,
      with the client on the private side and the server on the public side of
      the NAT. This NAT is assumed to be a "bad" NAT; for example,
      it might have a mapping property of "address-[RFC4787](#RFC4787)]).[¶](#section-3-4)

The client talks to the server from a (IP address, port) combination
      called the client's "host transport address". (The combination of an IP
      address and port is called a "transport address".)[¶](#section-3-5)

The client sends TURN messages from its host transport address to a
      transport address on the TURN server that is known as the "TURN server
      transport address". The client learns the TURN server transport address
      through some unspecified means (e.g., configuration), and this address
      is typically used by many clients simultaneously.[¶](#section-3-6)

Since the client is behind a NAT, the server sees packets from the
      client as coming from a transport address on the NAT itself. This
      address is known as the client's "server-[¶](#section-3-7)

The client uses TURN commands to create and manipulate an ALLOCATION
      on the server. An allocation is a data structure on the server. This
      data structure contains, amongst other things, the relayed transport
      address for the allocation. The relayed transport address is the
      transport address on the server that peers can use to have the server
      relay data to the client. An allocation is uniquely identified by its
      relayed transport address.[¶](#section-3-8)

Once an allocation is created, the client can send application data
      to the server along with an indication of to which peer the data is to
      be sent, and the server will relay this data to the intended peer. The
      client sends the application data to the server inside a TURN message;
      at the server, the data is extracted from the TURN message and sent to
      the peer in a UDP datagram. In the reverse direction, a peer can send
      application data in a UDP datagram to the relayed transport address for
      the allocation; the server will then encapsulate this data inside a TURN
      message and send it to the client along with an indication of which peer
      sent the data. Since the TURN message always contains an indication of
      which peer the client is communicating with, the client can use a single
      allocation to communicate with multiple peers.[¶](#section-3-9)

When the peer is behind a NAT, the client must identify the peer
      using its server-[¶](#section-3-10)

Each allocation on the server belongs to a single client and has
      either one or two relayed transport addresses that are used only by that
      allocation. Thus, when a packet arrives at a relayed transport address
      on the server, the server knows for which client the data is
      intended.[¶](#section-3-11)

The client may have multiple allocations on a server at the same
      time.[¶](#section-3-12)

### 
[3.1.](#section-3.1) [Transports](#name-transports)
        

TURN, as defined in this specification, always uses UDP between the
        server and the peer. However, this specification allows the use of any
        one of UDP, TCP, Transport Layer Security (TLS) over TCP, or Datagram
        Transport Layer Security (DTLS) over UDP to carry the TURN messages
        between the client and the server.[¶](#section-3.1-1)

| Table 1 |  | 
|---|---|
| TURN client to TURN server | TURN server to peer | 
|---|---|
| UDP | UDP | 
| TCP | UDP | 
| TLS-over-TCP | UDP | 
| DTLS-over-UDP | UDP | 

[Table 1](#table-1)

If TCP or TLS-over-TCP is used between the client and the server,
        then the server will convert between these transports and UDP
        transport when relaying data to/from the peer.[¶](#section-3.1-3)

Since this version of TURN only supports UDP between the server and
        the peer, it is expected that most clients will prefer to use UDP
        between the client and the server as well. That being the case, some
        readers may wonder: Why also support TCP and TLS-over-TCP?[¶](#section-3.1-4)

TURN supports TCP transport between the client and the server
        because some firewalls are configured to block UDP entirely. These
        firewalls block UDP but not TCP, in part because TCP has properties
        that make the intention of the nodes being protected by the firewall
        more obvious to the firewall. For example, TCP has a three-way
        handshake that makes it clearer that the protected node really wishes
        to have that particular connection established, while for UDP, the best
        the firewall can do is guess which flows are desired by using
        filtering rules. Also, TCP has explicit connection teardown; while for
        UDP, the firewall has to use timers to guess when the flow is
        finished.[¶](#section-3.1-5)

TURN supports TLS-over-TCP transport and DTLS-over-UDP transport
        between the client and the server because (D)TLS provides additional
        security properties not provided by TURN's default digest
        authentication, properties that some clients may wish to take
        advantage of. In particular, (D)TLS provides a way for the client to
        ascertain that it is talking to the correct server and provides for
        confidentiality of TURN control messages. 
If (D)TLS transport is used between the TURN client and the TURN server, refer
to [Section 6.2.3](/info/rfc8489/#section-6.2.3) of [[RFC8489](#RFC8489)] for more
information about cipher suites, server certificate validation, and
authentication of TURN servers.
The guidance given in [[RFC7525](#RFC7525)]
          MUST be followed to avoid attacks on (D)TLS. TURN does not
require (D)TLS because the overhead of using (D)TLS is higher than that of
digest authentication; for example, using (D)TLS likely means that most
application data will be doubly encrypted (once by (D)TLS and once to ensure
it is still encrypted in the UDP datagram).[¶](#section-3.1-6)

There is an extension to TURN for TCP transport between the server
        and the peers [[RFC6062](#RFC6062)]. For this
        reason, allocations that use UDP between the server and the peers are
        known as "UDP allocations", while allocations that use TCP between the
        server and the peers are known as "TCP allocations". This specification
        describes only UDP allocations.[¶](#section-3.1-7)

In some applications for TURN, the client may send and receive
        packets other than TURN packets on the host transport address it uses
        to communicate with the server. This can happen, for example, when
        using TURN with ICE. In these cases, the client can distinguish TURN
        packets from other packets by examining the source address of the
        arriving packet; those arriving from the TURN server will be TURN
        packets. The algorithm of demultiplexing packets received from
        multiple protocols on the host transport address is discussed in [[RFC7983](#RFC7983)].[¶](#section-3.1-8)

### 
[3.2.](#section-3.2) [Allocations](#name-allocations)
        

To create an allocation on the server, the client uses an Allocate
        transaction. The client sends an Allocate request to the server, and
        the server replies with an Allocate success response containing the
        allocated relayed transport address. The client can include attributes
        in the Allocate request that describe the type of allocation it
        desires (e.g., the lifetime of the allocation). Since relaying data
        has security implications, the server requires that the client
        authenticate itself, typically using STUN's long-term credential
        mechanism or the STUN Extension for Third-Party Authorization [[RFC7635](#RFC7635)], to show that it is authorized to use the
        server.[¶](#section-3.2-1)

Once a relayed transport address is allocated, a client must keep
        the allocation alive. To do this, the client periodically sends a
        Refresh request to the server. TURN deliberately uses a different
        method (Refresh rather than Allocate) for refreshes to ensure that the
        client is informed if the allocation vanishes for some reason.[¶](#section-3.2-2)

The frequency of the Refresh transaction is determined by the
        lifetime of the allocation. The default lifetime of an allocation is
        10 minutes; this value was chosen to be long enough so that
        refreshing is not typically a burden on the client while expiring
        allocations where the client has unexpectedly quit in a timely manner.
        However, the client can request a longer lifetime in the Allocate
        request and may modify its request in a Refresh request, and the
        server always indicates the actual lifetime in the response. The
        client must issue a new Refresh transaction within "lifetime" seconds
        of the previous Allocate or Refresh transaction. Once a client no
        longer wishes to use an allocation, it should delete the allocation
        using a Refresh request with a requested lifetime of zero.[¶](#section-3.2-3)

Both the server and client keep track of a value known as the
        "5-tuple". At the client, the 5-tuple consists of the client's host
        transport address, the server transport address, and the transport
        protocol used by the client to communicate with the server. At the
        server, the 5-tuple value is the same except that the client's host
        transport address is replaced by the client's server-[¶](#section-3.2-4)

Both the client and the server remember the 5-tuple used in the
        Allocate request. Subsequent messages between the client and the
        server use the same 5-tuple. In this way, the client and server know
        which allocation is being referred to. If the client wishes to
        allocate a second relayed transport address, it must create a second
        allocation using a different 5-tuple (e.g., by using a different
        client host address or port).[¶](#section-3.2-5)

In [Figure 2](#fig-allocate), the client sends an
        Allocate request to the server with invalid or missing credentials.
        Since the server requires that all requests be authenticated using
        STUN's long-term credential mechanism, the server rejects the request
        with a 401 (Unauthorized) error code. The client then tries again,
        this time including credentials. This time, the server accepts the
        Allocate request and returns an Allocate success response containing
        (amongst other things) the relayed transport address assigned to the
        allocation. Sometime later, the client decides to refresh the
        allocation; thus, it sends a Refresh request to the server. The refresh
        is accepted and the server replies with a Refresh success
        response.[¶](#section-3.2-8)

### 
[3.3.](#section-3.3) [Permissions](#name-permissions)
        

To ease concerns amongst enterprise IT administrators that TURN
        could be used to bypass corporate firewall security, TURN includes the
        notion of permissions. TURN permissions mimic the address-[RFC4787](#RFC4787)].[¶](#section-3.3-1)

An allocation can have zero or more permissions. Each permission
        consists of an IP address and a lifetime. When the server receives a
        UDP datagram on the allocation's relayed transport address, it first
        checks the list of permissions. If the source IP address of the
        datagram matches a permission, the application data is relayed to the
        client; otherwise, the UDP datagram is silently discarded.[¶](#section-3.3-2)

A permission expires after 5 minutes if it is not refreshed, and
        there is no way to explicitly delete a permission. This behavior was
        selected to match the behavior of a NAT that complies with [[RFC4787](#RFC4787)].[¶](#section-3.3-3)

The client can install or refresh a permission using either a
        Create[¶](#section-3.3-4)

Note that permissions are within the context of an allocation, so
        adding or expiring a permission in one allocation does not affect
        other allocations.[¶](#section-3.3-5)

### 
[3.4.](#section-3.4) [Send Mechanism](#name-send-mechanism)
        

There are two mechanisms for the client and peers to exchange
        application data using the TURN server. The first mechanism uses the
        Send and Data methods, the second mechanism uses channels. Common to
        both mechanisms is the ability of the client to communicate with
        multiple peers using a single allocated relayed transport address;
        thus, both mechanisms include a means for the client to indicate to
        the server which peer should receive the data and for the server to
        indicate to the client which peer sent the data.[¶](#section-3.4-1)

The Send mechanism uses Send and Data indications. Send indications
        are used to send application data from the client to the server, while
        Data indications are used to send application data from the server to
        the client.[¶](#section-3.4-2)

When using the Send mechanism, the client sends a Send indication
        to the TURN server containing (a) an XOR-[¶](#section-3.4-3)

In the reverse direction, UDP datagrams arriving at the relayed
        transport address on the TURN server are converted into Data
        indications and sent to the client, with the server-[¶](#section-3.4-4)

Some ICMP (Internet Control Message Protocol) packets arriving at
        the relayed transport address on the TURN server may be converted into
        Data indications and sent to the client, with the transport address of
        the peer included in an XOR-[¶](#section-3.4-5)

Send and Data indications cannot be authenticated since the
        long-term credential mechanism of STUN does not support authenticating
        indications. This is not as big an issue as it might first appear
        since the client-[¶](#section-3.4-6)

Because Send indications are not authenticated, it is possible for
        an attacker to send bogus Send indications to the server, which will
        then relay these to a peer. To partly mitigate this attack, TURN
        requires that the client install a permission towards a peer before
        sending data to it using a Send indication. The technique to fully
        mitigate the attack is discussed in [Section 21.1.4](#fate-data).[¶](#section-3.4-7)

In [Figure 3](#fig-send-data), the client has already
        created an allocation and now wishes to send data to its peers. The
        client first creates a permission by sending the server a
        Create[¶](#section-3.4-9)

### 
[3.5.](#section-3.5) [Channels](#name-channels)
        

For some applications (e.g., Voice over IP (VoIP)), the 36 bytes of
        overhead that a Send indication or Data indication adds to the
        application data can substantially increase the bandwidth required
        between the client and the server. To remedy this, TURN offers a
        second way for the client and server to associate data with a specific
        peer.[¶](#section-3.5-1)

This second way uses an alternate packet format known as the
        "ChannelData message". The ChannelData message does not use the STUN
        header used by other TURN messages, but instead has a 4-byte header
        that includes a number known as a "channel number". Each channel number
        in use is bound to a specific peer; thus, it serves as a shorthand for
        the peer's host transport address.[¶](#section-3.5-2)

To bind a channel to a peer, the client sends a ChannelBind request
        to the server and includes an unbound channel number and the
        transport address of the peer. Once the channel is bound, the client
        can use a ChannelData message to send the server data destined for the
        peer. Similarly, the server can relay data from that peer towards the
        client using a ChannelData message.[¶](#section-3.5-3)

Channel bindings last for 10 minutes unless refreshed; this
        lifetime was chosen to be longer than the permission lifetime. Channel
        bindings are refreshed by sending another ChannelBind request
        rebinding the channel to the peer. Like permissions (but unlike
        allocations), there is no way to explicitly delete a channel binding;
        the client must simply wait for it to time out.[¶](#section-3.5-4)

[Figure 4](#fig-channels) shows the channel mechanism in
        use. The client has already created an allocation and now wishes to
        bind a channel to Peer A. To do this, the client sends a ChannelBind
        request to the server, specifying the transport address of Peer A and
        a channel number (0x4001). After that, the client can send application
        data encapsulated inside ChannelData messages to Peer A: this is shown
        as "(0x4001) data" where 0x4001 is the channel number. When the
        ChannelData message arrives at the server, the server transfers the
        data to a UDP datagram and sends it to Peer A (which is the peer bound
        to channel number 0x4001).[¶](#section-3.5-6)

In the reverse direction, when Peer A sends a UDP datagram to the
        relayed transport address, this UDP datagram arrives at the server on
        the relayed transport address assigned to the allocation. Since the
        UDP datagram was received from Peer A, which has a channel number
        assigned to it, the server encapsulates the data into a ChannelData
        message when sending the data to the client.[¶](#section-3.5-7)

Once a channel has been bound, the client is free to intermix
        ChannelData messages and Send indications. In the figure, the client
        later decides to use a Send indication rather than a ChannelData
        message to send additional data to Peer A. The client might decide to
        do this, for example, so it can use the DONT-FRAGMENT attribute (see
        the next section). However, once a channel is bound, the server will
        always use a ChannelData message, as shown in the call flow.[¶](#section-3.5-8)

Note that ChannelData messages can only be used for peers to which
        the client has bound a channel. In the example above, Peer A has been
        bound to a channel, but Peer B has not, so application data to and
        from Peer B would use the Send mechanism.[¶](#section-3.5-9)

### 
[3.6.](#section-3.6) [Unprivileged TURN Servers](#name-unprivileged-turn-servers)
        

This version of TURN is designed so that the server can be
        implemented as an application that runs in user space under commonly
        available operating systems without requiring special privileges. This
        design decision was made to make it easy to deploy a TURN server: for
        example, to allow a TURN server to be integrated into a peer-to-peer
        application so that one peer can offer NAT traversal services to
        another peer and to use (D)TLS to secure the TURN connection.[¶](#section-3.6-1)

This design decision has the following implications for data
        relayed by a TURN server:[¶](#section-3.6-2)

- The value of the Diffserv field may not be preserved across the
            server;[¶](#section-3.6-3.1)
- The Time to Live (TTL) field may be reset, rather than
            decremented, across the server;[¶](#section-3.6-3.2)
- The Explicit Congestion Notification (ECN) field may be reset
            by the server;[¶](#section-3.6-3.3)
- There is no end-to-end fragmentation since the packet is
            reassembled at the server.[¶](#section-3.6-3.4)

Future work may specify alternate TURN semantics that address
        these limitations.[¶](#section-3.6-4)

### 
[3.7.](#section-3.7) [Avoiding IP Fragmentation](#name-avoiding-ip-fragmentation)
        

For reasons described in [[FRAG-HARMFUL](#FRAG-HARMFUL)], applications, especially those sending large
        volumes of data, should avoid having their packets fragmented. [[FRAG-FRAGILE](#I-D.ietf-intarea-frag-fragile)] discusses issues associated
        with IP fragmentation and proposes alternatives to IP
        fragmentation.
 Applications using TCP can, more or less, ignore this
        issue because fragmentation avoidance is now a standard part of TCP,
        but applications using UDP (and, thus, any application using this
        version of TURN) need to avoid IP fragmentation by sending
        sufficiently small messages or by using UDP fragmentation [[UDP-OPT](#I-D.ietf-tsvwg-udp-options)]. Note that the UDP
        fragmentation option needs to be supported by both endpoints, and at
        the time of writing of this document, UDP fragmentation support is
        under discussion and is not deployed.[¶](#section-3.7-1)

The application running on the client and the peer can take one of
        two approaches to avoid IP fragmentation until UDP fragmentation
        support is available. The first uses messages that are limited to a
        predetermined fixed maximum, and the second relies on network feedback
        to adapt that maximum.[¶](#section-3.7-2)

The first approach is to avoid sending large amounts of application
        data in the TURN messages/UDP datagrams exchanged between the client
        and the peer. This is the approach taken by most VoIP 
        applications. In this approach, the application MUST
        assume a Path MTU (PMTU) of 1280 bytes because IPv6 requires that every
        link in the Internet has an MTU of 1280 octets or greater as
        specified in [[RFC8200](#RFC8200)]. If IPv4
        support on legacy or otherwise unusual networks is a consideration,
        the application MAY assume an effective MTU of 576
        bytes for IPv4 datagrams, as every IPv4 host must be capable of
        receiving a packet with a length equal to 576 bytes as discussed in
        [[RFC0791](#RFC0791)] and [[RFC1122](#RFC1122)].[¶](#section-3.7-3)

The exact amount of application data that can be included while
        avoiding fragmentation depends on the details of the TURN session
        between the client and the server: whether UDP, TCP, or (D)TLS
        transport is used; whether ChannelData messages or Send/Data
        indications are used; and whether any additional attributes (such as
        the DONT-FRAGMENT attribute) are included. Another factor, which is
        hard to determine, is whether the MTU is reduced somewhere along the
        path for other reasons, such as the use of IP-in-IP tunneling.[¶](#section-3.7-4)

As a guideline, sending a maximum of 500 bytes of application data
        in a single TURN message (by the client on the client-[¶](#section-3.7-5)

The second approach the client and peer can take to avoid
        fragmentation is to use a path MTU discovery algorithm to determine
        the maximum amount of application data that can be sent without
        fragmentation. The classic path MTU discovery algorithm defined in
        [[RFC1191](#RFC1191)] may not be able to discover the MTU of
        the transmission path between the client and the peer since:[¶](#section-3.7-6)

- A probe packet with a Don't Fragment (DF) bit in the IPv4 header set to test a
            path for a larger MTU can be dropped by routers, or[¶](#section-3.7-7.1)
- ICMP error messages can be dropped by middleboxes.[¶](#section-3.7-7.2)

As a result, the client and server need to use a path MTU discovery
        algorithm that does not require ICMP messages. The Packetized Path MTU
        Discovery algorithm defined in [[RFC4821](#RFC4821)] is one
        such algorithm, and a set of algorithms is defined in [[MTU-DATAGRAM](#I-D.ietf-tsvwg-datagram-plpmtud)].[¶](#section-3.7-8)

[[MTU-STUN](#I-D.ietf-tram-stun-pmtud)] is an
        implementation of [[RFC4821](#RFC4821)] that uses STUN to
        discover the path MTU; so it might be a suitable approach to be used
        in conjunction with a TURN server that supports the DONT-FRAGMENT
        attribute. When the client includes the DONT-FRAGMENT attribute in a
        Send indication, this tells the server to set the DF bit in the
        resulting UDP datagram that it sends to the peer. Since some servers
        may be unable to set the DF bit, the client should also include this
        attribute in the Allocate request; any server that does not support
        the DONT-FRAGMENT attribute will indicate this by rejecting the
        Allocate request. If the TURN server carrying out packet translation
        from IPv4-to-IPv6 is unable to access the state of the Don't Fragment (DF)
        bit in the IPv4 header, it MUST reject the Allocate request with
        the DONT-FRAGMENT attribute.[¶](#section-3.7-9)

### 
[3.8.](#section-3.8) [RTP Support](#name-rtp-support)
        

One of the envisioned uses of TURN is as a relay for clients and
        peers wishing to exchange real-time data (e.g., voice or video) using
        RTP. To facilitate the use of TURN for this purpose, TURN includes
        some special support for older versions of RTP.[¶](#section-3.8-1)

Old versions of RTP [[RFC3550](#RFC3550)] required that
        the RTP stream be on an even port number and the associated RTP
        Control Protocol (RTCP) stream, if present, be on the next highest
        port. To allow clients to work with peers that still require this,
        TURN allows the client to request that the server allocate a relayed
        transport address with an even port number and optionally request
        the server reserve the next-highest port number for a subsequent
        allocation.[¶](#section-3.8-2)

### 
[3.9.](#section-3.9) [Happy Eyeballs for TURN](#name-happy-eyeballs-for-turn)
        

If an IPv4 path to reach a TURN server is found, but the TURN
        server's IPv6 path is not working, a dual-stack TURN client can
        experience a significant connection delay compared to an IPv4-only
        TURN client. To overcome these connection setup problems, the TURN
        client needs to query both A and AAAA records for the TURN server
        specified using a domain name and try connecting to the TURN server
        using both IPv6 and IPv4 addresses in a fashion similar to the Happy
        Eyeballs mechanism defined in [[RFC8305](#RFC8305)]. The TURN
        client performs the following steps based on the transport protocol
        being used to connect to the TURN server.[¶](#section-3.9-1)

- For TCP or TLS-over-TCP, the results of the Happy Eyeballs
            procedure [[RFC8305](#RFC8305) ] are used by the TURN
            client for sending its TURN messages to the server.[¶](#section-3.9-2.1)
- For clear text UDP, send TURN Allocate requests to both IP
            address families as discussed in [[RFC8305](#RFC8305) ]
            without authentication information.
     If the TURN server requires
            authentication, it will send back a 401 unauthenticated response;
            the TURN client will use the first UDP connection on which a 401
            error response is received. If a 401 error response is received
            from both IP address families, then the TURN client can silently
            abandon the UDP connection on the IP address family with lower
            precedence. If the TURN server does not require authentication (as
            described in[Section 9](/info/rfc8155/#section-9) of [[RFC8155](#RFC8155) ]), it is
            possible for both Allocate requests to succeed. In this case, the
            TURN client sends a Refresh with a LIFETIME value of zero on the
            allocation using the IP address family with lower precedence to
            delete the allocation.[¶](#section-3.9-2.2)
- For DTLS over UDP, initiate a DTLS handshake to both IP address
          families as discussed in [[RFC8305](#RFC8305) ],
          and use the first DTLS session that is established. If the DTLS
          session is established on both IP address families, then the client
          sends a DTLS close_notify alert to terminate the DTLS session using the IP address family with lower precedence. If the TURN over DTLS server has been configured to require a cookie exchange ( [Section 4.2](/info/rfc6347/#section-4.2) of [[RFC6347](#RFC6347) ]) and
          a HelloVerify Request is received from the TURN servers on both IP address families, then the client can silently abandon the connection on the IP address family with lower precedence. [¶](#section-3.9-2.3)

## 
[4.](#section-4) [Discovery of TURN Server](#name-discovery-of-turn-server)
      

Methods of TURN server discovery, including using anycast, are
      described in [[RFC8155](#RFC8155)]. If a host with
      multiple interfaces discovers a TURN server in each interface, the
      mechanism described in [[RFC7982](#RFC7982)] can be
      used by the TURN client to influence the TURN server selection. The
      syntax of the "turn" and "turns" URIs are defined in [Section 3.1](/info/rfc7065/#section-3.1) of [[RFC7065](#RFC7065)]. DTLS as a transport
      protocol for TURN is defined in [[RFC7350](#RFC7350)].[¶](#section-4-1)

### 
[4.1.](#section-4.1) [TURN URI Scheme Semantics](#name-turn-uri-scheme-semantics)
        

The "turn" and "turns" URI schemes are used to designate a TURN
        server (also known as a "relay") on Internet hosts accessible using the
        TURN protocol. The TURN protocol supports sending messages over UDP,
        TCP, TLS-over-TCP, or DTLS-over-UDP. The "turns" URI scheme MUST be
        used when TURN is run over TLS-over-TCP or in DTLS-over-UDP, and the
        "turn" scheme MUST be used otherwise. The required <host> part
        of the "turn" URI denotes the TURN server host. The <port> part,
        if present, denotes the port on which the TURN server is awaiting
        connection requests. If it is absent, the default port is 3478 for
        both UDP and TCP. The default port for TURN over TLS and TURN over
        DTLS is 5349.[¶](#section-4.1-1)

## 
[5.](#section-5) [General Behavior](#name-general-behavior)
      

This section contains general TURN processing rules that apply to all
      TURN messages.[¶](#section-5-1)

TURN is an extension to STUN. All TURN messages, with the exception
      of the ChannelData message, are STUN-formatted messages. All the base
      processing rules described in [[RFC8489](#RFC8489)] apply to STUN-formatted messages.
      This means that all the message-[RFC8489](#RFC8489)].[¶](#section-5-2)

[[RFC8489](#RFC8489)] specifies an
      authentication mechanism called the "long-term credential mechanism". TURN
      servers and clients MUST implement this mechanism, and the
      authentication options are discussed in [Section 7.2](#sec-rcv-allocate).[¶](#section-5-3)

Note that the long-term credential mechanism applies only to requests
      and cannot be used to authenticate indications; thus, indications in
      TURN are never authenticated. If the server requires requests to be
      authenticated, then the server's administrator MUST choose a realm value
      that will uniquely identify the username and password combination that
      the client must use, even if the client uses multiple servers under
      different administrations. The server's administrator MAY choose to
      allocate a unique username to each client, or it MAY choose to allocate the
      same username to more than one client (for example, to all clients from
      the same department or company). For each Allocate request, the server
      SHOULD generate a new random nonce when the allocation is first
      attempted following the randomness recommendations in [[RFC4086](#RFC4086)] and SHOULD expire the nonce at least once every
      hour during the lifetime of the allocation. The server uses the
      mechanism described in [Section 9.2](/info/rfc8489/#section-9.2) of [[RFC8489](#RFC8489)] to indicate that it supports
      [[RFC8489](#RFC8489)].[¶](#section-5-4)

All requests after the initial Allocate must use the same username as
      that used to create the allocation to prevent attackers from hijacking
      the client's allocation.[¶](#section-5-5)

Specifically, if:[¶](#section-5-6)

- the server requires the use of the long-term credential mechanism, and;[¶](#section-5-7.1)
- a non-Allocate request passes authentication under this mechanism, and;[¶](#section-5-7.2)
- the 5-tuple identifies an existing allocation, but;[¶](#section-5-7.3)
- the request does not use the same username as used to create the allocation,[¶](#section-5-7.4)

 then the request MUST be rejected with a 441 (Wrong
Credentials) error.[¶](#section-5-8)

When a TURN message arrives at the server from the client, the server
      uses the 5-tuple in the message to identify the associated allocation.
      For all TURN messages (including ChannelData) EXCEPT an Allocate
      request, if the 5-tuple does not identify an existing allocation, then
      the message MUST either be rejected with a 437 Allocation Mismatch error
      (if it is a request) or be silently ignored (if it is an indication or a
      ChannelData message). A client receiving a 437 error response to a
      request other than Allocate MUST assume the allocation no longer
      exists.[¶](#section-5-9)

[[RFC8489](#RFC8489)] defines a number of
      attributes, including the SOFTWARE and FINGERPRINT attributes. The
      client SHOULD include the SOFTWARE attribute in all Allocate and Refresh
      requests and MAY include it in any other requests or indications. The
      server SHOULD include the SOFTWARE attribute in all Allocate and Refresh
      responses (either success or failure) and MAY include it in other
      responses or indications. The client and the server MAY include the
      FINGERPRINT attribute in any STUN-formatted messages defined in this
      document.[¶](#section-5-10)

TURN does not use the backwards-[RFC8489](#RFC8489)].[¶](#section-5-11)

TURN, as defined in this specification, supports both IPv4 and IPv6.
      IPv6 support in TURN includes IPv4-to-IPv6, IPv6-to-IPv6, and
      IPv6-to-IPv4 relaying. When only a single address type is desired, the
      REQUESTED-[¶](#section-5-12)

By default, TURN runs on the same ports as STUN: 3478 for TURN over
      UDP and TCP, and 5349 for TURN over (D)TLS. However, TURN has its own
      set of Service Record (SRV) names: "turn" for UDP and TCP, and "turns"
      for (D)TLS. Either the DNS resolution procedures or the ALTERNATE-[Section 7](#sec-create-allocation), can be used to run TURN on a
      different port.[¶](#section-5-13)

To ensure interoperability, a TURN server MUST support the use of UDP
      transport between the client and the server, and it SHOULD support the use
      of TCP, TLS-over-TCP, and DTLS-over-UDP transports.[¶](#section-5-14)

When UDP or DTLS-over-UDP transport is used between the client and
      the server, the client will retransmit a request if it does not receive
      a response within a certain timeout period. Because of this, the server
      may receive two (or more) requests with the same 5-tuple and same
      transaction id. STUN requires that the server recognize this case and
      treat the request as idempotent (see [[RFC8489](#RFC8489)]). Some implementations may choose
      to meet this requirement by remembering all received requests and the
      corresponding responses for 40 seconds ([Section 6.3.1](/info/rfc8489/#section-6.3.1) of [[RFC8489](#RFC8489)]). Other implementations may
      choose to reprocess the request and arrange that such reprocessing
      returns essentially the same response. To aid implementors who choose
      the latter approach (the so-called "stateless stack approach"), this
      specification includes some implementation notes on how this might be
      done. Implementations are free to choose either approach or some
      other approach that gives the same results.[¶](#section-5-15)

To mitigate either intentional or unintentional denial-[Section 7.2](#sec-rcv-allocate)), and since UDP does not
      include a congestion control mechanism, it should discard application
      data traffic that exceeds the bandwidth quota.[¶](#section-5-16)

## 
[6.](#section-6) [Allocations](#name-allocations-2)
      

All TURN operations revolve around allocations, and all TURN messages
      are associated with either a single or dual allocation. An allocation
      conceptually consists of the following state data:[¶](#section-6-1)

- the relayed transport address or addresses;[¶](#section-6-2.1)
- the 5-tuple: (client's IP address, client's port, server IP
          address, server port, and transport protocol);[¶](#section-6-2.2)
- the authentication information;[¶](#section-6-2.3)
- the time-to-expiry for each relayed transport address;[¶](#section-6-2.4)
- a list of permissions for each relayed transport address;[¶](#section-6-2.5)
- a list of channel-to- peer bindings for each relayed transport address. [¶](#section-6-2.6)

The relayed transport address is the transport address
      allocated by the server for communicating with peers, while the 5-tuple
      describes the communication path between the client and the server. On
      the client, the 5-tuple uses the client's host transport address; on the
      server, the 5-tuple uses the client's server-[¶](#section-6-3)

The authentication information (e.g., username, password, realm, and
      nonce) is used to both verify subsequent requests and to compute the
      message integrity of responses. The username, realm, and nonce values
      are initially those used in the authenticated Allocate request that
      creates the allocation, though the server can change the nonce value
      during the lifetime of the allocation using a 438 (Stale Nonce) reply.
      For security reasons, the server MUST NOT store the
      password explicitly and MUST store the key value, which
      is a cryptographic hash over the username, realm, and password (see
      [Section 16.1.3](/info/rfc8489/#section-16.1.3) of [[RFC8489](#RFC8489)]).[¶](#section-6-4)

Note that if the response contains a PASSWORD-[¶](#section-6-5)

The time-to-expiry is the time in seconds left until the allocation
      expires. Each Allocate or Refresh transaction sets this timer, which
      then ticks down towards zero. By default, each Allocate or Refresh
      transaction resets this timer to the default lifetime value of 600
      seconds (10 minutes), but the client can request a different value in
      the Allocate and Refresh request. Allocations can only be refreshed
      using the Refresh request; sending data to a peer does not refresh an
      allocation. When an allocation expires, the state data associated with
      the allocation can be freed.[¶](#section-6-6)

The list of permissions is described in [Section 9](#sec-permissions) and the list of channels is described
      in [Section 12](#sec-channels).[¶](#section-6-7)

## 
[7.](#section-7) [Creating an Allocation](#name-creating-an-allocation)
      

An allocation on the server is created using an Allocate
      transaction.[¶](#section-7-1)

### 
[7.1.](#section-7.1) [Sending an Allocate Request](#name-sending-an-allocate-request)
        

The client forms an Allocate request as follows.[¶](#section-7.1-1)

The client first picks a host transport address. It is RECOMMENDED
        that the client pick a currently unused transport address, typically
        by allowing the underlying OS to pick a currently unused port.[¶](#section-7.1-2)

The client then picks a transport protocol that the client supports
        to use between the client and the server based on the transport
        protocols supported by the server. Since this specification only
        allows UDP between the server and the peers, it is RECOMMENDED that
        the client pick UDP unless it has a reason to use a different
        transport. One reason to pick a different transport would be that the
        client believes, either through configuration or discovery or by
        experiment, that it is unable to contact any TURN server using UDP.
        See [Section 3.1](#sec-transports) for more discussion.[¶](#section-7.1-3)

The client also picks a server transport address, which SHOULD be
        done as follows. The client uses one or more procedures described in
        [[RFC8155](#RFC8155)] to discover a TURN server and uses the
        TURN server resolution mechanism defined in [[RFC5928](#RFC5928)] and [[RFC7350](#RFC7350)] to get a
        list of server transport addresses that can be tried to create a TURN
        allocation.[¶](#section-7.1-4)

The client MUST include a REQUESTED-[¶](#section-7.1-5)

If the client wishes to obtain a relayed transport address of a
        specific address type, then it includes a REQUESTED-[¶](#section-7.1-6)

If the client wishes to obtain one IPv6 and one IPv4 relayed
        transport address, then it includes an ADDITIONAL-[¶](#section-7.1-7)

If the client wishes the server to initialize the time-to-expiry
        field of the allocation to some value other than the default lifetime,
        then it MAY include a LIFETIME attribute specifying its desired value.
        This is just a hint, and the server may elect to use a different
        value. Note that the server will ignore requests to initialize the
        field to less than the default value.[¶](#section-7.1-8)

If the client wishes to later use the DONT-FRAGMENT attribute in
        one or more Send indications on this allocation, then the client
        SHOULD include the DONT-FRAGMENT attribute in the Allocate request.
        This allows the client to test whether this attribute is supported by
        the server.[¶](#section-7.1-9)

If the client requires the port number of the relayed transport
        address to be even, the client includes the EVEN-PORT attribute. If this
        attribute is not included, then the port can be even or odd. By
        setting the R bit in the EVEN-PORT attribute to 1, the client can
        request that the server reserve the next highest port number (on the
        same IP address) for a subsequent allocation. If the R bit is 0, no
        such request is made.[¶](#section-7.1-10)

The client MAY also include a RESERVATION-[¶](#section-7.1-11)

Once constructed, the client sends the Allocate request on the
        5-tuple.[¶](#section-7.1-12)

### 
[7.2.](#section-7.2) [Receiving an Allocate Request](#name-receiving-an-allocate-reque)
        

When the server receives an Allocate request, it performs the
        following checks:[¶](#section-7.2-1)

1. The TURN server provided by the local or access network
          MAY allow an unauthenticated request in order to
          accept Allocation requests from new and/or guest users in the
          network who do not necessarily possess long-term credentials for
          STUN authentication.  The security implications of STUN and making
          STUN authentication optional are discussed in [[RFC8155](#RFC8155) ]. Otherwise, the server MUST
          require that the request be authenticated. If the request is
          authenticated, the authentication MUST be done either
          using the long-term credential mechanism of [[RFC8489](#RFC8489) ] or using the STUN Extension for Third-Party
          Authorization [[RFC7635](#RFC7635) ] unless the
          client and server agree to use another mechanism through some
          procedure outside the scope of this document.[¶](#section-7.2-2.1)
2. The server checks if the 5-tuple is currently in use by an
            existing allocation. If yes, the server rejects the request with a
            437 (Allocation Mismatch) error.[¶](#section-7.2-2.2)
3. The server checks if the request contains a REQUESTED-TRANSPORT attribute. If the REQUESTED- TRANSPORT attribute is not included or is malformed, the server rejects the request with a 400 (Bad Request) error. Otherwise, if the attribute is included but specifies a protocol that is not supported by the server, the server rejects the request with a 442 (Unsupported Transport Protocol) error. [¶](#section-7.2-2.3)
4. The request may contain a DONT-FRAGMENT attribute. If it does,
            but the server does not support sending UDP datagrams with the DF
            bit set to 1 (see Sections [14](#sec-ip-header-fields) and[15](#sec-ip-header-fields-tcp-udp) ), then the
            server treats the DONT-FRAGMENT attribute in the Allocate request
            as an unknown comprehension-required attribute. [¶](#section-7.2-2.4)
5. The server checks if the request contains a RESERVATION-TOKEN attribute. If yes, and the request also contains an EVEN-PORT or REQUESTED- ADDRESS- FAMILY or ADDITIONAL- ADDRESS- FAMILY attribute, the server rejects the request with a 400 (Bad Request) error. Otherwise, it checks to see if the token is valid (i.e., the token is in range and has not expired, and the corresponding relayed transport address is still available). If the token is not valid for some reason, the server rejects the request with a 508 (Insufficient Capacity) error. [¶](#section-7.2-2.5)
6. The server checks if the request contains both
            REQUESTED-ADDRESS- FAMILY and ADDITIONAL- ADDRESS- FAMILY attributes. If yes, then the server rejects the request with a 400 (Bad Request) error. [¶](#section-7.2-2.6)
7. If the server does not support the address family requested by
            the client in REQUESTED-ADDRESS- FAMILY, or if the allocation of the requested address family is disabled by local policy, it MUST generate an Allocate error response, and it MUST include an ERROR-CODE attribute with the 440 (Address Family not Supported) response code. If the REQUESTED- ADDRESS- FAMILY attribute is absent and the server does not support the IPv4 address family, the server MUST include an ERROR-CODE attribute with the 440 (Address Family not Supported) response code. If the REQUESTED- ADDRESS- FAMILY attribute is absent and the server supports the IPv4 address family, the server MUST allocate an IPv4 relayed transport address for the TURN client. [¶](#section-7.2-2.7)
8. The server checks if the request contains an EVEN-PORT
            attribute with the R bit set to 1. If yes, and the request also
            contains an ADDITIONAL-ADDRESS- FAMILY attribute, the server rejects the request with a 400 (Bad Request) error. Otherwise, the server checks if it can satisfy the request (i.e., can allocate a relayed transport address as described below). If the server cannot satisfy the request, then the server rejects the request with a 508 (Insufficient Capacity) error. [¶](#section-7.2-2.8)
9. The server checks if the request contains an
            ADDITIONAL-ADDRESS- FAMILY attribute. If yes, and the attribute value is 0x01 (IPv4 address family), then the server rejects the request with a 400 (Bad Request) error. Otherwise, the server checks if it can allocate relayed transport addresses of both address types. If the server cannot satisfy the request, then the server rejects the request with a 508 (Insufficient Capacity) error. If the server can partially meet the request, i.e., if it can only allocate one relayed transport address of a specific address type, then it includes ADDRESS- ERROR- CODE attribute in the success response to inform the client the reason for partial failure of the request. The error code value signaled in the ADDRESS- ERROR- CODE attribute could be 440 (Address Family not Supported) or 508 (Insufficient Capacity). If the server can fully meet the request, then the server allocates one IPv4 and one IPv6 relay address and returns an Allocate success response containing the relayed transport addresses assigned to the dual allocation in two XOR- RELAYED- ADDRESS attributes. [¶](#section-7.2-2.9)
10. At any point, the server MAY choose to reject the
          request with a 486 (Allocation Quota Reached) error if it feels the
          client is trying to exceed some locally defined allocation
          quota. The server is free to define this allocation quota any way it
          wishes, but it SHOULD define it based on the username
          used to authenticate the request and not on the client's transport
          address.[¶](#section-7.2-2.10)
11. Also, at any point, the server MAY choose to reject the request
            with a 300 (Try Alternate) error if it wishes to redirect the
            client to a different server. The use of this error code and
            attribute follows the specification in [[RFC8489](#RFC8489) ].[¶](#section-7.2-2.11)

If all the checks pass, the server creates the allocation. The
        5-tuple is set to the 5-tuple from the Allocate request, while the
        list of permissions and the list of channels are initially empty.[¶](#section-7.2-3)

The server chooses a relayed transport address for the allocation
        as follows:[¶](#section-7.2-4)

- If the request contains a RESERVATION-TOKEN attribute, the server uses the previously reserved transport address corresponding to the included token (if it is still available). Note that the reservation is a server-wide reservation and is not specific to a particular allocation since the Allocate request containing the RESERVATION- TOKEN uses a different 5-tuple than the Allocate request that made the reservation. The 5-tuple for the Allocate request containing the RESERVATION- TOKEN attribute can be any allowed 5-tuple; it can use a different client IP address and port, a different transport protocol, and even a different server IP address and port (provided, of course, that the server IP address and port are ones on which the server is listening for TURN requests). [¶](#section-7.2-5.1)
- If the request contains an EVEN-PORT attribute with the R bit
            set to 0, then the server allocates a relayed transport address
            with an even port number.[¶](#section-7.2-5.2)
- If the request contains an EVEN-PORT attribute with the R bit
            set to 1, then the server looks for a pair of port numbers N and
            N+1 on the same IP address, where N is even. Port N is used in the
            current allocation, while the relayed transport address with port
            N+1 is assigned a token and reserved for a future allocation. The
            server MUST hold this reservation for at least 30 seconds and MAY
            choose to hold longer (e.g., until the allocation with port N
            expires). The server then includes the token in a
            RESERVATION-TOKEN attribute in the success response. [¶](#section-7.2-5.3)
- Otherwise, the server allocates any available relayed transport
            address.[¶](#section-7.2-5.4)

In all cases, the server SHOULD only allocate ports from the range
        49152 - 65535 (the Dynamic and/or Private Port range [[PORT-NUMBERS](#PORT-NUMBERS)]), unless the TURN server application
        knows, through some means not specified here, that other applications
        running on the same host as the TURN server application will not be
        impacted by allocating ports outside this range. This condition can
        often be satisfied by running the TURN server application on a
        dedicated machine and/or by arranging that any other applications on
        the machine allocate ports before the TURN server application starts.
        In any case, the TURN server SHOULD NOT allocate ports in the range 0
        - 1023 (the Well-Known Port range) to discourage clients from using
        TURN to run standard services.[¶](#section-7.2-6)

The server determines the initial value of the time-to-expiry field
        as follows. If the request contains a LIFETIME attribute, then the
        server computes the minimum of the client's proposed lifetime and the
        server's maximum allowed lifetime. If this computed value is greater
        than the default lifetime, then the server uses the computed lifetime
        as the initial value of the time-to-expiry field. Otherwise, the
        server uses the default lifetime. It is RECOMMENDED that the server
        use a maximum allowed lifetime value of no more than 3600 seconds (1
        hour). Servers that implement allocation quotas or charge users for
        allocations in some way may wish to use a smaller maximum allowed
        lifetime (perhaps as small as the default lifetime) to more quickly
        remove orphaned allocations (that is, allocations where the
        corresponding client has crashed or terminated, or the client
        connection has been lost for some reason). Also, note that the time-
        to-expiry is recomputed with each successful Refresh request, and thus,
        the value computed here applies only until the first refresh.[¶](#section-7.2-8)

Once the allocation is created, the server replies with a success
        response. The success response contains:[¶](#section-7.2-9)

- An XOR-RELAYED- ADDRESS attribute containing the relayed transport address or two XOR- RELAYED- ADDRESS attributes containing the relayed transport addresses. [¶](#section-7.2-10.1)
- A LIFETIME attribute containing the current value of the
            time-to-expiry timer.[¶](#section-7.2-10.2)
- A RESERVATION-TOKEN attribute (if a second relayed transport address was reserved). [¶](#section-7.2-10.3)
- An XOR-MAPPED- ADDRESS attribute containing the client's IP address and port (from the 5-tuple). [¶](#section-7.2-10.4)

The response (either success or error) is sent back to the client
        on the 5-tuple.[¶](#section-7.2-12)

### 
[7.3.](#section-7.3) [Receiving an Allocate Success Response](#name-receiving-an-allocate-succe)
        

If the client receives an Allocate success response, then it MUST
        check that the mapped address and the relayed transport address or
        addresses are part of an address family or families that the client
        understands and is prepared to handle. If these addresses are not part
        of an address family or families that the client is prepared to
        handle, then the client MUST delete the allocation ([Section 8](#sec-refreshing-allocation)) and MUST NOT attempt to
        create another allocation on that server until it believes the
        mismatch has been fixed.[¶](#section-7.3-1)

Otherwise, the client creates its own copy of the allocation data
        structure to track what is happening on the server. In particular, the
        client needs to remember the actual lifetime received back from the
        server, rather than the value sent to the server in the request. The
        client must also remember the 5-tuple used for the request and the
        username and password it used to authenticate the request to ensure
        that it reuses them for subsequent messages. The client also needs to
        track the channels and permissions it establishes on the server.[¶](#section-7.3-2)

If the client receives an Allocate success response but with an
        ADDRESS-[¶](#section-7.3-3)

The client will probably wish to send the relayed transport address
        to peers (using some method not specified here) so the peers can
        communicate with it. The client may also wish to use the
        server-[¶](#section-7.3-4)

### 
[7.4.](#section-7.4) [Receiving an Allocate Error Response](#name-receiving-an-allocate-error)
        

If the client receives an Allocate error response, then the
        processing depends on the actual error code returned:[¶](#section-7.4-1)

- 408 (Request timed out):
- There is either a problem with the
          server or a problem reaching the server with the chosen
          transport. The client considers the current transaction as having
          failed but MAY choose to retry the Allocate request
          using a different transport (e.g., TCP instead of UDP).[¶](#section-7.4-2.2)
- 300 (Try Alternate):
- The server would like the client to use
            the server specified in the ALTERNATE-SERVER attribute instead. The client considers the current transaction as having failed, but it SHOULD try the Allocate request with the alternate server before trying any other servers (e.g., other servers discovered using the DNS resolution procedures). When trying the Allocate request with the alternate server, the client follows the ALTERNATE- SERVER procedures specified in [ [RFC8489](#RFC8489) ].[¶](#section-7.4-2.4)
- 400 (Bad Request):
- The server believes the client's request is
            malformed for some reason. The client considers the current
            transaction as having failed. The client MAY notify the user or
            operator and SHOULD NOT retry the request with this server until
            it believes the problem has been fixed.[¶](#section-7.4-2.6)
- 401 (Unauthorized):
-  If the client has followed the procedures
            of the long-term credential mechanism and still gets this error,
            then the server is not accepting the client's credentials. In this
            case, the client considers the current transaction as having
            failed and SHOULD notify the user or operator. The client SHOULD NOT send any further requests to this server until it believes the
            problem has been fixed.[¶](#section-7.4-2.8)
- 403 (Forbidden):
- The request is valid, but the server is
            refusing to perform it, likely due to administrative restrictions.
            The client considers the current transaction as having failed. The
            client MAY notify the user or operator and SHOULD NOT retry the
            same request with this server until it believes the problem has
            been fixed.[¶](#section-7.4-2.10)
- 420 (Unknown Attribute):
- If the client included a DONT-FRAGMENT
            attribute in the request and the server rejected the request with
            a 420 error code and listed the DONT-FRAGMENT attribute in the
            UNKNOWN-ATTRIBUTES attribute in the error response, then the client now knows that the server does not support the DONT-FRAGMENT attribute. The client considers the current transaction as having failed but MAY choose to retry the Allocate request without the DONT-FRAGMENT attribute. [¶](#section-7.4-2.12)
- 437 (Allocation Mismatch):
- This indicates that the client has
            picked a 5-tuple that the server sees as already in use. One way
            this could happen is if an intervening NAT assigned a mapped
            transport address that was used by another client that recently
            crashed. The client considers the current transaction as having
            failed. The client SHOULD pick another client transport address
            and retry the Allocate request (using a different transaction id).
            The client SHOULD try three different client transport addresses
            before giving up on this server. Once the client gives up on the
            server, it SHOULD NOT try to create another allocation on the
            server for 2 minutes.[¶](#section-7.4-2.14)
- 438 (Stale Nonce):
- See the procedures for the long-term
            credential mechanism [[RFC8489](#RFC8489) ].[¶](#section-7.4-2.16)
- 440 (Address Family not Supported):
- The server does not support
            the address family requested by the client. If the client receives
            an Allocate error response with the 440 (Address Family not
     Supported) error code, the client MUST NOT retry the request.[¶](#section-7.4-2.18)
- 441 (Wrong Credentials):
- The client should not receive this
            error in response to an Allocate request. The client MAY notify the
            user or operator and SHOULD NOT retry the same request with this
            server until it believes the problem has been fixed.[¶](#section-7.4-2.20)
- 442 (Unsupported Transport Address):
- The client should not
            receive this error in response to a request for a UDP allocation.
            The client MAY notify the user or operator and SHOULD NOT
            reattempt the request with this server until it believes the
            problem has been fixed.[¶](#section-7.4-2.22)
- 486 (Allocation Quota Reached):
- The server is currently unable
            to create any more allocations with this username. The client
            considers the current transaction as having failed. The client
            SHOULD wait at least 1 minute before trying to create any more
            allocations on the server.[¶](#section-7.4-2.24)
- 508 (Insufficient Capacity):
- 
     The server has no more relayed transport addresses available or has
     none with the requested properties, or the one that was reserved
     is no longer available.  The client considers the current
     operation as having failed. If the client is using either the
     EVEN-PORT or the RESERVATION-TOKEN attribute, then the client MAY choose to remove or modify this attribute and try again immediately. Otherwise, the client SHOULD wait at least 1 minute before trying to create any more allocations on this server. [¶](#section-7.4-2.26)

Note that the error code values 486 and 508 indicate to a
        eavesdropper that several other users are using the server at this
        time, similar to that of the HTTP error response code 503, but
 it does
        not reveal any information about the users using the TURN server.[¶](#section-7.4-3)

An unknown error response MUST be handled as described in [[RFC8489](#RFC8489)].[¶](#section-7.4-4)

## 
[8.](#section-8) [Refreshing an Allocation](#name-refreshing-an-allocation)
      

A Refresh transaction can be used to either (a) refresh an existing
      allocation and update its time-to-expiry or (b) delete an existing
      allocation.[¶](#section-8-1)

If a client wishes to continue using an allocation, then the client
      MUST refresh it before it expires. It is suggested that the client
      refresh the allocation roughly 1 minute before it expires. If a client
      no longer wishes to use an allocation, then it SHOULD explicitly delete
      the allocation. A client MAY refresh an allocation at any time for other
      reasons.[¶](#section-8-2)

### 
[8.1.](#section-8.1) [Sending a Refresh Request](#name-sending-a-refresh-request)
        

If the client wishes to immediately delete an existing allocation,
        it includes a LIFETIME attribute with a value of zero. All other forms of
        the request refresh the allocation.[¶](#section-8.1-1)

When refreshing a dual allocation, the client includes
        a REQUESTED-[¶](#section-8.1-2)

The Refresh transaction updates the time-to-expiry timer of an
        allocation. If the client wishes the server to set the time-to-expiry
        timer to something other than the default lifetime, it includes a
        LIFETIME attribute with the requested value. The server then computes
        a new time-to-expiry value in the same way as it does for an Allocate
        transaction, with the exception that a requested lifetime of zero causes
        the server to immediately delete the allocation.[¶](#section-8.1-3)

### 
[8.2.](#section-8.2) [Receiving a Refresh Request](#name-receiving-a-refresh-request)
        

When the server receives a Refresh request, it processes the
        request as per [Section 5](#sec-general-behavior) plus the
        specific rules mentioned here.[¶](#section-8.2-1)

If the server receives a Refresh Request with a
        REQUESTED-[¶](#section-8.2-2)

The server computes a value called the "desired lifetime" as
        follows: if the request contains a LIFETIME attribute and the
        attribute value is zero, then the "desired lifetime" is zero. Otherwise, if
        the request contains a LIFETIME attribute, then the server computes
        the minimum of the client's requested lifetime and the server's
        maximum allowed lifetime. If this computed value is greater than the
        default lifetime, then the "desired lifetime" is the computed value.
        Otherwise, the "desired lifetime" is the default lifetime.[¶](#section-8.2-3)

Subsequent processing depends on the "desired lifetime" value:[¶](#section-8.2-4)

- If the "desired lifetime" is zero, then the request succeeds and
            the allocation is deleted.[¶](#section-8.2-5.1)
- If the "desired lifetime" is non-zero, then the request
            succeeds and the allocation's time-to-expiry is set to the
            "desired lifetime".[¶](#section-8.2-5.2)

If the request succeeds, then the server sends a success
        response containing:[¶](#section-8.2-6)

- A LIFETIME attribute containing the current value of the
            time-to-expiry timer.[¶](#section-8.2-7.1)

### 
[8.3.](#section-8.3) [Receiving a Refresh Response](#name-receiving-a-refresh-respons)
        

If the client receives a success response to its Refresh request
        with a non-zero lifetime, it updates its copy of the allocation data
        structure with the time-to-expiry value contained in the response. If
        the client receives a 437 (Allocation Mismatch) error response to its
        request to refresh the allocation, it should consider the allocation
        no longer exists. If the client receives a 438 (Stale Nonce) error to
        its request to refresh the allocation, it should reattempt the request
        with the new nonce value.[¶](#section-8.3-1)

If the client receives a 437 (Allocation Mismatch) error response
        to a request to delete the allocation, then the allocation no longer
        exists and it should consider its request as having effectively
        succeeded.[¶](#section-8.3-2)

## 
[9.](#section-9) [Permissions](#name-permissions-2)
      

For each allocation, the server keeps a list of zero or more
      permissions. Each permission consists of an IP address and an associated
      time-[¶](#section-9-1)

By sending either Create[¶](#section-9-2)

- If no permission for that IP address exists, then a permission is
          created with the given IP address and a time-to-expiry equal to
          Permission Lifetime.[¶](#section-9-3.1)
- If a permission for that IP address already exists, then the
          time-to-expiry for that permission is reset to Permission
          Lifetime.[¶](#section-9-3.2)

The Permission Lifetime MUST be 300 seconds (= 5 minutes).[¶](#section-9-4)

Each permission's time-to-expiry decreases down once per second
      until it reaches zero, at which point, the permission expires and is
      deleted.[¶](#section-9-5)

Create[¶](#section-9-6)

When a UDP datagram arrives at the relayed transport address for the
      allocation, the server extracts the source IP address from the IP
      header. The server then compares this address with the IP address
      associated with each permission in the list of permissions for the
      allocation. Note that only addresses are compared and port numbers are
      not considered. If no match is found, relaying is not permitted and the
      server silently discards the UDP datagram. If an exact match is found,
      the permission check is considered to have succeeded and the server
      continues to process the UDP datagram as specified elsewhere ([Section 11.3](#sec-sending-data-indication)).[¶](#section-9-7)

The permissions for one allocation are totally unrelated to the
      permissions for a different allocation. If an allocation expires, all
      its permissions expire with it.[¶](#section-9-8)

## 
[10.](#section-10) [CreatePermission](#name-createpermission)
      

TURN supports two ways for the client to install or refresh
      permissions on the server. This section describes one way: the
      Create[¶](#section-10-1)

A Create[Section 11](#sec-sendanddata) or the Channel
      mechanism in [Section 12](#sec-channels).[¶](#section-10-2)

### 
[10.1.](#section-10.1) [Forming a CreatePermission Request](#name-forming-a-createpermission-)
        

The client who wishes to install or refresh one or more permissions
        can send a Create[¶](#section-10.1-1)

When forming a Create[¶](#section-10.1-2)

### 
[10.2.](#section-10.2) [Receiving a CreatePermission Request](#name-receiving-a-createpermissio)
        

When the server receives the Create[Section 5](#sec-general-behavior) plus the specific
        rules mentioned here.[¶](#section-10.2-1)

The message is checked for validity. The Create[¶](#section-10.2-2)

If an XOR-[¶](#section-10.2-3)

The server MAY impose restrictions on the IP address allowed in the
        XOR-[¶](#section-10.2-4)

If the message is valid and the server is capable of carrying out
        the request, then the server installs or refreshes a permission for
        the IP address contained in each XOR-[Section 9](#sec-permissions). The port portion
        of each attribute is ignored and may be any arbitrary value.[¶](#section-10.2-5)

The server then responds with a Create[¶](#section-10.2-6)

### 
[10.3.](#section-10.3) [Receiving a CreatePermission Response](#name-receiving-a-createpermission)
        

If the client receives a valid Create[¶](#section-10.3-1)

## 
[11.](#section-11) [Send and Data Methods](#name-send-and-data-methods)
      

TURN supports two mechanisms for sending and receiving data from
      peers. This section describes the use of the Send and Data mechanisms,
      while [Section 12](#sec-channels) describes the use of the
      Channel mechanism.[¶](#section-11-1)

### 
[11.1.](#section-11.1) [Forming a Send Indication](#name-forming-a-send-indication)
        

The client can use a Send indication to pass data to the server for
        relaying to a peer. A client may use a Send indication even if a
        channel is bound to that peer. However, the client MUST ensure that
        there is a permission installed for the IP address of the peer to
        which the Send indication is being sent; this prevents a third party
        from using a TURN server to send data to arbitrary destinations.[¶](#section-11.1-1)

When forming a Send indication, the client MUST include an
        XOR-[¶](#section-11.1-2)

The client MAY include a DONT-FRAGMENT attribute in the Send
        indication if it wishes the server to set the DF bit on the UDP
        datagram sent to the peer.[¶](#section-11.1-3)

### 
[11.2.](#section-11.2) [Receiving a Send Indication](#name-receiving-a-send-indication)
        

When the server receives a Send indication, it processes as per
        [Section 5](#sec-general-behavior) plus the specific rules
        mentioned here.[¶](#section-11.2-1)

The message is first checked for validity. The Send indication MUST
        contain both an XOR-[¶](#section-11.2-2)

The Send indication may also contain the DONT-FRAGMENT attribute.
        If the server is unable to set the DF bit on outgoing UDP datagrams
        when this attribute is present, then the server acts as if the
        DONT-FRAGMENT attribute is an unknown comprehension-[¶](#section-11.2-3)

The server also checks that there is a permission installed for the
        IP address contained in the XOR-[¶](#section-11.2-4)

The server MAY impose restrictions on the IP address and port
        values allowed in the XOR-[¶](#section-11.2-5)

If everything is OK, then the server forms a UDP datagram as
        follows:[¶](#section-11.2-6)

- the source transport address is the relayed transport address
            of the allocation, where the allocation is determined by the
            5-tuple on which the Send indication arrived;[¶](#section-11.2-7.1)
- the destination transport address is taken from the
            XOR-PEER- ADDRESS attribute; [¶](#section-11.2-7.2)
- the data following the UDP header is the contents of the value
            field of the DATA attribute.[¶](#section-11.2-7.3)

The handling of the DONT-FRAGMENT attribute (if present), is
        described in Sections [14](#sec-ip-header-fields) and [15](#sec-ip-header-fields-tcp-udp).[¶](#section-11.2-8)

The resulting UDP datagram is then sent to the peer.[¶](#section-11.2-9)

### 
[11.3.](#section-11.3) [Receiving a UDP Datagram](#name-receiving-a-udp-datagram)
        

When the server receives a UDP datagram at a currently allocated
        relayed transport address, the server looks up the allocation
        associated with the relayed transport address. The server then checks
        to see whether the set of permissions for the allocation allow the
        relaying of the UDP datagram as described in [Section 9](#sec-permissions).[¶](#section-11.3-1)

If relaying is permitted, then the server checks if there is a
        channel bound to the peer that sent the UDP datagram (see [Section 12](#sec-channels)). If a channel is bound, then processing
        proceeds as described in [Section 12.7](#sec-channel-relaying).[¶](#section-11.3-2)

If relaying is permitted but no channel is bound to the peer, then
        the server forms and sends a Data indication. The Data indication MUST
        contain both an XOR-[¶](#section-11.3-3)

### 
[11.4.](#section-11.4) [Receiving a Data Indication](#name-receiving-a-data-indication)
        

When the client receives a Data indication, it checks that the Data
        indication contains an XOR-[¶](#section-11.4-1)

If the XOR-[Section 11.6](#receive-senderror).[¶](#section-11.4-3)

If the Data indication passes the above checks, the client delivers
        the data octets inside the DATA attribute to the application, along
        with an indication that they were received from the peer whose
        transport address is given by the XOR-[¶](#section-11.4-4)

### 
[11.5.](#section-11.5) [Receiving an ICMP Packet](#name-receiving-an-icmp-packet)
        

When the server receives an ICMP packet, the server verifies that
        the type is either 3 or 11 for an ICMPv4 [[RFC0792](#RFC0792)] packet or either 1, 2, or 3 for an ICMPv6
        [[RFC4443](#RFC4443)] packet. It also verifies that the IP
        packet in the ICMP packet payload contains a UDP header. If either of
        these conditions fail, then the ICMP packet is silently dropped. If a
        UDP header is present, the server extracts the source and destination
        IP address and UDP port information.[¶](#section-11.5-1)

The server looks up the allocation whose relayed transport address
        corresponds to the encapsulated packet's source IP address and UDP
        port. If no such allocation exists, the packet is silently dropped.
        The server then checks to see whether the set of permissions for the
        allocation allows the relaying of the ICMP packet. For ICMP packets,
        the source IP address MUST NOT be checked against the permissions list
        as it would be for UDP packets. Instead, the server extracts the
        destination IP address from the encapsulated IP header. The server
        then compares this address with the IP address associated with each
        permission in the list of permissions for the allocation. If no match
        is found, relaying is not permitted and the server silently discards
        the ICMP packet. Note that only addresses are compared and port
        numbers are not considered.[¶](#section-11.5-2)

If relaying is permitted, then the server forms and sends a Data
        indication. The Data indication MUST contain both an XOR-[¶](#section-11.5-3)

### 
[11.6.](#section-11.6) [Receiving a Data Indication with an ICMP Attribute](#name-receiving-a-data-indication-)
        

When the client receives a Data indication with an ICMP attribute,
        it checks that the Data indication contains an XOR-[¶](#section-11.6-1)

If the Data indication passes the above checks, the client signals
        the application of the error condition along with an indication that
        it was received from the peer whose transport address is given by the
        XOR-[¶](#section-11.6-2)

## 
[12.](#section-12) [Channels](#name-channels-2)
      

Channels provide a way for the client and server to send application
      data using ChannelData messages, which have less overhead than Send and
      Data indications.[¶](#section-12-1)

The ChannelData message (see [Section 12.4](#sec-channeldata-msg)) starts with a two-byte field that
      carries the channel number. The values of this field are allocated as
      follows:[¶](#section-12-2)

Note that the channel number range is not backwards compatible with
      [[RFC5766](#RFC5766)], which could prevent a client
      compliant with RFC 5766 from establishing channel bindings with a
      TURN server that complies with this specification.[¶](#section-12-4)

According to [[RFC7983](#RFC7983)], ChannelData messages can
      be distinguished from other multiplexed protocols by examining the first
      byte of the message:[¶](#section-12-5)

| Table 3 |  | 
|---|---|
| [0..3] | STUN | 
| [16..19] | ZRTP | 
| [20..63] | DTLS | 
| [64..79] | TURN Channel | 
| [128..191] | RTP/RTCP | 
| Others | Reserved; MUST be dropped and an alert MAY be logged | 

[Table 3](#table-3)

Reserved values may be used in the future by other protocols. When
      the client uses channel binding, it MUST comply with the demultiplexing
      scheme discussed above.[¶](#section-12-7)

Channel bindings are always initiated by the client. The client can
      bind a channel to a peer at any time during the lifetime of the
      allocation. The client may bind a channel to a peer before exchanging
      data with it or after exchanging data with it (using Send and Data
      indications) for some time, or may choose never to bind a channel to it.
      The client can also bind channels to some peers while not binding
      channels to other peers.[¶](#section-12-8)

Channel bindings are specific to an allocation so that the use of a
      channel number or peer transport address in a channel binding in one
      allocation has no impact on their use in a different allocation. If an
      allocation expires, all its channel bindings expire with it.[¶](#section-12-9)

A channel binding consists of:[¶](#section-12-10)

Within the context of an allocation, a channel binding is
      uniquely identified either by the channel number or by the peer's
      transport address. Thus, the same channel cannot be bound to two
      different transport addresses, nor can the same transport address be
      bound to two different channels.[¶](#section-12-12)

A channel binding lasts for 10 minutes unless refreshed. Refreshing
      the binding (by the server receiving a ChannelBind request rebinding the
      channel to the same peer) resets the time-to-expiry timer back to 10
      minutes.[¶](#section-12-13)

When the channel binding expires, the channel becomes unbound. Once
      unbound, the channel number can be bound to a different transport
      address, and the transport address can be bound to a different channel
      number. To prevent race conditions, the client MUST wait 5 minutes after
      the channel binding expires before attempting to bind the channel number
      to a different transport address or the transport address to a different
      channel number.[¶](#section-12-14)

When binding a channel to a peer, the client SHOULD be prepared to
      receive ChannelData messages on the channel from the server as soon as
      it has sent the ChannelBind request. Over UDP, it is possible for the
      client to receive ChannelData messages from the server before it
      receives a ChannelBind success response.[¶](#section-12-15)

In the other direction, the client MAY elect to send ChannelData
      messages before receiving the ChannelBind success response. Doing so,
      however, runs the risk of having the ChannelData messages dropped by the
      server if the ChannelBind request does not succeed for some reason
      (e.g., packet lost if the request is sent over UDP or the server being
      unable to fulfill the request). A client that wishes to be safe should
      either queue the data or use Send indications until the channel binding
      is confirmed.[¶](#section-12-16)

### 
[12.1.](#section-12.1) [Sending a ChannelBind Request](#name-sending-a-channelbind-reque)
        

A channel binding is created or refreshed using a ChannelBind
        transaction. A ChannelBind transaction also creates or refreshes a
        permission towards the peer (see [Section 9](#sec-permissions)).[¶](#section-12.1-1)

To initiate the ChannelBind transaction, the client forms a
        ChannelBind request. The channel to be bound is specified in a
        CHANNEL-NUMBER attribute, and the peer's transport address is
        specified in an XOR-[Section 12.2](#sec-receiving-ChannelBind) describes the restrictions
        on these attributes. The client MUST only include an XOR-[¶](#section-12.1-2)

Rebinding a channel to the same transport address that it is
        already bound to provides a way to refresh a channel binding and the
        corresponding permission without sending data to the peer. Note,
        however, that permissions need to be refreshed more frequently than
        channels.[¶](#section-12.1-3)

### 
[12.2.](#section-12.2) [Receiving a ChannelBind Request](#name-receiving-a-channelbind-req)
        

When the server receives a ChannelBind request, it processes as per
        [Section 5](#sec-general-behavior) plus the specific rules
        mentioned here.[¶](#section-12.2-1)

The server checks the following:[¶](#section-12.2-2)

- The request contains both a CHANNEL-NUMBER and an
            XOR-PEER- ADDRESS attribute; [¶](#section-12.2-3.1)
- The channel number is in the range 0x4000 through 0x4FFF
            (inclusive);[¶](#section-12.2-3.2)
- The channel number is not currently bound to a different
            transport address (same transport address is OK);[¶](#section-12.2-3.3)
- The transport address is not currently bound to a different
            channel number.[¶](#section-12.2-3.4)

If any of these tests fail, the server replies with a 400 (Bad
        Request) error. If the XOR-[¶](#section-12.2-4)

The server MAY impose restrictions on the IP address and port
        values allowed in the XOR-[¶](#section-12.2-5)

If the request is valid, but the server is unable to fulfill the
        request due to some capacity limit or similar, the server replies with
        a 508 (Insufficient Capacity) error.[¶](#section-12.2-6)

Otherwise, the server replies with a ChannelBind success response.
        There are no required attributes in a successful ChannelBind
        response.[¶](#section-12.2-7)

If the server can satisfy the request, then the server creates or
        refreshes the channel binding using the channel number in the
        CHANNEL-NUMBER attribute and the transport address in the
        XOR-[Section 9](#sec-permissions).[¶](#section-12.2-8)

### 
[12.3.](#section-12.3) [Receiving a ChannelBind Response](#name-receiving-a-channelbind-res)
        

When the client receives a ChannelBind success response, it updates
        its data structures to record that the channel binding is now active.
        It also updates its data structures to record that the corresponding
        permission has been installed or refreshed.[¶](#section-12.3-1)

If the client receives a ChannelBind failure response that
        indicates that the channel information is out of sync between the
        client and the server (e.g., an unexpected 400 "Bad Request"
        response), then it is RECOMMENDED that the client immediately delete
        the allocation and start afresh with a new allocation.[¶](#section-12.3-2)

### 
[12.4.](#section-12.4) [The ChannelData Message](#name-the-channeldata-message)
        

The ChannelData message is used to carry application data between
        the client and the server. It has the following format:[¶](#section-12.4-1)

The Channel Number field specifies the number of the channel on
        which the data is traveling, and thus, the address of the peer that is
        sending or is to receive the data.[¶](#section-12.4-3)

The Length field specifies the length in bytes of the application
        data field (i.e., it does not include the size of the ChannelData
        header). Note that 0 is a valid length.[¶](#section-12.4-4)

The Application Data field carries the data the client is trying to
        send to the peer, or that the peer is sending to the client.[¶](#section-12.4-5)

### 
[12.5.](#section-12.5) [Sending a ChannelData Message](#name-sending-a-channeldata-messa)
        

Once a client has bound a channel to a peer, then when the client
        has data to send to that peer, it may use either a ChannelData message
        or a Send indication; that is, the client is not obligated to use the
        channel when it exists and may freely intermix the two message types
        when sending data to the peer. The server, on the other hand, MUST use
        the ChannelData message if a channel has been bound to the peer. The
        server uses a Data indication to signal the XOR-[¶](#section-12.5-1)

The fields of the ChannelData message are filled in as described in
        [Section 12.4](#sec-channeldata-msg).[¶](#section-12.5-2)

Over TCP and TLS-over-TCP, the ChannelData message MUST be padded
        to a multiple of four bytes in order to ensure the alignment of
        subsequent messages. The padding is not reflected in the length field
        of the ChannelData message, so the actual size of a ChannelData
        message (including padding) is (4 + Length) rounded up to the nearest
        multiple of 4 (see [Section 14](/info/rfc8489/#section-14) of [[RFC8489](#RFC8489)]). Over UDP, the padding is not
        required but MAY be included.[¶](#section-12.5-3)

The ChannelData message is then sent on the 5-tuple associated with
        the allocation.[¶](#section-12.5-4)

### 
[12.6.](#section-12.6) [Receiving a ChannelData Message](#name-receiving-a-channeldata-mes)
        

The receiver of the ChannelData message uses the first byte to
        distinguish it from other multiplexed protocols as described in [Table 3](#fig-demultiplexing). If the message uses a
        value in the reserved range (0x5000 through 0xFFFF), then the message
        is silently discarded.[¶](#section-12.6-1)

If the ChannelData message is received in a UDP datagram, and if
        the UDP datagram is too short to contain the claimed length of the
        ChannelData message (i.e., the UDP header length field value is less
        than the ChannelData header length field value + 4 + 8), then the
        message is silently discarded.[¶](#section-12.6-2)

If the ChannelData message is received over TCP or over
        TLS-over-TCP, then the actual length of the ChannelData message is as
        described in [Section 12.5](#sec-sending-channeldata-msg).[¶](#section-12.6-3)

If the ChannelData message is received on a channel that is not
        bound to any peer, then the message is silently discarded.[¶](#section-12.6-4)

On the client, it is RECOMMENDED that the client discard the
        ChannelData message if the client believes there is no active
        permission towards the peer. On the server, the receipt of a
        ChannelData message MUST NOT refresh either the channel binding or the
        permission towards the peer.[¶](#section-12.6-5)

On the server, if no errors are detected, the server relays the
        application data to the peer by forming a UDP datagram as
        follows:[¶](#section-12.6-6)

- the source transport address is the relayed transport address
            of the allocation, where the allocation is determined by the
            5-tuple on which the ChannelData message arrived;[¶](#section-12.6-7.1)
- the destination transport address is the transport address to
            which the channel is bound;[¶](#section-12.6-7.2)
- the data following the UDP header is the contents of the data
            field of the ChannelData message.[¶](#section-12.6-7.3)

The resulting UDP datagram is then sent to the peer. Note
        that if the Length field in the ChannelData message is 0, then there
        will be no data in the UDP datagram, but the UDP datagram is still
        formed and sent ([Section 4.1](/info/rfc6263/#section-4.1) of [[RFC6263](#RFC6263)]).[¶](#section-12.6-8)

### 
[12.7.](#section-12.7) [Relaying Data from the Peer](#name-relaying-data-from-the-peer)
        

When the server receives a UDP datagram on the relayed transport
        address associated with an allocation, the server processes it as
        described in [Section 11.3](#sec-sending-data-indication). If
        that section indicates that a ChannelData message should be sent
        (because there is a channel bound to the peer that sent to the UDP
        datagram), then the server forms and sends a ChannelData message as
        described in [Section 12.5](#sec-sending-channeldata-msg).[¶](#section-12.7-1)

When the server receives an ICMP packet, the server processes it as
        described in [Section 11.5](#sec-sending-senderror-indication).[¶](#section-12.7-2)

## 
[13.](#section-13) [Packet Translations](#name-packet-translations)
      

This section addresses IPv4-to-IPv6, IPv6-to-IPv4, and IPv6-to-IPv6
      translations. Requirements for translation of the IP addresses and port
      numbers of the packets are described above. The following sections
      specify how to translate other header fields.[¶](#section-13-1)

As discussed in [Section 3.6](#unpriv), translations in TURN
      are designed so that a TURN server can be implemented as an application
      that runs in user space under commonly available operating systems and
      that does not require special privileges. The translations specified in
      the following sections follow this principle.[¶](#section-13-2)

The descriptions below have two parts: a preferred behavior and an
      alternate behavior. The server SHOULD implement the preferred behavior,
      but if that is not possible for a particular field, the server MUST
      implement the alternate behavior and MUST NOT do anything else for the
      reasons detailed in [[RFC7915](#RFC7915)]. The TURN server
      solely relies on the DF bit in the IPv4 header and the Fragment header
      in the IPv6 header to handle fragmentation using the approach described in
      [[RFC7915](#RFC7915)] and does not rely on the DONT-FRAGMENT
      attribute; ignoring the DONT-FRAGMENT attribute is only applicable for UDP-to-UDP
      relay and not for TCP-to-UDP relay.[¶](#section-13-3)

### 
[13.1.](#section-13.1) [IPv4-to-IPv6 Translations](#name-ipv4-to-ipv6-translations)
        

Time to Live (TTL) field[¶](#section-13.1-1)

- Preferred Behavior: As specified in [Section 4](/info/rfc7915/#section-4) of [[RFC7915](#RFC7915) ].[¶](#section-13.1-2.1)
- Alternate Behavior: Set the outgoing value to the default for
            outgoing packets.[¶](#section-13.1-2.2)

Traffic Class[¶](#section-13.1-3)

- Preferred behavior: As specified in [Section 4](/info/rfc7915/#section-4) of [[RFC7915](#RFC7915) ].[¶](#section-13.1-4.1)
- Alternate behavior: The TURN server sets the Traffic Class to
            the default value for outgoing packets.[¶](#section-13.1-4.2)

Flow Label[¶](#section-13.1-5)

- Preferred behavior: The TURN server can use the 5-tuple of
            relayed transport address, peer transport address, and UDP protocol
            number to identify each flow and to generate and set the flow
            label value in the IPv6 packet as discussed in [Section 3](/info/rfc6437/#section-3) of [[RFC6437](#RFC6437) ]. If the TURN server is incapable of
            generating the flow label value from the IPv6 packet's 5-tuple, it
            sets the Flow label to zero.[¶](#section-13.1-6.1)
- Alternate behavior: The alternate behavior is the same as the
            preferred behavior for a TURN server that does not support flow
            labels.[¶](#section-13.1-6.2)

Hop Limit[¶](#section-13.1-7)

- Preferred behavior: As specified in [Section 4](/info/rfc7915/#section-4) of [[RFC7915](#RFC7915) ].[¶](#section-13.1-8.1)
- Alternate behavior: The TURN server sets the Hop Limit to the
            default value for outgoing packets.[¶](#section-13.1-8.2)

Fragmentation[¶](#section-13.1-9)

- Preferred behavior: As specified in [Section 4](/info/rfc7915/#section-4) of [[RFC7915](#RFC7915) ].[¶](#section-13.1-10.1)
- Alternate behavior: The TURN server assembles incoming
            fragments. The TURN server follows its default behavior to send
            outgoing packets.[¶](#section-13.1-10.2)
- For both preferred and alternate behavior, the DONT-FRAGMENT
            attribute MUST be ignored by the server.[¶](#section-13.1-10.3)

Extension Headers[¶](#section-13.1-11)

### 
[13.2.](#section-13.2) [IPv6-to-IPv6 Translations](#name-ipv6-to-ipv6-translations)
        

Flow Label[¶](#section-13.2-1)

NOTE: The TURN server should consider that it is handling two different
        IPv6 flows. Therefore, the Flow label [[RFC6437](#RFC6437)]
          SHOULD NOT be copied as part of the translation.[¶](#section-13.2-2)

- Preferred behavior: The TURN server can use the 5-tuple of relayed
  transport address, peer transport address, and UDP protocol number to
  identify each flow and to generate and set the flow label value in the IPv6
  packet as discussed in [Section 3](/info/rfc6437/#section-3) of [[RFC6437](#RFC6437) ]. If the TURN server is incapable of generating the flow
  label value from the IPv6 packet's 5-tuple, it sets the Flow label to
  zero.[¶](#section-13.2-3.1)
- Alternate behavior: The alternate behavior is the same as the
            preferred behavior for a TURN server that does not support flow
            labels.[¶](#section-13.2-3.2)

Hop Limit[¶](#section-13.2-4)

- Preferred behavior: The TURN server acts as a regular router
            with respect to decrementing the Hop Limit and generating an
            ICMPv6 error if it reaches zero.[¶](#section-13.2-5.1)
- Alternate behavior: The TURN server sets the Hop Limit to the
            default value for outgoing packets.[¶](#section-13.2-5.2)

Fragmentation[¶](#section-13.2-6)

- Preferred behavior: If the incoming packet did not include a
            Fragment header and the outgoing packet size does not exceed the
            outgoing link's MTU, the TURN server sends the outgoing packet
            without a Fragment header.[¶](#section-13.2-7.1)
- If the incoming packet did not include a Fragment header and
            the outgoing packet size exceeds the outgoing link's MTU, the TURN
            server drops the outgoing packet and sends an ICMP message of type
            2 code 0 ("Packet too big") to the sender of the incoming packet.
            If the ICMPv6 packet ("Packet too big") is being sent to the peer,
            the TURN server SHOULD reduce the MTU reported in the ICMP message
            by 48 bytes to allow room for the overhead of a Data
            indication.[¶](#section-13.2-7.2)
- If the incoming packet included a Fragment header and the
            outgoing packet size (with a Fragment header included) does not
            exceed the outgoing link's MTU, the TURN server sends the outgoing
            packet with a Fragment header. The TURN server sets the fields of
            the Fragment header as appropriate for a packet originating from
            the server.[¶](#section-13.2-7.3)
- If the incoming packet included a Fragment header and the
            outgoing packet size exceeds the outgoing link's MTU, the TURN
            server MUST fragment the outgoing packet into fragments of no more
            than 1280 bytes. The TURN server sets the fields of the Fragment
            header as appropriate for a packet originating from the
            server.[¶](#section-13.2-7.4)
- Alternate behavior: The TURN server assembles incoming
            fragments. The TURN server follows its default behavior to send
            outgoing packets.[¶](#section-13.2-7.5)
- For both preferred and alternate behavior, the DONT-FRAGMENT
            attribute MUST be ignored by the server.[¶](#section-13.2-7.6)

Extension Headers[¶](#section-13.2-8)

### 
[13.3.](#section-13.3) [IPv6-to-IPv4 Translations](#name-ipv6-to-ipv4-translations)
        

Type of Service and Precedence[¶](#section-13.3-1)

- Preferred behavior: As specified in [Section 5](/info/rfc7915/#section-5) of [[RFC7915](#RFC7915) ].[¶](#section-13.3-2.1)
- Alternate behavior: The TURN server sets the Type of Service
            and Precedence to the default value for outgoing packets.[¶](#section-13.3-2.2)

Time to Live[¶](#section-13.3-3)

- Preferred behavior: As specified in [Section 5](/info/rfc7915/#section-5) of [[RFC7915](#RFC7915) ].[¶](#section-13.3-4.1)
- Alternate behavior: The TURN server sets the Time to Live to
            the default value for outgoing packets.[¶](#section-13.3-4.2)

Fragmentation[¶](#section-13.3-5)

- Preferred behavior: As specified in [Section 5](/info/rfc7915/#section-5) of [[RFC7915](#RFC7915) ]. Additionally, when the outgoing packet's
            size exceeds the outgoing link's MTU, the TURN server needs to
            generate an ICMP error (ICMPv6 "Packet too big") reporting the MTU
            size. If the ICMPv4 packet (Destination Unreachable (Type 3) with
            Code 4) is being sent to the peer, the TURN server SHOULD reduce
            the MTU reported in the ICMP message by 48 bytes to allow room for
            the overhead of a Data indication.[¶](#section-13.3-6.1)
- Alternate behavior: The TURN server assembles incoming
            fragments. The TURN server follows its default behavior to send
            outgoing packets.[¶](#section-13.3-6.2)
- For both preferred and alternate behavior, the DONT-FRAGMENT
            attribute MUST be ignored by the server.[¶](#section-13.3-6.3)

## 
[14.](#section-14) [UDP-to-UDP Relay](#name-udp-to-udp-relay)
      

This section describes how the server sets various fields in the IP
      header for UDP-to-UDP relay from the client to the peer or vice versa.
      The descriptions in this section apply (a) when the server sends a UDP
      datagram to the peer or (b) when the server sends a Data indication or
      ChannelData message to the client over UDP transport. The descriptions
      in this section do not apply to TURN messages sent over TCP or TLS
      transport from the server to the client.[¶](#section-14-1)

The descriptions below have two parts: a preferred behavior and an
      alternate behavior. The server SHOULD implement the preferred behavior,
      but if that is not possible for a particular field, then it SHOULD
      implement the alternative behavior.[¶](#section-14-2)

Differentiated Services Code Point (DSCP) field [[RFC2474](#RFC2474)][¶](#section-14-3)

- Preferred Behavior: Set the outgoing value to the incoming value
          unless the server includes a differentiated services classifier and
          marker [[RFC2474](#RFC2474) ].[¶](#section-14-4.1)
- Alternate Behavior: Set the outgoing value to a fixed value,
          which by default is Best Effort unless configured otherwise.[¶](#section-14-4.2)
- In both cases, if the server is immediately adjacent to a
          differentiated services classifier and marker, then DSCP MAY be set
          to any arbitrary value in the direction towards the classifier.[¶](#section-14-4.3)

Explicit Congestion Notification (ECN) field [[RFC3168](#RFC3168)][¶](#section-14-5)

- Preferred Behavior: Set the outgoing value to the incoming value.
          The server may perform Active Queue Management, in which case it
          SHOULD behave as an ECN-aware router [[RFC3168](#RFC3168) ]
          and can mark traffic with Congestion Experienced (CE) instead of
          dropping the packet. The use of ECT(1) is subject to experimental
          usage [[RFC8311](#RFC8311) ].[¶](#section-14-6.1)
- Alternate Behavior: Set the outgoing value to Not-ECT
          (=0b00).[¶](#section-14-6.2)

IPv4 Fragmentation fields (applicable only for IPv4-to-IPv4
      relay)[¶](#section-14-7)

- Preferred Behavior: When the server sends a packet to a peer in
          response to a Send indication containing the DONT-FRAGMENT
          attribute, then set the outgoing UDP packet to not fragment. In all
          other cases, when sending an outgoing packet containing application
          data (e.g., Data indication, a ChannelData message, or the DONT-FRAGMENT
          attribute not included in the Send indication), copy the DF bit from
          the DF bit of the incoming packet that contained the application
          data.[¶](#section-14-8.1)
- Set the other fragmentation fields (Identification, More
          Fragments, Fragment Offset) as appropriate for a packet originating
          from the server.[¶](#section-14-8.2)
- Alternate Behavior: As described in the Preferred Behavior,
          except always assume the incoming DF bit is 0.[¶](#section-14-8.3)
- In both the Preferred and Alternate Behaviors, the resulting
          packet may be too large for the outgoing link. If this is the case,
          then the normal fragmentation rules apply [[RFC1122](#RFC1122) ].[¶](#section-14-8.4)

IPv4 Options[¶](#section-14-9)

## 
[15.](#section-15) [TCP-to-UDP Relay](#name-tcp-to-udp-relay)
      

This section describes how the server sets various fields in the IP
      header for TCP-to-UDP relay from the client to the peer. The
      descriptions in this section apply when the server sends a UDP datagram
      to the peer. Note that the server does not perform per-packet
      translation for TCP-to-UDP relaying.[¶](#section-15-1)

Multipath TCP [[TCP-EXT](#I-D.ietf-mptcp-rfc6824bis)] is not supported by this version of TURN because TCP
      multipath is not used by either SIP or WebRTC protocols [[RFC7478](#RFC7478)] for media and non-media data. TCP
      connection between the TURN client and server can use the TCP
      Authentication Option (TCP-AO) [[RFC5925](#RFC5925)], but UDP does not provide a similar type of
      authentication, though it might be added in the future [[UDP-OPT](#I-D.ietf-tsvwg-udp-options)]. Even if both
      TCP-AO and UDP authentication would be used between TURN client and
      server, it would not change the end-to-end security properties of the
      application payload being relayed. Therefore, applications using TURN
      will need to secure their application data end to end appropriately,
      e.g., Secure Real-time Transport Protocol (SRTP) for RTP
      applications. Note that the TCP-AO option obsoletes the TCP MD5
      option.[¶](#section-15-2)

Unlike UDP, TCP without the TCP Fast Open extension [[RFC7413](#RFC7413)] does not support 0-RTT session
      resumption. The TCP user timeout [[RFC5482](#RFC5482)] equivalent for application data relayed by the TURN
      is the use of RTP control protocol (RTCP). As a reminder, RTCP is a
      fundamental and integral part of RTP.[¶](#section-15-3)

The descriptions below have two parts: a preferred behavior and an
      alternate behavior. The server SHOULD implement the preferred behavior,
      but if that is not possible for a particular field, then it SHOULD
      implement the alternative behavior.[¶](#section-15-4)

For the UDP datagram sent to the peer based on a Send Indication or
      ChannelData message arriving at the TURN server over a TCP Transport,
      the server sets various fields in the IP header as follows:[¶](#section-15-5)

Differentiated Services Code Point (DSCP) field [[RFC2474](#RFC2474)][¶](#section-15-6)

- Preferred Behavior: The TCP connection can only use a single DSCP,
          so inter-flow differentiation is not possible; see
          [Section 5.1](/info/rfc7657/#section-5.1) of [[RFC7657](#RFC7657) ]. The server sets the
          outgoing value to the DSCP used by the TCP connection,
          unless the server includes a differentiated services classifier and
          marker [[RFC2474](#RFC2474) ].[¶](#section-15-7.1)
- Alternate Behavior: Set the outgoing value to a fixed value,
          which by default is Best Effort unless configured otherwise.[¶](#section-15-7.2)
- In both cases, if the server is immediately adjacent to a
          differentiated services classifier and marker, then DSCP MAY be set
          to any arbitrary value in the direction towards the classifier.[¶](#section-15-7.3)

Explicit Congestion Notification (ECN) field [[RFC3168](#RFC3168)][¶](#section-15-8)

- Preferred Behavior: No mechanism is defined to indicate what ECN
          value should be used for the outgoing UDP datagrams of an
          allocation; therefore, set the outgoing value to Not-ECT (=0b00).[¶](#section-15-9.1)
- Alternate Behavior: Same as preferred.[¶](#section-15-9.2)

IPv4 Fragmentation fields (applicable only for IPv4-to-IPv4
      relay)[¶](#section-15-10)

- Preferred Behavior: When the server sends a packet to a peer in
          response to a Send indication containing the DONT-FRAGMENT
          attribute, set the outgoing UDP packet to not fragment. In all
          other cases, when sending an outgoing UDP packet containing
          application data (e.g., Data indication, ChannelData message, or
          DONT-FRAGMENT attribute not included in the Send indication), set
          the DF bit in the outgoing IP header to 0.[¶](#section-15-11.1)
- Alternate Behavior: Same as preferred.[¶](#section-15-11.2)

IPv6 Fragmentation fields[¶](#section-15-12)

- Preferred Behavior: If the TCP traffic arrives over IPv6, the
          server relies on the presence of the DONT-FRAGMENT attribute in the send
          indication to set the outgoing UDP packet to not fragment.[¶](#section-15-13.1)
- Alternate Behavior: Same as preferred.[¶](#section-15-13.2)

IPv4 Options[¶](#section-15-14)

## 
[16.](#section-16) [UDP-to-TCP Relay](#name-udp-to-tcp-relay)
      

This section describes how the server sets various fields in the IP
      header for UDP-to-TCP relay from the peer to the client. The
      descriptions in this section apply when the server sends a Data
      indication or ChannelData message to the client over TCP or TLS
      transport. Note that the server does not perform per-packet translation
      for UDP-to-TCP relaying.[¶](#section-16-1)

The descriptions below have two parts: a preferred behavior and an
      alternate behavior. The server SHOULD implement the preferred behavior,
      but if that is not possible for a particular field, then it SHOULD
      implement the alternative behavior.[¶](#section-16-2)

The TURN server sets IP header fields in the TCP packets on a
      per-connection basis for the TCP connection as follows:[¶](#section-16-3)

Differentiated Services Code Point (DSCP) field [[RFC2474](#RFC2474)][¶](#section-16-4)

- Preferred Behavior: Ignore the incoming DSCP value. When TCP is
          used between the client and the server, a single DSCP should be used
          for all traffic on that TCP connection. Note, TURN/ICE occurs before
          application data is exchanged.[¶](#section-16-5.1)
- Alternate Behavior: Same as preferred.[¶](#section-16-5.2)

Explicit Congestion Notification (ECN) field [[RFC3168](#RFC3168)][¶](#section-16-6)

- Preferred Behavior: Ignore; ECN signals are dropped in the TURN
          server for the incoming UDP datagrams from the peer.[¶](#section-16-7.1)
- Alternate Behavior: Same as preferred.[¶](#section-16-7.2)

Fragmentation[¶](#section-16-8)

- Preferred Behavior: Any fragmented packets are reassembled in the
          server and then forwarded to the client over the TCP connection.
          ICMP messages resulting from the UDP datagrams sent to the peer are
          processed by the server as described in [Section 11.5](#sec-sending-senderror-indication) and forwarded to
          the client using TURN's mechanism for relevant ICMP types and
          codes.[¶](#section-16-9.1)
- Alternate Behavior: Same as preferred.[¶](#section-16-9.2)

Extension Headers[¶](#section-16-10)

- Preferred behavior: The outgoing packet uses the system defaults
          for IPv6 extension headers.[¶](#section-16-11.1)
- Alternate behavior: Same as preferred.[¶](#section-16-11.2)

IPv4 Options[¶](#section-16-12)

## 
[17.](#section-17) [STUN Methods](#name-stun-methods)
      

This section lists the code points for the STUN methods defined in
      this specification. See elsewhere in this document for the semantics of
      these methods.[¶](#section-17-1)

| Table 4 |  |  | 
|---|---|---|
| 0x003 | Allocate | (only request/response semantics defined) | 
| 0x004 | Refresh | (only request/response semantics defined) | 
| 0x006 | Send | (only indication semantics defined) | 
| 0x007 | Data | (only indication semantics defined) | 
| 0x008 | Create | (only request/response semantics defined) | 
| 0x009 | ChannelBind | (only request/response semantics defined) | 

[Table 4](#table-4)

## 
[18.](#section-18) [STUN Attributes](#name-stun-attributes)
      

This STUN extension defines the following
        attributes:[¶](#section-18-1)

| Table 5 |  | 
|---|---|
| 0x000C | CHANNEL-NUMBER | 
| 0x000D | LIFETIME | 
| 0x0010 | Reserved (was BANDWIDTH) | 
| 0x0012 | XOR- | 
| 0x0013 | DATA | 
| 0x0016 | XOR- | 
| 0x0017 | REQUESTED- | 
| 0x0018 | EVEN-PORT | 
| 0x0019 | REQUESTED- | 
| 0x001A | DONT-FRAGMENT | 
| 0x0021 | Reserved (was TIMER-VAL) | 
| 0x0022 | RESERVATION- | 
| 0x8000 | ADDITIONAL- | 
| 0x8001 | ADDRESS- | 
| 0x8004 | ICMP | 

[Table 5](#table-5)

Some of these attributes have lengths that are not multiples of 4. By
      the rules of STUN, any attribute whose length is not a multiple of 4
      bytes MUST be immediately followed by 1 to 3 padding bytes to ensure the
      next attribute (if any) would start on a 4-byte boundary (see [[RFC8489](#RFC8489)]).[¶](#section-18-3)

### 
[18.1.](#section-18.1) [CHANNEL-NUMBER](#name-channel-number)
        

The CHANNEL-NUMBER attribute contains the number of the channel.
        The value portion of this attribute is 4 bytes long and consists of a
        16-bit unsigned integer followed by a two-octet RFFU (Reserved For
        Future Use) field, which MUST be set to 0 on transmission and MUST be
        ignored on reception.[¶](#section-18.1-1)

### 
[18.2.](#section-18.2) [LIFETIME](#name-lifetime)
        

The LIFETIME attribute represents the duration for which the server
        will maintain an allocation in the absence of a refresh. The TURN
        client can include the LIFETIME attribute with the desired lifetime in
        Allocate and Refresh requests. The value portion of this attribute is
        4 bytes long and consists of a 32-bit unsigned integral value
        representing the number of seconds remaining until expiration.[¶](#section-18.2-1)

### 
[18.3.](#section-18.3) [XOR-PEER-](#name-xor-peer-address)
        

The XOR-[RFC8489](#RFC8489)].[¶](#section-18.3-1)

### 
[18.4.](#section-18.4) [DATA](#name-data)
        

The DATA attribute is present in all Send indications. If the ICMP
        attribute is not present in a Data indication, it contains a DATA
        attribute. The value portion of this attribute is variable length and
        consists of the application data (that is, the data that would
        immediately follow the UDP header if the data was sent directly
        between the client and the peer). The application data is equivalent
        to the "UDP user data" and does not include the "surplus area" defined
        in [Section 4](https://tools.ietf.org/html/draft-ietf-tsvwg-udp-options-08#section-4) of [[UDP-OPT](#I-D.ietf-tsvwg-udp-options)]. If
        the length of this attribute is not a multiple of 4, then padding must
        be added after this attribute.[¶](#section-18.4-1)

### 
[18.5.](#section-18.5) [XOR-RELAYED-](#name-xor-relayed-address)
        

The XOR-[RFC8489](#RFC8489)].[¶](#section-18.5-1)

### 
[18.6.](#section-18.6) [REQUESTED-ADDRESS-](#name-requested-address-family)
        

This attribute is used in Allocate and Refresh requests to specify
        the address type requested by the client. The value of this attribute
        is 4 bytes with the following format:[¶](#section-18.6-1)

- Family:
- There are two values defined for this field and specified in
          [Section 14.1](/info/rfc8489/#section-14.1) of [[RFC8489](#RFC8489) ]: 0x01 for
          IPv4 addresses and 0x02 for IPv6 addresses.[¶](#section-18.6-3.2)
- Reserved:
- At this point, the 24 bits in the Reserved
            field MUST be set to zero by the client and MUST be ignored by the
            server.[¶](#section-18.6-3.4)

### 
[18.7.](#section-18.7) [EVEN-PORT](#name-even-port)
        

This attribute allows the client to request that the port in the
        relayed transport address be even and (optionally) that the server
        reserve the next-higher port number. The value portion of this
        attribute is 1 byte long. Its format is:[¶](#section-18.7-1)

The value contains a single 1-bit flag:[¶](#section-18.7-3)

- R:
- If 1, the server is requested to reserve the
            next-higher port number (on the same IP address) for a subsequent
            allocation. If 0, no such reservation is requested.[¶](#section-18.7-4.2)
- RFFU:
- Reserved For Future Use.[¶](#section-18.7-4.4)

The RFFU field must be set to zero on transmission and
        ignored on reception.[¶](#section-18.7-5)

Since the length of this attribute is not a multiple of 4, padding
        must immediately follow this attribute.[¶](#section-18.7-6)

### 
[18.8.](#section-18.8) [REQUESTED-TRANSPORT](#name-requested-transport)
        

This attribute is used by the client to request a specific
        transport protocol for the allocated transport address. The value of
        this attribute is 4 bytes with the following format:[¶](#section-18.8-1)

The Protocol field specifies the desired protocol. The code points
        used in this field are taken from those allowed in the Protocol field
        in the IPv4 header and the NextHeader field in the IPv6 header [[PROTOCOL-](#PROTOCOL-NUMBERS)]. This specification only
        allows the use of code point 17 (User Datagram Protocol).[¶](#section-18.8-3)

The RFFU field MUST be set to zero on transmission and MUST be
        ignored on reception. It is reserved for future uses.[¶](#section-18.8-4)

### 
[18.9.](#section-18.9) [DONT-FRAGMENT](#name-dont-fragment)
        

This attribute is used by the client to request that the server set
        the DF (Don't Fragment) bit in the IP header when relaying the
        application data onward to the peer and for determining the server
        capability in Allocate requests. This attribute has no value part, and
        thus, the attribute length field is 0.[¶](#section-18.9-1)

### 
[18.10.](#section-18.10) [RESERVATION-TOKEN](#name-reservation-token)
        

The RESERVATION-[¶](#section-18.10-1)

The attribute value is 8 bytes and contains the token value.[¶](#section-18.10-2)

### 
[18.11.](#section-18.11) [ADDITIONAL-ADDRESS-](#name-additional-address-family)
        

This attribute is used by clients to request the allocation of an
        IPv4 and IPv6 address type from a server. It is encoded in the same
        way as the REQUESTED-[Section 18.6](#sec-requested-address-family). The
        ADDITIONAL-[¶](#section-18.11-1)

### 
[18.12.](#section-18.12) [ADDRESS-ERROR-](#name-address-error-code)
        

This attribute is used by servers to signal the reason for not
        allocating the requested address family. The value portion of this
        attribute is variable length with the following format:[¶](#section-18.12-1)

- Family:
- There are two values defined for this field and specified in
          [Section 14.1](/info/rfc8489/#section-14.1) of [[RFC8489](#RFC8489) ]: 0x01 for
          IPv4 addresses and 0x02 for IPv6 addresses.[¶](#section-18.12-3.2)
- Reserved:
- At this point, the 13 bits in the Reserved
            field MUST be set to zero by the server and MUST be ignored by the
            client.[¶](#section-18.12-3.4)
- Class:
- The Class represents the hundreds digit of
            the error code and is defined in [Section 14.8](/info/rfc8489/#section-14.8) of [[RFC8489](#RFC8489) ].[¶](#section-18.12-3.6)
- Number:
- This 8-bit field contains the reason the server
            cannot allocate one of the requested address types. The error code
            values could be either 440 (Address Family not Supported) or 508
            (Insufficient Capacity). The number representation is defined in
            [Section 14.8](/info/rfc8489/#section-14.8) of [[RFC8489](#RFC8489) ].[¶](#section-18.12-3.8)
- Reason Phrase:
- The recommended reason phrases for
            error codes 440 and 508 are explained in [Section 19](#sec-stun-errors) . The reason phrase MUST be a
            UTF-8 [[RFC3629](#RFC3629) ] encoded sequence of less than
            128 characters (which can be as long as 509 bytes when encoding
            them or 763 bytes when decoding them).[¶](#section-18.12-3.10)

### 
[18.13.](#section-18.13) [ICMP](#name-icmp)
        

This attribute is used by servers to signal the reason a UDP
        packet was dropped. The following is the format of the ICMP
        attribute.[¶](#section-18.13-1)

- Reserved:
- This field MUST be set to 0 when sent and
            MUST be ignored when received.[¶](#section-18.13-3.2)
- ICMP Type:
- The field contains the value of the ICMP
            type. Its interpretation depends on whether the ICMP was received
            over IPv4 or IPv6.[¶](#section-18.13-3.4)
- ICMP Code:
- The field contains the value of the ICMP
            code. Its interpretation depends on whether the ICMP was received
            over IPv4 or IPv6.[¶](#section-18.13-3.6)
- Error Data:
- This field size is 4 bytes long. If the ICMPv6 type is 2
          ("Packet too big" message) or ICMPv4 type is 3 (Destination
          Unreachable) and Code is 4 (fragmentation needed and DF set), the
          Error Data field will be set to the Maximum Transmission Unit of the
          next-hop link ([Section 3.2](/info/rfc4443/#section-3.2) of [[RFC4443](#RFC4443) ] and[Section 4](/info/rfc1191/#section-4) of [[RFC1191](#RFC1191) ]). For other ICMPv6 types and ICMPv4 types and
          codes, the Error Data field MUST be set to zero.[¶](#section-18.13-3.8)

## 
[19.](#section-19) [STUN Error Response Codes](#name-stun-error-response-codes)
      

This document defines the following error response codes:[¶](#section-19-1)

- 403 (Forbidden):
- The request was valid but cannot be
          performed due to administrative or similar restrictions.[¶](#section-19-2.2)
- 437 (Allocation Mismatch):
- A request was received by
          the server that requires an allocation to be in place, but no
          allocation exists, or a request was received that requires no
          allocation, but an allocation exists.[¶](#section-19-2.4)
- 440 (Address Family not Supported):
- The server does
          not support the address family requested by the client.[¶](#section-19-2.6)
- 441 (Wrong Credentials):
- (Wrong Credentials): The credentials in the
          (non-Allocate) request do not match those used to create the
          allocation.[¶](#section-19-2.8)
- 442 (Unsupported Transport Protocol):
- The Allocate
          request asked the server to use a transport protocol between the
          server and the peer that the server does not support. NOTE: This
          does NOT refer to the transport protocol used in the 5-tuple.[¶](#section-19-2.10)
- 443 (Peer Address Family Mismatch):
- A peer address is
          part of a different address family than that of the relayed
          transport address of the allocation.[¶](#section-19-2.12)
- 486 (Allocation Quota Reached):
- No more allocations
          using this username can be created at the present time.[¶](#section-19-2.14)
- 508 (Insufficient Capacity):
- The server is unable to
          carry out the request due to some capacity limit being reached. In
          an Allocate response, this could be due to the server having no more
          relayed transport addresses available at that time, having none with
          the requested properties, or the one that corresponds to the
          specified reservation token is not available.[¶](#section-19-2.16)

## 
[20.](#section-20) [Detailed Example](#name-detailed-example)
      

This section gives an example of the use of TURN, showing in detail
      the contents of the messages exchanged. The example uses the network
      diagram shown in the Overview ([Figure 1](#fig-turn-model)).[¶](#section-20-1)

For each message, the attributes included in the message and their
      values are shown. For convenience, values are shown in a human-readable
      format rather than showing the actual octets; for example,
      "XOR-[¶](#section-20-2)

The client begins by selecting a host transport address to use for
      the TURN session; in this example, the client has selected
      198[Figure 1](#fig-turn-model).
      The client then sends an Allocate request to the server at the server
      transport address. The client randomly selects a 96-bit transaction id
      of 0xA56250D3[¶](#section-20-4)

Servers require any request to be authenticated. Thus, when the
      server receives the initial Allocate request, it rejects the request
      because the request does not contain the authentication attributes.
      Following the procedures of the long-term credential mechanism of STUN
      [[RFC8489](#RFC8489)], the server includes an
      ERROR-CODE attribute with a value of 401 (Unauthorized), a REALM
      attribute that specifies the authentication realm used by the server (in
      this case, the server's domain "example[¶](#section-20-5)

The client, upon receipt of the 401 error, reattempts the Allocate
      request, this time including the authentication attributes. The client
      selects a new transaction id and then populates the new Allocate
      request with the same attributes as before. The client includes a
      USERNAME attribute and uses the realm value received from the server to
      help it determine which value to use; here, the client is configured to
      use the username "George" for the realm "example[¶](#section-20-6)

The server, upon receipt of the authenticated Allocate request,
      checks that everything is OK, then creates an allocation. The server
      replies with an Allocate success response. The server includes a
      LIFETIME attribute giving the lifetime of the allocation; here, the
      server has reduced the client's requested 1-hour lifetime to just 20
      minutes because this particular server doesn't allow lifetimes longer
      than 20 minutes. The server includes an XOR-[¶](#section-20-7)

The client then creates a permission towards Peer A in preparation
      for sending it some application data. This is done through a
      Create[¶](#section-20-9)

The server receives the Create[¶](#section-20-10)

The client now sends application data to Peer A using a Send
      indication. Peer A's server-[¶](#section-20-12)

Upon receipt of the Send indication, the server extracts the
      application data and sends it in a UDP datagram to Peer A, with the
      relayed transport address as the source transport address of the
      datagram and with the DF bit set as requested. Note that had the
      client not previously established a permission for Peer A's
      server-[¶](#section-20-13)

Peer A then replies with its own UDP datagram containing application
      data. The datagram is sent to the relayed transport address on the
      server. When this arrives, the server creates a Data indication
      containing the source of the UDP datagram in the XOR-[¶](#section-20-14)

The client now binds a channel to Peer B, specifying a free channel
      number (0x4000) in the CHANNEL-NUMBER attribute, and Peer B's transport
      address in the XOR-[¶](#section-20-16)

Upon receipt of the request, the server binds the channel number to
      the peer, installs a permission for Peer B's IP address, and then
      replies with a ChannelBind success response.[¶](#section-20-17)

The client now sends a ChannelData message to the server with data
      destined for Peer B. The ChannelData message is not a STUN message;
      thus, it has no transaction id. Instead, it has only three fields: a channel
      number, data, and data length; here, the channel number field is 0x4000
      (the channel the client just bound to Peer B). When the server receives
      the ChannelData message, it checks that the channel is currently bound
      (which it is) and then sends the data onward to Peer B in a UDP
      datagram, using the relayed transport address as the source transport
      address, and 192.0.2[¶](#section-20-19)

Later, Peer B sends a UDP datagram back to the relayed transport
      address. This causes the server to send a ChannelData message to the
      client containing the data from the UDP datagram. The server knows to
      which client to send the ChannelData message because of the relayed
      transport address at which the UDP datagram arrived, and it knows to use
      channel 0x4000 because this is the channel bound to 192.0.2[¶](#section-20-20)

The channel binding lasts for 10 minutes unless refreshed. The TURN
      client refreshes the binding by sending a ChannelBind request rebinding
      the channel to the same peer (Peer B's IP address). The server processes
      the ChannelBind request, rebinds the channel to the same peer, and resets
      the time-to-expiry timer back to 10 minutes.[¶](#section-20-22)

Sometime before the 20-minute lifetime is up, the client refreshes
      the allocation. This is done using a Refresh request. As before, the
      client includes the latest username, realm, and nonce values in the
      request. The client also includes the SOFTWARE attribute, following the
      recommended practice of always including this attribute in Allocate and
      Refresh messages. When the server receives the Refresh request, it
      notices that the nonce value has expired and so replies with a 438 (Stale
      Nonce) error given a new nonce value. The client then reattempts the
      request, this time with the new nonce value. This second attempt is
      accepted, and the server replies with a success response. Note that the
      client did not include a LIFETIME attribute in the request, so the
      server refreshes the allocation for the default lifetime of 10 minutes
      (as can be seen by the LIFETIME attribute in the success response).[¶](#section-20-24)

## 
[21.](#section-21) [Security Considerations](#name-security-considerations)
      

This section considers attacks that are possible in a TURN
      deployment and discusses how they are mitigated by mechanisms in the
      protocol or recommended practices in the implementation.[¶](#section-21-1)

Most of the attacks on TURN are mitigated by the server requiring
      requests be authenticated. Thus, this specification requires the use of
      authentication. The mandatory-[¶](#section-21-2)

### 
[21.1.](#section-21.1) [Outsider Attacks](#name-outsider-attacks)
        

Outsider attacks are ones where the attacker has no credentials in
        the system and is attempting to disrupt the service seen by the
        client or the server.[¶](#section-21.1-1)

#### 
[21.1.1.](#section-21.1.1) [Obtaining Unauthorized Allocations](#name-obtaining-unauthorized-allo)
          

An attacker might wish to obtain allocations on a TURN server for
          any number of nefarious purposes. A TURN server provides a mechanism
          for sending and receiving packets while cloaking the actual IP
          address of the client. This makes TURN servers an attractive target
          for attackers who wish to use it to mask their true identity.[¶](#section-21.1.1-1)

An attacker might also wish to simply utilize the services of a
          TURN server without paying for them. Since TURN services require
          resources from the provider, it is anticipated that their usage will
          come with a cost.[¶](#section-21.1.1-2)

These attacks are prevented using the long-term credential
          mechanism, which allows the TURN server to determine the identity of
          the requestor and whether the requestor is allowed to obtain the
          allocation.[¶](#section-21.1.1-3)

#### 
[21.1.2.](#section-21.1.2) [Offline Dictionary Attacks](#name-offline-dictionary-attacks)
          

The long-term credential mechanism used by TURN is subject to
          offline dictionary attacks. An attacker that is capable of
          eavesdropping on a message exchange between a client and server can
          determine the password by trying a number of candidate passwords and
          seeing if one of them is correct. This attack works when the
          passwords are low entropy such as a word from the dictionary. This
          attack can be mitigated by using strong passwords with large
          entropy. In situations where even stronger mitigation is required,
          (D)TLS transport between the client and the server can be used.[¶](#section-21.1.2-1)

#### 
[21.1.3.](#section-21.1.3) [Faked Refreshes and Permissions](#name-faked-refreshes-and-permiss)
          

An attacker might wish to attack an active allocation by sending
          it a Refresh request with an immediate expiration in order to
          delete it and disrupt service to the client. This is prevented by
          authentication of refreshes. Similarly, an attacker wishing to send
          Create[Section 21.2](#sec-firewall).[¶](#section-21.1.3-1)

#### 
[21.1.4.](#section-21.1.4) [Fake Data](#name-fake-data)
          

An attacker might wish to send data to the client or the peer as
          if they came from the peer or client, respectively. To do that, the
          attacker can send the client a faked Data indication or ChannelData
          message, or send the TURN server a faked Send indication or
          ChannelData message.[¶](#section-21.1.4-1)

Since indications and ChannelData messages are not authenticated,
          this attack is not prevented by TURN. However, this attack is
          generally present in IP-based communications and is not
          substantially worsened by TURN. Consider a normal, non-TURN IP
          session between hosts A and B. An attacker can send packets to B as
          if they came from A by sending packets towards B with a spoofed IP
          address of A. This attack requires the attacker to know the IP
          addresses of A and B. With TURN, an attacker wishing to send packets
          towards a client using a Data indication needs to know its IP
          address (and port), the IP address and port of the TURN server, and
          the IP address and port of the peer (for inclusion in the
          XOR-[¶](#section-21.1.4-2)

These attacks are more properly mitigated by application-[RFC3711](#RFC3711)] prevents these attacks.[¶](#section-21.1.4-3)

In some situations, the TURN server may be situated in the
          network such that it is able to send to hosts to which the client
          cannot directly send. This can happen, for example, if the server is
          located behind a firewall that allows packets from outside the
          firewall to be delivered to the server, but not to other hosts
          behind the firewall. In these situations, an attacker could send the
          server a Send indication with an XOR-[¶](#section-21.1.4-4)

To mitigate this attack, TURN requires that the client establish
          a permission to a host before sending it data. Thus, an attacker can
          only attack hosts with which the client is already communicating
          unless the attacker is able to create authenticated requests.
          Furthermore, the server administrator may configure the server to
          restrict the range of IP addresses and ports to which it will relay
          data. To provide even greater security, the server administrator can
          require that the client use (D)TLS for all communication between the
          client and the server.[¶](#section-21.1.4-5)

#### 
[21.1.5.](#section-21.1.5) [Impersonating a Server](#name-impersonating-a-server)
          

When a client learns a relayed address from a TURN server, it
          uses that relayed address in application protocols to receive
          traffic. Therefore, an attacker wishing to intercept or redirect
          that traffic might try to impersonate a TURN server and provide the
          client with a faked relayed address.[¶](#section-21.1.5-1)

This attack is prevented through the long-term credential
          mechanism, which provides message integrity for responses in
          addition to verifying that they came from the server. Furthermore,
          an attacker cannot replay old server responses as the transaction id
          in the STUN header prevents this. Replay attacks are further
          thwarted through frequent changes to the nonce value.[¶](#section-21.1.5-2)

#### 
[21.1.6.](#section-21.1.6) [Eavesdropping Traffic](#name-eavesdropping-traffic)
          

If the TURN client and server use the STUN Extension for
          Third-Party Authorization [[RFC7635](#RFC7635)] (for
          example, it is used in WebRTC), the username does not reveal the real
          user's identity; the USERNAME attribute carries an ephemeral and
          unique key identifier. If the TURN client and server use the STUN
          long-term credential mechanism and the username reveals the real
          user's identity, the client MUST either use the USERHASH attribute
          instead of the USERNAME attribute to anonymize the username or use
          (D)TLS transport between the client and the server.[¶](#section-21.1.6-1)

If the TURN client and server use the STUN long-term credential
          mechanism, and realm information is privacy sensitive, TURN can be
          run over (D)TLS. As a reminder, STUN Extension for Third-Party
          Authorization does not use realm.[¶](#section-21.1.6-2)

The SOFTWARE attribute can reveal the specific software version
          of the TURN client and server to the eavesdropper, and it might possibly
          allow attacks against vulnerable software that is known to contain
          security vulnerabilities. If the software version is known to
          contain security vulnerabilities, TURN SHOULD be run over (D)TLS to
          prevent leaking the SOFTWARE attribute in clear text. If zero-day
          vulnerabilities are detected in the software version, the endpoint
          policy can be modified to mandate the use of (D)TLS until the patch
          is in place to fix the flaw.[¶](#section-21.1.6-3)

TURN concerns itself primarily with authentication and message
          integrity. Confidentiality is only a secondary concern as TURN
          control messages do not include information that is particularly
          sensitive with the exception of USERNAME, REALM, and SOFTWARE. The
          primary protocol content of the messages is the IP address of the
          peer. If it is important to prevent an eavesdropper on a TURN
          connection from learning this, TURN can be run over (D)TLS.[¶](#section-21.1.6-4)

Confidentiality for the application data relayed by TURN is best
          provided by the application protocol itself since running TURN over
          (D)TLS does not protect application data between the server and the
          peer. If confidentiality of application data is important, then the
          application should encrypt or otherwise protect its data. For
          example, for real-time media, confidentiality can be provided by
          using SRTP.[¶](#section-21.1.6-5)

#### 
[21.1.7.](#section-21.1.7) [TURN Loop Attack](#name-turn-loop-attack)
          

An attacker might attempt to cause data packets to loop
          indefinitely between two TURN servers. The attack goes as follows:
          first, the attacker sends an Allocate request to server A using the
          source address of server B. Server A will send its response to
          server B, and for the attack to succeed, the attacker must have the
          ability to either view or guess the contents of this response so
          that the attacker can learn the allocated relayed transport address.
          The attacker then sends an Allocate request to server B using the
          source address of server A. Again, the attacker must be able to view
          or guess the contents of the response so it can learn the
          allocated relayed transport address. Using the same spoofed source
          address technique, the attacker then binds a channel number on
          server A to the relayed transport address on server B and similarly
          binds the same channel number on server B to the relayed transport
          address on server A. Finally, the attacker sends a ChannelData
          message to server A.[¶](#section-21.1.7-1)

The result is a data packet that loops from the relayed transport
          address on server A to the relayed transport address on server B,
          then from server B's transport address to server A's transport
          address, and then around the loop again.[¶](#section-21.1.7-2)

This attack is mitigated as follows: by requiring all requests to
          be authenticated and/or by randomizing the port number allocated for
          the relayed transport address, the server forces the attacker to
          either intercept or view responses sent to a third party (in this
          case, the other server) so that the attacker can authenticate the
          requests and learn the relayed transport address. Without one of
          these two measures, an attacker can guess the contents of the
          responses without needing to see them, which makes the attack much
          easier to perform. Furthermore, by requiring authenticated requests,
          the server forces the attacker to have credentials acceptable to the
          server, which turns this from an outsider attack into an insider
          attack and allows the attack to be traced back to the client
          initiating it.[¶](#section-21.1.7-3)

The attack can be further mitigated by imposing a per-username
          limit on the bandwidth used to relay data by allocations owned by
          that username to limit the impact of this attack on other
          allocations. More mitigation can be achieved by decrementing the TTL
          when relaying data packets (if the underlying OS allows this).[¶](#section-21.1.7-4)

### 
[21.2.](#section-21.2) [Firewall Considerations](#name-firewall-considerations)
        

A key security consideration of TURN is that TURN should not weaken
        the protections afforded by firewalls deployed between a client and a
        TURN server. It is anticipated that TURN servers will often be present
        on the public Internet, and clients may often be inside enterprise
        networks with corporate firewalls. If TURN servers provide a
        "backdoor" for reaching into the enterprise, TURN will be blocked by
        these firewalls.[¶](#section-21.2-1)

TURN servers therefore emulate the behavior of NAT devices that
        implement address-[RFC4787](#RFC4787)],
        a property common in many firewalls as well. When a NAT or firewall
        implements this behavior, packets from an outside IP address are only
        allowed to be sent to an internal IP address and port if the internal
        IP address and port had recently sent a packet to that outside IP
        address. TURN servers introduce the concept of permissions, which
        provide exactly this same behavior on the TURN server. An attacker
        cannot send a packet to a TURN server and expect it to be relayed
        towards the client, unless the client has tried to contact the
        attacker first.[¶](#section-21.2-2)

It is important to note that some firewalls have policies that are
        even more restrictive than address-[¶](#section-21.2-3)

#### 
[21.2.1.](#section-21.2.1) [Faked Permissions](#name-faked-permissions)
          

In firewalls and NAT devices, permissions are granted implicitly
          through the traversal of a packet from the inside of the network
          towards the outside peer. Thus, a permission cannot, by definition,
          be created by any entity except one inside the firewall or NAT. With
          TURN, this restriction no longer holds. Since the TURN server sits
          outside the firewall, an attacker outside the firewall can now send
          a message to the TURN server and try to create a permission for
          itself.[¶](#section-21.2.1-1)

This attack is prevented because all messages that create
          permissions (i.e., ChannelBind and Create[¶](#section-21.2.1-2)

#### 
[21.2.2.](#section-21.2.2) [Blacklisted IP Addresses](#name-blacklisted-ip-addresses)
          

Many firewalls can be configured with blacklists that prevent a
          client behind the firewall from sending packets to, or receiving
          packets from, ranges of blacklisted IP addresses. This is
          accomplished by inspecting the source and destination addresses of
          packets entering and exiting the firewall, respectively.[¶](#section-21.2.2-1)

This feature is also present in TURN since TURN servers are
          allowed to arbitrarily restrict the range of addresses of peers that
          they will relay to.[¶](#section-21.2.2-2)

#### 
[21.2.3.](#section-21.2.3) [Running Servers on Well-Known Ports](#name-running-servers-on-well-kno)
          

A malicious client behind a firewall might try to connect to a
          TURN server and obtain an allocation that it then uses to run a
          server. For example, a client might try to run a DNS server or FTP
          server.[¶](#section-21.2.3-1)

This is not possible in TURN. A TURN server will never accept
          traffic from a peer for which the client has not installed a
          permission. Thus, peers cannot just connect to the allocated port in
          order to obtain the service.[¶](#section-21.2.3-2)

### 
[21.3.](#section-21.3) [Insider Attacks](#name-insider-attacks)
        

In insider attacks, a client has legitimate credentials but defies
        the trust relationship that goes with those credentials. These attacks
        cannot be prevented by cryptographic means but need to be considered
        in the design of the protocol.[¶](#section-21.3-1)

#### 
[21.3.1.](#section-21.3.1) [DoS against TURN Server](#name-dos-against-turn-server)
          

A client wishing to disrupt service to other clients might obtain
          an allocation and then flood it with traffic in an attempt to swamp
          the server and prevent it from servicing other legitimate clients.
          This is mitigated by the recommendation that the server limit the
          amount of bandwidth it will relay for a given username. This won't
          prevent a client from sending a large amount of traffic, but it
          allows the server to immediately discard traffic in excess.[¶](#section-21.3.1-1)

Since each allocation uses a port number on the IP address of the
          TURN server, the number of allocations on a server is finite. An
          attacker might attempt to consume all of them by requesting a large
          number of allocations. This is prevented by the recommendation that
          the server impose a limit on the number of allocations active at a
          time for a given username.[¶](#section-21.3.1-2)

#### 
[21.3.2.](#section-21.3.2) [Anonymous Relaying of Malicious Traffic](#name-anonymous-relaying-of-malic)
          

TURN servers provide a degree of anonymization. A client can send
          data to peers without revealing its own IP address. TURN servers may
          therefore become attractive vehicles for attackers to launch attacks
          against targets without fear of detection. Indeed, it is possible
          for a client to chain together multiple TURN servers such that any
          number of relays can be used before a target receives a packet.[¶](#section-21.3.2-1)

Administrators who are worried about this attack can maintain
          logs that capture the actual source IP and port of the client and
          perhaps even every permission that client installs. This will allow
          for forensic tracing to determine the original source should it be
          discovered that an attack is being relayed through a TURN
          server.[¶](#section-21.3.2-2)

#### 
[21.3.3.](#section-21.3.3) [Manipulating Other Allocations](#name-manipulating-other-allocati)
          

An attacker might attempt to disrupt service to other users of
          the TURN server by sending Refresh requests or Create[¶](#section-21.3.3-1)

### 
[21.4.](#section-21.4) [Tunnel Amplification Attack](#name-tunnel-amplification-attack)
        

An attacker might attempt to cause data packets to loop numerous
        times between a TURN server and a tunnel between IPv4 and IPv6. The
        attack goes as follows:[¶](#section-21.4-1)

Suppose an attacker knows that a tunnel endpoint will forward
        encapsulated packets from a given IPv6 address (this doesn't
        necessarily need to be the tunnel endpoint's address). Suppose he then
        spoofs two packets from this address:[¶](#section-21.4-2)

1. An Allocate request asking for a v4 address, and[¶](#section-21.4-3.1)
2. A ChannelBind request establishing a channel to the IPv4
            address of the tunnel endpoint.[¶](#section-21.4-3.2)

Then, he has set up an amplification attack:[¶](#section-21.4-4)

- The TURN server will re-encapsulate IPv6 UDP data in v4 and
            send it to the tunnel endpoint.[¶](#section-21.4-5.1)
- The tunnel endpoint will de-encapsulate packets from the v4
            interface and send them to v6.[¶](#section-21.4-5.2)

So, if the attacker sends a packet of the following form:[¶](#section-21.4-6)

then the TURN server and the tunnel endpoint will send it
        back and forth until the last TURN header is consumed, at which point
        the TURN server will send an empty packet that the tunnel endpoint
        will drop.[¶](#section-21.4-8)

The amplification potential here is limited by the MTU, so it's not
        huge: IPv6+UDP+TURN takes 334 bytes, so a four-to-one amplification
        out of a 1500-byte packet is possible. But, the attacker could still
        increase traffic volume by sending multiple packets or by establishing
        multiple channels spoofed from different addresses behind the same
        tunnel endpoint.[¶](#section-21.4-9)

The attack is mitigated as follows. It is RECOMMENDED that TURN
        servers not accept allocation or channel-[¶](#section-21.4-10)

### 
[21.5.](#section-21.5) [Other Considerations](#name-other-considerations)
        

Any relay addresses learned through an Allocate request will not
        operate properly with IPsec Authentication Header (AH) [[RFC4302](#RFC4302)] in transport or tunnel
        mode. However, tunnel-mode IPsec Encapsulating Security Payload (ESP)
        [[RFC4303](#RFC4303)] should still operate.[¶](#section-21.5-1)

## 
[22.](#section-22) [IANA Considerations](#name-iana-considerations)
      

The code points for the STUN methods defined in this specification are
      listed in [Section 17](#sec-stun-methods). IANA has
      updated the references from [[RFC5766](#RFC5766)] to
      this document (for the STUN methods listed in [Section 17](#sec-stun-methods)).[¶](#section-22-1)

The code points for the STUN attributes defined in this specification
      are listed in [Section 18](#sec-stun-attributes). IANA has
      updated the references from [[RFC5766](#RFC5766)] to
      this document (for the STUN attributes CHANNEL-[Section 18](#sec-stun-attributes)).[¶](#section-22-2)

The code points for the STUN error codes defined in this specification
      are listed in [Section 19](#sec-stun-errors). IANA has
      updated the references from [[RFC5766](#RFC5766)]
      and [[RFC6156](#RFC6156)] to this document (for the STUN error codes listed in
      [Section 19](#sec-stun-errors)).[¶](#section-22-3)

IANA has updated the references to [[RFC5766](#RFC5766)] to this document for the SRV service name of "turn" for TURN over UDP
      or TCP and the service name of "turns" for TURN over (D)TLS.[¶](#section-22-4)

IANA has created a registry for TURN channel numbers (the "Traversal
      Using Relays around NAT (TURN) Channel Numbers" registry), initially
      populated as follows:[¶](#section-22-5)

Any change to this registry must be made through an IETF
      Standards Action.[¶](#section-22-7)

## 
[23.](#section-23) [IAB Considerations](#name-iab-considerations)
      

The IAB has studied the problem of Unilateral Self-Address Fixing
      (UNSAF), which is the general process by which a client attempts to
      determine its address in another realm on the other side of a NAT
      through a collaborative protocol reflection mechanism [[RFC3424](#RFC3424)]. The TURN extension is an example of
      a protocol that performs this type of function. The IAB has mandated
      that any protocols developed for this purpose document a specific set of
      considerations. These considerations and the responses for TURN are
      documented in this section.[¶](#section-23-1)

Consideration 1: Precise definition of a specific, limited-scope
      problem that is to be solved with the UNSAF proposal. A short-term fix
      should not be generalized to solve other problems. Such generalizations
      lead to the prolonged dependence on and usage of the supposed short-term
      fix, meaning that it is no longer accurate to call it
      "short-term".[¶](#section-23-2)

Response: TURN is a protocol for communication between a relay (=
      TURN server) and its client. The protocol allows a client that is behind
      a NAT to obtain and use a public IP address on the relay. As a
      convenience to the client, TURN also allows the client to determine its
      server-[¶](#section-23-3)

Consideration 2: Description of an exit strategy/transition plan. The
      better short-term fixes are the ones that will naturally see less and
      less use as the appropriate technology is deployed.[¶](#section-23-4)

Response: TURN will no longer be needed once there are no longer any
      NATs. Unfortunately, as of the date of publication of this document, it
      no longer seems very likely that NATs will go away any time soon.
      However, the need for TURN will also decrease as the number of NATs with
      the mapping property of Endpoint-[RFC4787](#RFC4787)] increases.[¶](#section-23-5)

Consideration 3: Discussion of specific issues that may render
      systems more "brittle". For example, approaches that involve using data
      at multiple network layers create more dependencies, increase debugging
      challenges, and make it harder to transition.[¶](#section-23-6)

Response: TURN is "brittle" in that it requires the NAT bindings
      between the client and the server to be maintained unchanged for the
      lifetime of the allocation. This is typically done using keep-alives. If
      this is not done, then the client will lose its allocation and can no
      longer exchange data with its peers.[¶](#section-23-7)

Consideration 4: Identify requirements for longer-term, sound
      technical solutions; contribute to the process of finding the right
      longer-term solution.[¶](#section-23-8)

Response: The need for TURN will be reduced once NATs implement the
      recommendations for NAT UDP behavior documented in [[RFC4787](#RFC4787)]. Applications are also strongly
      urged to use ICE [[RFC8445](#RFC8445)] to
      communicate with peers; though ICE uses TURN, it does so only as a last
      resort, and it uses it in a controlled manner.[¶](#section-23-9)

Consideration 5: Discussion of the impact of the noted practical
      issues with existing deployed NATs and experience reports.[¶](#section-23-10)

Response: Some NATs deployed today exhibit a mapping behavior other
      than Endpoint-[RFC5128](#RFC5128)] do not
      work.[¶](#section-23-11)

## 
[24.](#section-24) [Changes since RFC 5766](#name-changes-since-rfc-5766)
      

This section lists the major changes in the TURN protocol from the
      original [[RFC5766](#RFC5766)] specification.[¶](#section-24-1)

## 
[25.](#section-25) [Updates to RFC 6156](#name-updates-to-rfc-6156)
      

This section lists the major updates to [[RFC6156](#RFC6156)] in this specification.[¶](#section-25-1)

## 
[26.](#section-26) [References](#name-references)
      

### 
[26.1.](#section-26.1) [Normative References](#name-normative-references)
        

- [PROTOCOL-NUMBERS]
- 
IANA, "Protocol Numbers", , <[https://](https://www.iana.org/assignments/protocol-numbers) >.www .iana .org /assignments /protocol- numbers
- [RFC0792]
- 
Postel, J., "Internet Control Message Protocol", STD 5, RFC 792, DOI 10.17487/RFC0792 , , <[https://](/info/rfc792) >.www .rfc- editor .org /info /rfc792
- [RFC1122]
- 
Braden, R., Ed., "Requirements for Internet Hosts - Communication Layers", STD 3, RFC 1122, DOI 10.17487/RFC1122 , , <[https://](/info/rfc1122) >.www .rfc- editor .org /info /rfc1122
- [RFC2119]
- 
Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119 , , <[https://](/info/rfc2119) >.www .rfc- editor .org /info /rfc2119
- [RFC2474]
- 
Nichols, K., Blake, S., Baker, F., and D. Black, "Definition of the Differentiated Services Field (DS Field) in the IPv4 and IPv6 Headers", RFC 2474, DOI 10.17487/RFC2474 , , <[https://](/info/rfc2474) >.www .rfc- editor .org /info /rfc2474
- [RFC3168]
- 
Ramakrishnan, K., Floyd, S., and D. Black, "The Addition of Explicit Congestion Notification (ECN) to IP", RFC 3168, DOI 10.17487/RFC3168 , , <[https://](/info/rfc3168) >.www .rfc- editor .org /info /rfc3168
- [RFC3629]
- 
Yergeau, F., "UTF-8, a transformation format of ISO 10646", STD 63, RFC 3629, DOI 10.17487/RFC3629 , , <[https://](/info/rfc3629) >.www .rfc- editor .org /info /rfc3629
- [RFC4443]
- 
Conta, A., Deering, S., and M. Gupta, Ed., "Internet Control Message Protocol (ICMPv6) for the Internet Protocol Version 6 (IPv6) Specification", STD 89, RFC 4443, DOI 10.17487/RFC4443 , , <[https://](/info/rfc4443) >.www .rfc- editor .org /info /rfc4443
- [RFC6347]
- 
Rescorla, E. and N. Modadugu, "Datagram Transport Layer Security Version 1.2", RFC 6347, DOI 10.17487/RFC6347 , , <[https://](/info/rfc6347) >.www .rfc- editor .org /info /rfc6347
- [RFC6437]
- 
Amante, S., Carpenter, B., Jiang, S., and J. Rajahalme, "IPv6 Flow Label Specification", RFC 6437, DOI 10.17487/RFC6437 , , <[https://](/info/rfc6437) >.www .rfc- editor .org /info /rfc6437
- [RFC7065]
- 
Petit-Huguenin, M. , Nandakumar, S., Salgueiro, G., and P. Jones, "Traversal Using Relays around NAT (TURN) Uniform Resource Identifiers", RFC 7065, DOI 10.17487/RFC7065 , , <[https://](/info/rfc7065) >.www .rfc- editor .org /info /rfc7065
- [RFC7350]
- 
Petit-Huguenin, M. and G. Salgueiro, "Datagram Transport Layer Security (DTLS) as Transport for Session Traversal Utilities for NAT (STUN)", RFC 7350, DOI 10.17487/RFC7350 , , <[https://](/info/rfc7350) >.www .rfc- editor .org /info /rfc7350
- [RFC7525]
- 
Sheffer, Y., Holz, R., and P. Saint-Andre, "Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)", BCP 195, RFC 7525, DOI 10.17487/RFC7525 , , <[https://](/info/rfc7525) >.www .rfc- editor .org /info /rfc7525
- [RFC7915]
- 
Bao, C., Li, X., Baker, F., Anderson, T., and F. Gont, "IP/ICMP Translation Algorithm", RFC 7915, DOI 10.17487/RFC7915 , , <[https://](/info/rfc7915) >.www .rfc- editor .org /info /rfc7915
- [RFC7982]
- 
Martinsen, P., Reddy, T., Wing, D., and V. Singh, "Measurement of Round-Trip Time and Fractional Loss Using Session Traversal Utilities for NAT (STUN)", RFC 7982, DOI 10.17487/RFC7982 , , <[https://](/info/rfc7982) >.www .rfc- editor .org /info /rfc7982
- [RFC8174]
- 
Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174 , , <[https://](/info/rfc8174) >.www .rfc- editor .org /info /rfc8174
- [RFC8200]
- 
Deering, S. and R. Hinden, "Internet Protocol, Version 6 (IPv6) Specification", STD 86, RFC 8200, DOI 10.17487/RFC8200 , , <[https://](/info/rfc8200) >.www .rfc- editor .org /info /rfc8200
- [RFC8305]
- 
Schinazi, D. and T. Pauly, "Happy Eyeballs Version 2: Better Connectivity Using Concurrency", RFC 8305, DOI 10.17487/RFC8305 , , <[https://](/info/rfc8305) >.www .rfc- editor .org /info /rfc8305
- [RFC8446]
- 
Rescorla, E., "The Transport Layer Security (TLS) Protocol Version 1.3", RFC 8446, DOI 10.17487/RFC8446 , , <[https://](/info/rfc8446) >.www .rfc- editor .org /info /rfc8446
- [RFC8489]
- 
Petit-Huguenin, M. , Salgueiro, G., Rosenberg, J., Wing, D., Mahy, R., and P. Matthews, "Session Traversal Utilities for NAT (STUN)", RFC 8489, DOI 10.17487/RFC8489 , , <[https://](/info/rfc8489) >.www .rfc- editor .org /info /rfc8489

### 
[26.2.](#section-26.2) [Informative References](#name-informative-references)
        

- [FRAG-FRAGILE]
- 
Bonica, R., Baker, F., Huston, G., Hinden, R., Troan, O., and F. Gont, "IP Fragmentation Considered Fragile", Work in Progress, Internet-Draft, draft- , , <ietf- intarea- frag- fragile-17 [https://](https://tools.ietf.org/html/draft-ietf-intarea-frag-fragile-17) >.tools .ietf .org /html /draft- ietf- intarea- frag- fragile-17
- [FRAG-HARMFUL]
- 
Kent, C. and J. Mogul, "Fragmentation Considered Harmful", , <[https://](https://www.hpl.hp.com/techreports/Compaq-DEC/WRL-87-3.pdf) >.www .hpl .hp .com /techreports /Compaq- DEC /WRL- 87-3 .pdf
- [MTU-DATAGRAM]
- 
Fairhurst, G., Jones, T., Tuexen, M., Ruengeler, I., and T. Voelker, "Packetization Layer Path MTU Discovery for Datagram Transports", Work in Progress, Internet-Draft, draft- , , <ietf- tsvwg- datagram- plpmtud-14 [https://](https://tools.ietf.org/html/draft-ietf-tsvwg-datagram-plpmtud-14) >.tools .ietf .org /html /draft- ietf- tsvwg- datagram- plpmtud-14
- [MTU-STUN]
- 
Petit-Huguenin, M. , Salgueiro, G., and F. Garrido, "Packetization Layer Path MTU Discovery (PLMTUD) For UDP Transports Using Session Traversal Utilities for NAT (STUN)", Work in Progress, Internet-Draft, draft- , , <ietf- tram- stun- pmtud-15 [https://](https://tools.ietf.org/html/draft-ietf-tram-stun-pmtud-15) >.tools .ietf .org /html /draft- ietf- tram- stun- pmtud-15
- [PORT-NUMBERS]
- 
IANA, "Service Name and Transport Protocol Port Number Registry", , <[https://](https://www.iana.org/assignments/port-numbers) >.www .iana .org /assignments /port- numbers
- [RFC0791]
- 
Postel, J., "Internet Protocol", STD 5, RFC 791, DOI 10.17487/RFC0791 , , <[https://](/info/rfc791) >.www .rfc- editor .org /info /rfc791
- [RFC1191]
- 
Mogul, J. and S. Deering, "Path MTU discovery", RFC 1191, DOI 10.17487/RFC1191 , , <[https://](/info/rfc1191) >.www .rfc- editor .org /info /rfc1191
- [RFC1918]
- 
Rekhter, Y., Moskowitz, B., Karrenberg, D., de Groot, G. J., and E. Lear, "Address Allocation for Private Internets", BCP 5, RFC 1918, DOI 10.17487/RFC1918 , , <[https://](/info/rfc1918) >.www .rfc- editor .org /info /rfc1918
- [RFC1928]
- 
Leech, M., Ganis, M., Lee, Y., Kuris, R., Koblas, D., and L. Jones, "SOCKS Protocol Version 5", RFC 1928, DOI 10.17487/RFC1928 , , <[https://](/info/rfc1928) >.www .rfc- editor .org /info /rfc1928
- [RFC3261]
- 
Rosenberg, J., Schulzrinne, H., Camarillo, G., Johnston, A., Peterson, J., Sparks, R., Handley, M., and E. Schooler, "SIP: Session Initiation Protocol", RFC 3261, DOI 10.17487/RFC3261 , , <[https://](/info/rfc3261) >.www .rfc- editor .org /info /rfc3261
- [RFC3424]
- 
Daigle, L., Ed. and IAB, "IAB Considerations for UNilateral Self-Address Fixing (UNSAF) Across Network Address Translation", RFC 3424, DOI 10.17487/RFC3424 , , <[https://](/info/rfc3424) >.www .rfc- editor .org /info /rfc3424
- [RFC3550]
- 
Schulzrinne, H., Casner, S., Frederick, R., and V. Jacobson, "RTP: A Transport Protocol for Real-Time Applications", STD 64, RFC 3550, DOI 10.17487/RFC3550 , , <[https://](/info/rfc3550) >.www .rfc- editor .org /info /rfc3550
- [RFC3711]
- 
Baugher, M., McGrew, D., Naslund, M., Carrara, E., and K. Norrman, "The Secure Real-time Transport Protocol (SRTP)", RFC 3711, DOI 10.17487/RFC3711 , , <[https://](/info/rfc3711) >.www .rfc- editor .org /info /rfc3711
- [RFC4086]
- 
Eastlake 3rd, D., Schiller, J., and S. Crocker, "Randomness Requirements for Security", BCP 106, RFC 4086, DOI 10.17487/RFC4086 , , <[https://](/info/rfc4086) >.www .rfc- editor .org /info /rfc4086
- [RFC4302]
- 
Kent, S., "IP Authentication Header", RFC 4302, DOI 10.17487/RFC4302 , , <[https://](/info/rfc4302) >.www .rfc- editor .org /info /rfc4302
- [RFC4303]
- 
Kent, S., "IP Encapsulating Security Payload (ESP)", RFC 4303, DOI 10.17487/RFC4303 , , <[https://](/info/rfc4303) >.www .rfc- editor .org /info /rfc4303
- [RFC4787]
- 
Audet, F., Ed. and C. Jennings, "Network Address Translation (NAT) Behavioral Requirements for Unicast UDP", BCP 127, RFC 4787, DOI 10.17487/RFC4787 , , <[https://](/info/rfc4787) >.www .rfc- editor .org /info /rfc4787
- [RFC4821]
- 
Mathis, M. and J. Heffner, "Packetization Layer Path MTU Discovery", RFC 4821, DOI 10.17487/RFC4821 , , <[https://](/info/rfc4821) >.www .rfc- editor .org /info /rfc4821
- [RFC5128]
- 
Srisuresh, P., Ford, B., and D. Kegel, "State of Peer-to-Peer (P2P) Communication across Network Address Translators (NATs)", RFC 5128, DOI 10.17487/RFC5128 , , <[https://](/info/rfc5128) >.www .rfc- editor .org /info /rfc5128
- [RFC5482]
- 
Eggert, L. and F. Gont, "TCP User Timeout Option", RFC 5482, DOI 10.17487/RFC5482 , , <[https://](/info/rfc5482) >.www .rfc- editor .org /info /rfc5482
- [RFC5766]
- 
Mahy, R., Matthews, P., and J. Rosenberg, "Traversal Using Relays around NAT (TURN): Relay Extensions to Session Traversal Utilities for NAT (STUN)", RFC 5766, DOI 10.17487/RFC5766 , , <[https://](/info/rfc5766) >.www .rfc- editor .org /info /rfc5766
- [RFC5925]
- 
Touch, J., Mankin, A., and R. Bonica, "The TCP Authentication Option", RFC 5925, DOI 10.17487/RFC5925 , , <[https://](/info/rfc5925) >.www .rfc- editor .org /info /rfc5925
- [RFC5928]
- 
Petit-Huguenin, M. , "Traversal Using Relays around NAT (TURN) Resolution Mechanism", RFC 5928, DOI 10.17487/RFC5928 , , <[https://](/info/rfc5928) >.www .rfc- editor .org /info /rfc5928
- [RFC6056]
- 
Larsen, M. and F. Gont, "Recommendations for Transport-Protocol Port Randomization" , BCP 156, RFC 6056, DOI 10.17487/RFC6056 , , <[https://](/info/rfc6056) >.www .rfc- editor .org /info /rfc6056
- [RFC6062]
- 
Perreault, S., Ed. and J. Rosenberg, "Traversal Using Relays around NAT (TURN) Extensions for TCP Allocations", RFC 6062, DOI 10.17487/RFC6062 , , <[https://](/info/rfc6062) >.www .rfc- editor .org /info /rfc6062
- [RFC6156]
- 
Camarillo, G., Novo, O., and S. Perreault, Ed., "Traversal Using Relays around NAT (TURN) Extension for IPv6", RFC 6156, DOI 10.17487/RFC6156 , , <[https://](/info/rfc6156) >.www .rfc- editor .org /info /rfc6156
- [RFC6263]
- 
Marjou, X. and A. Sollaud, "Application Mechanism for Keeping Alive the NAT Mappings Associated with RTP / RTP Control Protocol (RTCP) Flows", RFC 6263, DOI 10.17487/RFC6263 , , <[https://](/info/rfc6263) >.www .rfc- editor .org /info /rfc6263
- [RFC7413]
- 
Cheng, Y., Chu, J., Radhakrishnan, S., and A. Jain, "TCP Fast Open", RFC 7413, DOI 10.17487/RFC7413 , , <[https://](/info/rfc7413) >.www .rfc- editor .org /info /rfc7413
- [RFC7478]
- 
Holmberg, C., Hakansson, S., and G. Eriksson, "Web Real-Time Communication Use Cases and Requirements", RFC 7478, DOI 10.17487/RFC7478 , , <[https://](/info/rfc7478) >.www .rfc- editor .org /info /rfc7478
- [RFC7635]
- 
Reddy, T., Patil, P., Ravindranath, R., and J. Uberti, "Session Traversal Utilities for NAT (STUN) Extension for Third-Party Authorization", RFC 7635, DOI 10.17487/RFC7635 , , <[https://](/info/rfc7635) >.www .rfc- editor .org /info /rfc7635
- [RFC7657]
- 
Black, D., Ed. and P. Jones, "Differentiated Services (Diffserv) and Real-Time Communication", RFC 7657, DOI 10.17487/RFC7657 , , <[https://](/info/rfc7657) >.www .rfc- editor .org /info /rfc7657
- [RFC7983]
- 
Petit-Huguenin, M. and G. Salgueiro, "Multiplexing Scheme Updates for Secure Real-time Transport Protocol (SRTP) Extension for Datagram Transport Layer Security (DTLS)", RFC 7983, DOI 10.17487/RFC7983 , , <[https://](/info/rfc7983) >.www .rfc- editor .org /info /rfc7983
- [RFC8155]
- 
Patil, P., Reddy, T., and D. Wing, "Traversal Using Relays around NAT (TURN) Server Auto Discovery", RFC 8155, DOI 10.17487/RFC8155 , , <[https://](/info/rfc8155) >.www .rfc- editor .org /info /rfc8155
- [RFC8311]
- 
Black, D., "Relaxing Restrictions on Explicit Congestion Notification (ECN) Experimentation", RFC 8311, DOI 10.17487/RFC8311 , , <[https://](/info/rfc8311) >.www .rfc- editor .org /info /rfc8311
- [RFC8445]
- 
Keranen, A., Holmberg, C., and J. Rosenberg, "Interactive Connectivity Establishment (ICE): A Protocol for Network Address Translator (NAT) Traversal", RFC 8445, DOI 10.17487/RFC8445 , , <[https://](/info/rfc8445) >.www .rfc- editor .org /info /rfc8445
- [SDP-ICE]
- 
Petit-Huguenin, M. , Nandakumar, S., Holmberg, C., Keranen, A., and R. Shpount, "Session Description Protocol (SDP) Offer/Answer procedures for Interactive Connectivity Establishment (ICE)", Work in Progress, Internet-Draft, draft- , , <ietf- mmusic- ice- sip- sdp-39 [https://](https://tools.ietf.org/html/draft-ietf-mmusic-ice-sip-sdp-39) >.tools .ietf .org /html /draft- ietf- mmusic- ice- sip- sdp-39
- [SEC-WEBRTC]
- 
Rescorla, E., "Security Considerations for WebRTC", Work in Progress, Internet-Draft, draft- , , <ietf- rtcweb- security-12 [https://](https://tools.ietf.org/html/draft-ietf-rtcweb-security-12) >.tools .ietf .org /html /draft- ietf- rtcweb- security-12
- [TCP-EXT]
- 
Ford, A., Raiciu, C., Handley, M., Bonaventure, O., and C. Paasch, "TCP Extensions for Multipath Operation with Multiple Addresses", Work in Progress, Internet-Draft, draft- , , <ietf- mptcp- rfc6824bis-18 [https://](https://tools.ietf.org/html/draft-ietf-mptcp-rfc6824bis-18) >.tools .ietf .org /html /draft- ietf- mptcp- rfc6824bis-18
- [UDP-OPT]
- 
Touch, J., "Transport Options for UDP", Work in Progress, Internet-Draft, draft- , , <ietf- tsvwg- udp- options-08 [https://](https://tools.ietf.org/html/draft-ietf-tsvwg-udp-options-08) >.tools .ietf .org /html /draft- ietf- tsvwg- udp- options-08

## 
[Acknowledgements](#name-acknowledgements)
      

Most of the text in this note comes from the original TURN
      specification, [[RFC5766](#RFC5766)]. The authors would like to
      thank Rohan Mahy, coauthor of the original TURN specification, and everyone
      who had contributed to that document. The authors would also like to
      acknowledge that this document inherits material from [[RFC6156](#RFC6156)].[¶](#section-appendix.a-1)

Thanks to Justin Uberti, Pal       Martinsen, Oleg Moskalenko, Aijun Wang, and Simon Perreault for
      their help on the ADDITIONAL-[¶](#section-appendix.a-2)

Special thanks to Magnus Westerlund for the detailed AD review.[¶](#section-appendix.a-3)
