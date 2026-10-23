---
title: Financial Information eXchange - Wikipedia
source: https://en.wikipedia.org/wiki/Financial_Information_eXchange
published: '2004-06-18'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Financial Information eXchange - Wikipedia

# Financial Information eXchange

The **Financial Information eXchange** (**FIX**) protocol is an electronic [communications protocol](https://en.wikipedia.org/wiki/Communications_protocol) initiated in 1992 for international real-time exchange of information related to [securities](<https://en.wikipedia.org/wiki/Security_(finance)>) transactions and markets. With trillions of dollars traded annually on the [NASDAQ](https://en.wikipedia.org/wiki/NASDAQ) alone, financial service entities are employing [direct market access](https://en.wikipedia.org/wiki/Direct_market_access) (DMA) to increase their speed to financial markets. Managing the delivery of trading applications and keeping latency low increasingly requires an understanding of the FIX protocol.

## History

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=1)]

The FIX protocol specification was originally authored in 1992 by Robert "Bob" Lamoureux and Chris Morstatt to enable electronic communication of [equity](<https://en.wikipedia.org/wiki/Equity_(finance)>) trading data between [Fidelity Investments](https://en.wikipedia.org/wiki/Fidelity_Investments) and [Salomon Brothers](https://en.wikipedia.org/wiki/Salomon_Brothers). FIX initially addressed information between [broker-dealers](https://en.wikipedia.org/wiki/Broker-dealer) and their institutional clients. At the time, this information was communicated verbally over the telephone. Fidelity realized that information from their broker-dealers could be routed to the wrong trader, or simply lost when the parties hung up their phones. It wanted such communications to be replaced with [machine-readable data](https://en.wikipedia.org/wiki/Machine-readable_data) which could then be shared among traders, analyzed, acted on and stored. For example, broker-dealers call with an [indication of interest](https://en.wikipedia.org/wiki/Indication_of_interest) (IOI) to buy or sell a block of stock. The FIX initiative created new messages such as the IOI.

According to the FIX Trading Community, FIX has become the de facto messaging standard for pre-trade and trade communication in the global equity markets, and is expanding into the post-trade space to support [straight-through processing](https://en.wikipedia.org/wiki/Straight-through_processing), as well as continuing to expand into [foreign exchange](https://en.wikipedia.org/wiki/Foreign_exchange_market), [fixed income](https://en.wikipedia.org/wiki/Fixed_income) and [derivatives](<https://en.wikipedia.org/wiki/Derivative_(finance)>) markets.[\[1\]](#cite_note-1)

### FIX Trading Community

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=2)]

The FIX Trading Community is a non-profit, industry-driven standards body with a mission to address the business and regulatory issues impacting multi-asset trading across the global financial markets through the increased use of standards, including the FIX Protocol messaging language, delivering operational efficiency, increased transparency, and reduced costs and risk for all market participants.[\[2\]](#cite_note-2)

## Users

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=3)]

FIX is widely used by both the [buy side](https://en.wikipedia.org/wiki/Buy_side) (institutions) as well as the [sell side](https://en.wikipedia.org/wiki/Sell_side) (brokers/dealers) of the [financial markets](https://en.wikipedia.org/wiki/Financial_markets). Among its users are [mutual funds](https://en.wikipedia.org/wiki/Mutual_fund), [investment banks](https://en.wikipedia.org/wiki/Investment_bank), brokers, [stock exchanges](https://en.wikipedia.org/wiki/Stock_exchange) and [ECNs](https://en.wikipedia.org/wiki/Electronic_communication_network).

FIX has become the standard electronic protocol for pre-trade communications and trade execution. Although it is mainly used for equity transactions in the [front office](<https://en.wikipedia.org/wiki/Front_office_(finance)>) area, bond derivatives and FX-transactions are also possible. One could say that whereas [SWIFT](https://en.wikipedia.org/wiki/SWIFT) is the standard for [back office](https://en.wikipedia.org/wiki/Back_office) messaging, FIX is the standard for front office messaging. However, today, the membership of FIX Protocol Ltd. is extending FIX into [block trade](https://en.wikipedia.org/wiki/Block_trade) allocation and other phases of the trading process, in every market, for virtually every asset class.

## Technical specifications

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=4)]

Originally, the FIX standard was monolithic, including application layer semantics, message encoding, and session layer in a single technical specification.  It remained monolithic through FIX version 4.2.<sup>[\[3\]](#cite_note-3)</sup> Thereafter, message encodings and session layer specifications began to be split into separate documents, and ultimately, FIX evolved into a family of related technical standards.[\[4\]](#cite_note-4)

### Message encodings

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=5)]

Message encoding, called [Presentation Layer](https://en.wikipedia.org/wiki/Presentation_layer) in the Open Systems Interconnection model ([OSI model](https://en.wikipedia.org/wiki/OSI_model)), is responsible for the wire format of messages.

#### Tagvalue encoding (classic FIX)

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=6)]

The original FIX message encoding is known as tagvalue encoding.  Each field consists of a unique numeric tag and a value.  The tag identifies the field semantically. Therefore, messages are self-describing. Tagvalue encoding is character-based, using [ASCII](https://en.wikipedia.org/wiki/ASCII) codes.

##### FIX tagvalue message format

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=7)]

A message is composed of a header, a body, and a trailer. The message fields are separated by the [start of heading (SOH)](https://en.wikipedia.org/wiki/C0_and_C1_control_codes#SOH) character ([ASCII](https://en.wikipedia.org/wiki/ASCII) 0x01).

Up to FIX.4.4, the header contains three fields: 8 (`BeginString`), 9 (`BodyLength`), and 35 (`MsgType`).

From FIXT.1.1 / FIX.5.0, the header contains five or six fields: 8 (`BeginString`), 9 (`BodyLength`), 35 (`MsgType`), 49 (`SenderCompID`), 56 (`TargetCompID`) and the optional 1128 (`ApplVerID`).

The content of the message body is defined by the message type (35 `MsgType`) in the header.

The trailer contains the last field of the message, 10 ([Checksum](https://en.wikipedia.org/wiki/Checksum)`10=002`).

Example of a FIX message, Execution Report (`35=8`), with the pipe character (`|`) representing the SOH character:

- `8=FIX.4.2 | 9=178 | 35=8 | 49=PHLX | 56=PERS | 52=20071123-05:30:00.000 | 11=ATOMNOCCC9990900 | 20=3 | 150=E | 39=E | 55=MSFT | 167=CS | 54=1 | 38=15 | 40=2 | 44=15 | 58=PHLX EQUITY TESTING | 59=0 | 47=C | 32=0 | 31=0 | 151=15 | 14=0 | 6=0 | 10=128 |`

##### Body

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=8)]

FIX messages are formed from several fields; each field has a tag value pairing that is separated from the next field by a [delimiter](https://en.wikipedia.org/wiki/Delimiter) [SOH](https://en.wikipedia.org/wiki/C0_and_C1_control_codes#SOH) (0x01). The tag is an integer that indicates the meaning of the field. The value is an array of bytes that hold a specific meaning for the particular tag (e.g. tag 48 is SecurityID, a string that identifies the security; tag 22 is IDSource, an integer that indicates the identifier class being used). The values may be in plain text or encoded as pure binary (in which case the value is preceded by a length field). The FIX protocol defines meanings for most tags, but leaves a range of tags reserved for private use between consenting parties.

The FIX protocol also defines sets of fields that make a particular message; within the set of fields, some will be mandatory and others optional.  The ordering of fields within the message is generally unimportant, however repeating groups are preceded by a count and encrypted fields are preceded by their length. The message is broken into three distinct sections: the head, body and tail. Fields must remain within the correct section and within each section, the position may be important as fields can act as delimiters that stop one message from running into the next. The final field in any FIX message is tag 10 ([checksum](https://en.wikipedia.org/wiki/Checksum)).

There are two main groups of messages—admin and application. The admin messages handle the basics of a FIX session. They allow for a session to be started and terminated and for recovery of missed messages. The application messages deal with the sending and receiving of trade-related information such as an order request or information on the current state and subsequent execution of that order.

##### Body length

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=9)]

The body length is the character count starting at tag 35 (included) all the way to tag 10 (excluded), including trailing SOH delimiters.

The example below (displayed with SOH delimiters as '|') has a body length of 65:

```
8=FIX.4.2|9=65|35=A|49=SERVER|56=CLIENT|34=177|52=20090107-18:15:16|98=0|108=30|10=062|
              ^  5 +    10   +    10   +   7  +         21         +  5 +    7  ^       = 65 
```
##### Checksum

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=10)]

The checksum of a FIX message is always the last field in the message, with tag `10` and a 3 character value.<sup>[\[5\]](#cite_note-5)</sup> It is given by summing the [ASCII](https://en.wikipedia.org/wiki/ASCII) value of all characters in the message (except for the checksum field itself), then [modulo](https://en.wikipedia.org/wiki/Modulo_operation) 256. For example, in the message above, the summation of all ASCII values (including the SOH characters with ASCII value 1) results in 4158. Performing the modulo operation gives the value 62. Since the checksum is composed of three characters, this results in `10=062`.

#### FIXML

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=11)]

FIXML<sup>[\[6\]](#cite_note-6)</sup>  is an XML schema for FIX messages. It is semantically equivalent to tagvalue encoded messages but takes advantage of XML parser technology. FIXML is commonly used for back-office and clearing applications rather than trading.

#### Simple Binary Encoding (SBE)

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=12)]

Simple Binary Encoding<sup>[\[7\]](#cite_note-7)</sup> defines a wire format using primitive data types that are native to computing systems.  Message encoding and decoding is therefore much lower latency than character-based protocols since no translation is needed to put data into a format that computers can use.  Aside from latency advantages, performance is more deterministic because SBE messages are constrained by templates and fixed-length data elements are preferred.  Another consequence is that fields are generally at a fixed position so that message filters and routers do not need to crack an entire message to access key fields.

SBE was developed by the FIX High Performance Working Group to support high performance trading. Tagvalue encoding was deemed no longer fit-for-purpose since it is character based rather than binary and its variable-length fields and messages result in non-deterministic performance.

Unlike tagvalue and FIXML, an SBE message is not self-describing.  Only data is sent on the wire with a minimal header to identify the template that controls a message.  Metadata that describes a message layout is exchanged [out-of-band](https://en.wikipedia.org/wiki/Out-of-band_data) between peers.

FIX Trading Community publishes an XML schema for SBE message schemas. A message schema may contain any number of message templates. A template describes the fields that constitute a message. Additionally, a schema provides a listing of simple and composite data types that may be reused by any number of fields.

From a practical perspective, assuming a C/C++ implementation, and adjusting for [endianness](https://en.wikipedia.org/wiki/Endianness): most non-composite types in the message directly map to the same type in the language. For example, 32-bit integer maps to `uint32_t`, fixed strings maps `const char *`, floating point maps to `float` and so on. One can generate a C/C++ `struct` from the schema definition. Then, given a pointer to a message buffer, accessing non-composite fields of the message amount to type-casting it to a pointer to structure and accessing structure members directly.

```
/* Generated struct from schema */
struct Message {
  ...
  uint32_t qty;
  ...
  const char *symbol;
  ...
};
void consume_message(void *incoming_message) {
  const struct Message *msg = (const struct Message*) incoming_message;
  printf("Traded %u of %s\n", msg->qty, msg->symbol);
  ...
}
```
#### Other FIX encodings

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=13)]

FIX Trading Community has also developed standard mappings between FIX and other message protocols, including:

### Session protocols

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=14)]

The session layer is responsible for message exchange including checkpoint recovery mechanisms.

#### FIX Transport (FIXT)

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=15)]

The original FIX session protocol did not have its own name since it was part of a monolithic specification covering application layer semantics and message encoding as well. However, starting with FIX version 5.0, the session layer was split off as an independent specification with the introduction of FIXT.<sup>[\[8\]](#cite_note-8)</sup> FIXT was largely the same as the original unnamed session layer in version 4.x, but it offered one significant innovation--it provided a mechanism to mix FIX application layer versions over a common session version. The current FIXT version is 1.1.

Theoretically, FIXT is transport independent. However, it is usually employed over [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) (TCP).

FIXT is a [point-to-point protocol](https://en.wikipedia.org/wiki/Point-to-Point_Protocol). It guarantees message delivery in both directions. Messages sent in each direction carry a message sequence number in the message header. If there is a communication fault, a peer may request retransmission of missed messages. Message delivery is supported even in the event of disconnection and later reestablishment of a session.

To implement session establishment and guaranteed delivery, FIXT and classic FIX 4.x define these session message types:

- Heartbeat
- Test Request
- ResendRequest
- Reject
- SequenceReset
- Logout
- Logon
- XMLnonFIX

#### FIX Performance Session Layer (FIXP)

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=16)]

FIXP<sup>[\[9\]](#cite_note-9)</sup> was developed by the FIX High Performance Working Group<sup>[\[10\]](#cite_note-10)</sup> to meet the needs of high performance trading. The primary need is for low latency message encoding and decoding and control over message delivery guarantees.

To provide low latency, binary message encodings are supported both for session layer and application messages. The actual wire format is abstracted in the FIXP specification, so users may select a FIX encoding of their choice, so long as peers agree on a protocol to use. Early development has used Simple Binary Encoding.

FIXP covers both point-to-point and multicast use cases with common primitives.

When a point-to-point session is established, peers negotiate delivery guarantees from among the following choices:

- Recoverable: exactly-once message delivery. If gaps are detected, then missed messages may be recovered by retransmission.
- Idempotent: at-most-once delivery. If gaps are detected, the sender is notified, but recovery is under the control of the application, if it is done at all.
- Unsequenced: makes no delivery guarantees. This choice is appropriate if guarantees are unnecessary or if recovery is provided at the application layer or through a different [communication channel](https://en.wikipedia.org/wiki/Communication_channel) .
- Note: No application messages should be sent in one direction of a session.

Delivery guarantees may be asymmetrical. For example, a trader may enter orders over an idempotent flow while executions are returned over a recoverable flow. In fast moving markets, the delay inherent in retransmission is often undesirable, resulting in missed opportunities or bad trades.

## Diagrammatic representation of FIX system

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=17)]

Below is a diagram of how to FIX messaging looks between Buyside/Customer and Sellside/Supplier.[\[11\]](#cite_note-11)

## Latest developments in FIX protocol

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=18)]

The latest version of FIX Protocol implements "Transport Independence" by permitting multiple versions of application messages to be carried over a single version of Transport Independent FIX Session (FIXT.1.1 and higher).

Transport Independence also paves the way for transport protocols such as [message queues](https://en.wikipedia.org/wiki/Message_queue) and [web services](https://en.wikipedia.org/wiki/Web_service) to be used instead of traditional FIX over TCP.

FIX now supports [algorithmic trading](https://en.wikipedia.org/wiki/Algorithmic_trading) by the use of FIX Algorithmic Trading Definition Language [FIXatdl](https://en.wikipedia.org/wiki/FIXatdl).

In 2005, the FIX Trading Community released [FAST protocol](https://en.wikipedia.org/wiki/FAST_protocol) which stands for FIX Adapted for Streaming. [FAST](https://en.wikipedia.org/wiki/FAST_protocol) is a binary protocol and is used mostly for sending [Multicast](https://en.wikipedia.org/wiki/Multicast) [market data](https://en.wikipedia.org/wiki/Market_data) via UDP connections.

Further, in 2020, the FIX Trading Community released a new FIX binary encoding, based on Simple Binary Encoding (SBE), meant to complement the existing FAST encoding.[\[12\]](#cite_note-12)

## See also

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=19)]

## Notes

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=20)]

1. [↑](#cite_ref-1)["What is FIX?"](https://web.archive.org/web/20040909043901/http://fixprotocol.org/what-is-fix.shtml) . The FIX Protocol Organization. June 8, 2009. Archived from[the original](http://www.fixprotocol.org/what-is-fix.shtml) on September 9, 2004.
2. [↑](#cite_ref-2)["Overview • FIX Trading Community"](https://fixtrading.org/who-we-are/) .*FIX Trading Community* . Retrieved 2026-09-01.
3. [↑](#cite_ref-3)["FIX 4.2 Specification with 20010501 Errata • FIX Trading Community"](https://fixtrading.org/packages/fix-4-2-specification-with-errata-20010501/) .*FIX Trading Community* . Retrieved 2026-09-01.
4. [↑](#cite_ref-4)["FIX Standards • FIX Trading Community"](https://fixtrading.org/standards/technical-standards/) .*FIX Trading Community* . Retrieved 2026-09-01.
5. [↑](#cite_ref-5)[FIX 4.2 : CheckSum <10> field | FIX Dictionary](https://fiximate.fixtrading.org/legacy/en/FIX.4.2/tag10.html)
6. [↑](#cite_ref-6)["FIXML • FIX Trading Community"](https://www.fixtrading.org/standards/fixml/) .*FIX Trading Community* . Retrieved 2018-12-05.
7. [↑](#cite_ref-7)["Simple Binary Encoding (SBE) • FIX Trading Community"](https://www.fixtrading.org/standards/sbe/) .*FIX Trading Community* . Retrieved 2018-12-05.
8. [↑](#cite_ref-8)["FIX Transport (FIXT) • FIX Trading Community"](https://www.fixtrading.org/standards/fixt/) .*FIX Trading Community* . Retrieved 2018-12-05.
9. [↑](#cite_ref-9)["FIX Performance Session Layer (FIXP) • FIX Trading Community"](https://www.fixtrading.org/standards/fixp/) .*FIX Trading Community* . Retrieved 2018-12-05.
10. [↑](#cite_ref-10)["Home – High Performance Working Group"](https://www.fixtrading.org/groups/hpwg/) .*FIX Trading Community* . Retrieved 2018-12-05.
11. [↑](#cite_ref-11) DeMarco, Darren.["Exploiting Financial Information Exchange (FIX) Protocol?"](https://www.sans.org/reading-room/whitepapers/threats/exploiting-financial-information-exchange-fix-protocol-33964) .
12. [↑](#cite_ref-12)["Simple Binary Encoding (SBE)"](https://www.fixtrading.org/standards/sbe/) . 21 March 2024.

## External links

[
[edit](/w/index.php?title=Financial_Information_eXchange&action=edit§ion=21)]

- [FIX Protocol Ltd.](https://www.fixtrading.org/) - official FIX Trading Community website for the[FIX Protocol](https://fixtrading.org/standards/fix-protocol/) and related[Technical Standards](https://fixtrading.org/standards/technical-standards/) .
- [FIXimate](http://fiximate.fixtrading.org/) - official FIX dictionary browser maintained by the FIX Trading Community (see[FIX Latest](http://fiximate.fixtrading.org/) ,[FIX 4.4](https://fiximate.fixtrading.org/legacy/en/FIX.4.4/) ,[FIX 4.2](https://fiximate.fixtrading.org/legacy/en/FIX.4.2/) , and[FIX Legacy Versions](https://fixtrading.org/legacy-fix-specifications/) ).
- [Orchimate](https://orchimate.org) - hosting platform for FIXimate and other Orchestra repositories published by the FIX Trading Community, exchanges, and market participants defining their own protocols and FIX dialects.
- [B2BITS FIX Antenna .NET Core](https://github.com/epam/fix-antenna-net-core) - an open source .NET FIX engine implementation.
- [Esprow FIX Tools](http://www.esprow.com/fixtools/index.php) - an online FIX dictionary browser for all FIX versions, including a FIX message parser.
- [Full FIX Protocol Dictionary on Onixs](http://www.onixs.biz/fix-dictionary.html) - quick and easy to use contemporary dictionary of the FIX Protocol (versions[4.0](http://www.onixs.biz/fix-dictionary/4.0/index.html) ,[4.1](http://www.onixs.biz/fix-dictionary/4.1/index.html) ,[4.2](http://www.onixs.biz/fix-dictionary/4.2/index.html) ,[4.3](http://www.onixs.biz/fix-dictionary/4.3/index.html) ,[4.4](http://www.onixs.biz/fix-dictionary/4.4/index.html) ,[5.0](http://www.onixs.biz/fix-dictionary/5.0/index.html) ,[5.0.SP1](http://www.onixs.biz/fix-dictionary/5.0.SP1/index.html) ,[5.0.SP2](http://www.onixs.biz/fix-dictionary/5.0.SP2/index.html) ,[FIXT1.1](https://www.onixs.biz/fix-dictionary/FIXT1.1/index.html) ).
- [FIXSIM](https://www.fixsim.com/fix-parser) - FIX message parser, sample messages, testing support.
- [FIXGlobal](http://fixglobal.com/) - Free global trading journal and official magazine of the FIX Protocol.
- [What is FIX Protocol?](https://targetcompid.tumblr.com/post/39879066034/what-is-fix-protocol) - Non-technical overview of FIX Protocol.
- A simple [FIX Decoder](https://github.com/Alwyn-Teh/FIX-Decoder) written in shell script with sed that runs fast natively on Unix/Linux, in need of updating to the latest FIX version.
- [FIX Parser](https://fixparser.chronicle.software) - an online FIX message parser.
- [FIX Message Decoder](https://fix-decoder.samkov.ee/) - Powered by fix-message, an open-source Web Component for decoding FIX messages.
