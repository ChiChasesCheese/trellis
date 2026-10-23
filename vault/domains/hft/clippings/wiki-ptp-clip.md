---
title: Precision Time Protocol - Wikipedia
source: https://en.wikipedia.org/wiki/Precision_Time_Protocol
published: '2005-06-30'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Precision Time Protocol - Wikipedia

# Precision Time Protocol

| Precision Time Protocol |  | 
|---|---|
| [Communication protocol](https://en.wikipedia.org/wiki/Communication_protocol) |  | 
| Abbreviation | PTP | 
|---|---|
| Purpose | Time | 
| Developer | [IEEE](https://en.wikipedia.org/wiki/IEEE) | 
| Introduction | 2002 | 
| [Ports](<https://en.wikipedia.org/wiki/Port_(computer_networking)>) | udp/319, udp/320 | 

The **Precision Time Protocol** (**PTP**) is a [protocol](<https://en.wikipedia.org/wiki/Protocol_(computing)>) for [clock synchronization](https://en.wikipedia.org/wiki/Clock_synchronization) throughout a [computer network](https://en.wikipedia.org/wiki/Computer_network) with relatively high [precision](https://en.wikipedia.org/wiki/Accuracy_and_precision) as compared to using the earlier developed [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol) (NTP) and therefore *potentially* higher accuracy depending on the configuration. In a [local area network](https://en.wikipedia.org/wiki/Local_area_network) (LAN), accuracy can be sub-microsecond – making it suitable for measurement and control systems applications.<sup>[\[1\]](#cite_note-1)</sup> PTP can be used to synchronize [financial transactions](https://en.wikipedia.org/wiki/Financial_transaction)<sup>[\[2\]](#cite_note-2)</sup>, [mobile phone tower](https://en.wikipedia.org/wiki/Mobile_phone_tower) transmissions<sup>[\[3\]](#cite_note-3)</sup>, sub-sea [acoustic arrays](https://en.wikipedia.org/wiki/Acoustic_array)<sup>[\[4\]](#cite_note-4)</sup>, and networks that require precise timing as an alternative to using the timestamp of [satellite navigation](https://en.wikipedia.org/wiki/Satellite_navigation) signals or where sub-nanosecond accuracy as provided by the [White Rabbit Project](https://en.wikipedia.org/wiki/White_Rabbit_Project) is unnecessary.[\[5\]](#cite_note-5)

The first version of PTP, **IEEE 1588-2002**, was published in 2002. **IEEE 1588-2008**, also known as PTP Version 2, is not [backward compatible](https://en.wikipedia.org/wiki/Backward_compatible) with the 2002 version. **IEEE 1588-2019** was published in November 2019 and includes backward-compatible improvements to the 2008 publication. IEEE 1588-2008 includes a *profile* concept defining PTP operating parameters and options. Several profiles have been defined for applications including [telecommunications](https://en.wikipedia.org/wiki/Telecommunications), [electric power distribution](https://en.wikipedia.org/wiki/Electric_power_distribution) and [audiovisual](https://en.wikipedia.org/wiki/Audiovisual) uses. **IEEE 802.1AS** is an adaptation of PTP, called gPTP, for use with [Audio Video Bridging](https://en.wikipedia.org/wiki/Audio_Video_Bridging) (AVB) and [Time-Sensitive Networking](https://en.wikipedia.org/wiki/Time-Sensitive_Networking) (TSN).

## History

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=1)]

According to John Eidson, who led the IEEE 1588-2002 standardization effort, "IEEE 1588 is designed to fill a niche not well served by either of the two dominant protocols, [NTP](https://en.wikipedia.org/wiki/Network_Time_Protocol) and [GPS](https://en.wikipedia.org/wiki/GPS). IEEE 1588 is designed for local systems requiring accuracies beyond those attainable using NTP. It is also designed for applications that cannot bear the cost of a [GPS receiver](https://en.wikipedia.org/wiki/GPS_receiver) at each node, or for which GPS signals are inaccessible."[\[6\]](#cite_note-Eidson-6)

PTP was originally defined in the IEEE 1588-2002 standard, officially titled *Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems*, and published in 2002. In 2008, IEEE 1588-2008 was released as a revised standard; also known as PTP version 2 (PTPv2), it improves accuracy, precision and robustness but is not [backward compatible](https://en.wikipedia.org/wiki/Backward_compatible) with the original 2002 version.<sup>[\[7\]](#cite_note-Eidson2-7)</sup> IEEE 1588-2019 was published in November 2019,<sup>[\[8\]](#cite_note-8)</sup> is informally known as *PTPv2.1* and includes backwards-compatible improvements to the 2008 publication.[\[9\]](#cite_note-Arnold_2017-9)

## Architecture

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=2)]

The IEEE 1588 standards describe a [hierarchical](https://en.wikipedia.org/wiki/Hierarchical) [master–slave architecture](<https://en.wikipedia.org/wiki/Master/slave_(technology)>) for clock [distribution](https://en.wikipedia.org/wiki/Distributed_computing) consisting of one or more [network segments](https://en.wikipedia.org/wiki/Network_segment) and one or more clocks. An *ordinary clock* is a device with a single network connection that is either the source of or the destination for a synchronization reference. A source is called a *master* (alternately *timeTransmitter*<sup>[\[10\]](#cite_note-IEEE_1588g-10)</sup>), and a destination is called a *slave* (alternately *timeReceiver*<sup>[\[10\]](#cite_note-IEEE_1588g-10)</sup>). A *boundary clock* has multiple network connections and synchronizes one network segment to another. A single, synchronization leader is selected, a.k.a. elected, for each network segment. The root timing reference is called the *grandmaster*.[\[11\]](#cite_note-11)

A relatively simple PTP architecture consists of ordinary clocks on a single-segment network with no boundary clocks. A grandmaster is elected and all other clocks synchronize to it.

IEEE 1588-2008 introduces a clock associated with network equipment used to convey PTP messages. The *transparent clock* modifies PTP messages as they pass through the device.[\[12\]](#cite_note-TI2013-12)[Timestamps](https://en.wikipedia.org/wiki/Timestamps) in the messages are corrected for time spent traversing the network equipment. This scheme improves distribution accuracy by compensating for [delivery variability](https://en.wikipedia.org/wiki/Packet_delay_variation) across the network.

PTP typically uses the same [epoch](<https://en.wikipedia.org/wiki/Epoch_(computing)>) as [Unix time](https://en.wikipedia.org/wiki/Unix_time) (start of 1 January 1970).<sup>[\[a\]](#cite_note-14)</sup> While the Unix time is based on [Coordinated Universal Time](https://en.wikipedia.org/wiki/Coordinated_Universal_Time) (UTC) and is subject to [leap seconds](https://en.wikipedia.org/wiki/Leap_second), PTP is based on [International Atomic Time](https://en.wikipedia.org/wiki/International_Atomic_Time) (TAI). The PTP grandmaster communicates the current offset between UTC and TAI, so that UTC can be computed from the received PTP time.

## Protocol details

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=3)]

Synchronization and management of a PTP system is achieved through the exchange of messages across the communications medium. To this end, PTP uses the following message types.

- *Sync* ,*Follow_Up* ,*Delay_Req* and*Delay_Resp* messages are used by*ordinary* and*boundary* clocks and communicate time-related information used to synchronize clocks across the network.
- *Pdelay_Req* ,*Pdelay_Resp* and*Pdelay_Resp_Follow_Up* are used by*transparent* clocks to measure delays across the communications medium so that they can be compensated for by the system.*Transparent* clocks and these messages associated with them are not available in the original IEEE 1588-2002 PTPv1 standard, and were added in PTPv2.
- *Announce* messages are used by the[best master clock algorithm](#Best_master_clock_algorithm) in IEEE 1588-2008 to build a clock hierarchy and select the*grandmaster* .<sup>[\[b\]](#cite_note-15)</sup>
- *Management* messages are used by[network management](https://en.wikipedia.org/wiki/Network_management) to monitor, configure and maintain a PTP system.
- *Signaling* messages are used for non-time-critical communications between clocks. Signaling messages were introduced in IEEE 1588-2008.

Messages are categorized as *event* and *general* messages. *Event* messages are time-critical in that accuracy in transmission and receipt timestamp accuracy directly affects clock distribution accuracy. *Sync*, *Delay_Req*, *Pdelay_Req* and *Pdelay_resp* are *event* messages. *General* messages are more conventional [protocol data units](https://en.wikipedia.org/wiki/Protocol_data_units) in that the data in these messages is of importance to PTP, but their transmission and receipt timestamps are not. *Announce*, *Follow_Up*, *Delay_Resp*, *Pdelay_Resp_Follow_Up*, *Management* and *Signaling* messages are members of the *general* message class.[\[13\]](#cite_note-1588-2008-13)<sup>: Clause 6.4</sup> 

### Message transport

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=4)]

PTP messages may use the [User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol) over [Internet Protocol](https://en.wikipedia.org/wiki/Internet_Protocol) (UDP/IP) for transport. IEEE 1588-2002 uses only [IPv4](https://en.wikipedia.org/wiki/IPv4) transports,[\[14\]](#cite_note-1588-2002-16)<sup>: Annex D</sup>  but this has been extended to include [IPv6](https://en.wikipedia.org/wiki/IPv6) in IEEE 1588-2008.[\[13\]](#cite_note-1588-2008-13)<sup>: Annex F</sup>  In IEEE 1588-2002, all PTP messages are sent using [multicast](https://en.wikipedia.org/wiki/Multicast) messaging, while IEEE 1588-2008 introduced an option for devices to negotiate [unicast](https://en.wikipedia.org/wiki/Unicast) transmission on a port-by-port basis.[\[13\]](#cite_note-1588-2008-13)<sup>: Clause 16.1</sup>  Multicast transmissions use [IP multicast](https://en.wikipedia.org/wiki/IP_multicast) addressing, for which multicast group addresses are defined for IPv4 and IPv6 (see table).[\[13\]](#cite_note-1588-2008-13)<sup>: Annex D and E</sup>  Time-critical *event* messages (Sync, Delay_req, Pdelay_Req and Pdelay_Resp) are sent to [port number](https://en.wikipedia.org/wiki/Port_number) 319. *General* messages (Announce, Follow_Up, Delay_Resp, Pdelay_Resp_Follow_Up, management and signaling) use port number 320.[\[13\]](#cite_note-1588-2008-13)<sup>: Clause 6.4</sup> 

| Multicast group addresses |  |  |  |  | 
|---|---|---|---|---|
| Messages | IPv4 | IPv6 | IEEE 802.3 Ethernet <sup>[\[13\]](#cite_note-1588-2008-13)</sup><sup>: Annex F</sup> <sup>[\[c\]](#cite_note-17)</sup> | Type | 
|---|---|---|---|---|
| All except peer delay messages | 224.0.1.129 <sup>[\[d\]](#cite_note-18)</sup> | FF0x::181 <sup>[\[e\]](#cite_note-19)</sup> | 01-1B-19-00-00-00 <sup>[\[f\]](#cite_note-20)</sup> | Forwardable | 
| Peer delay messages: *Pdelay_Req* ,*Pdelay_Resp* and*Pdelay_Resp_Follow_Up*<sup>[\[g\]](#cite_note-21)</sup> | 224.0.0.107 <sup>[\[h\]](#cite_note-22)</sup> | FF02::6B | 01-80-C2-00-00-0E | Non-forwardable | 

In IEEE 1588-2008, encapsulation is also defined for [DeviceNet](https://en.wikipedia.org/wiki/DeviceNet),[\[13\]](#cite_note-1588-2008-13)<sup>: Annex G</sup>  [ControlNet](https://en.wikipedia.org/wiki/ControlNet)[\[13\]](#cite_note-1588-2008-13)<sup>: Annex H</sup>  and [PROFINET](https://en.wikipedia.org/wiki/PROFINET).[\[13\]](#cite_note-1588-2008-13)<sup>: Annex I</sup> 

### Domains

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=5)]

A domain<sup>[\[i\]](#cite_note-23)</sup> is an interacting set of clocks that synchronize to one another using PTP. Clocks are assigned to a domain by virtue of the contents of the *Subdomain name* (IEEE 1588-2002) or the *domainNumber* (IEEE 1588-2008) fields in PTP messages they receive or generate. Domains allow multiple clock distribution systems to share the same communications medium.

| *Subdomain name* field contents (IEEE1588-2002) | IPv4 multicast address (IEEE1588-2002) <sup>[\[j\]](#cite_note-24)</sup> | *domainNumber*(IEEE1588-2008) | Notes | 
|---|---|---|---|
| _DFLT | 224.0.1.129 | 0 | Default domain | 
| _ALT1 | 224.0.1.130 | 1 | Alternate domain 1 | 
| _ALT2 | 224.0.1.131 | 2 | Alternate domain 2 | 
| _ALT3 | 224.0.1.132 | 3 | Alternate domain 3 | 
| Application specific up to 15 octets <sup>[\[14\]](#cite_note-1588-2002-16)</sup><sup>: Clause 6.2.5.1</sup>  | 224.0.1.130, 131 or 132 as per [hash function](https://en.wikipedia.org/wiki/Hash_function) on*Subdomain name*<sup>[\[14\]](#cite_note-1588-2002-16)</sup><sup>: Annex C</sup>  | 4 through 127 | User-defined domains | 

## Best master clock algorithm

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=6)]

The *best master clock algorithm* (BMCA) performs a distributed selection of the best clock to act as leader based on the following clock properties:

- Identifier – A universally unique numeric identifier for the clock. This is typically constructed based on a device's [MAC address](https://en.wikipedia.org/wiki/MAC_address) .
- Quality – Both versions of IEEE 1588 attempt to quantify clock quality based on expected timing deviation, technology used to implement the clock or location in a [clock stratum](https://en.wikipedia.org/wiki/Clock_stratum) schema, although only V1 (IEEE 1588-2002) knows a data field*stratum* . PTP V2 (IEEE 1588-2008) defines the overall quality of a clock by using the data fields*clockAccuracy* and*clockClass* .
- Priority – An administratively assigned precedence hint used by the BMCA to help select a *grandmaster* for the PTP domain. IEEE 1588-2002 used a single[Boolean variable](https://en.wikipedia.org/wiki/Boolean_variable) to indicate precedence. IEEE 1588-2008 features two 8-bit priority fields.
- Variance – A clock's estimate of its stability based on observation of its performance against the PTP reference.

IEEE 1588-2008 uses a hierarchical selection algorithm based on the following properties, in the indicated order:[\[13\]](#cite_note-1588-2008-13)<sup>: Figure 27</sup> 

1. Priority 1 – the user can assign a specific static-designed priority to each clock, preemptively defining a priority among them. Smaller numeric values indicate higher priority.
2. Class – each clock is a member of a given class, each class getting its own priority.
3. Accuracy – precision between clock and UTC, in nanoseconds (ns)
4. Variance – variability of the clock
5. Priority 2 – final-defined priority, defining backup order in case the other criteria were not sufficient. Smaller numeric values indicate higher priority.
6. Unique identifier – MAC address-based selection is used as a tiebreaker when all other properties are equal.

IEEE 1588-2002 uses a selection algorithm based on similar properties.

Clock properties are advertised in IEEE 1588-2002 *Sync* messages and in IEEE 1588-2008 *Announce* messages. The current leader transmits this information at regular interval. A clock that considers itself a better leader will transmit this information in order to invoke a change of leader. Once the current leader recognizes the better clock, the current leader stops transmitting *Sync* messages and associated clock properties (*Announce* messages in the case of IEEE 1588-2008) and the better clock takes over as leader.<sup>[\[15\]](#cite_note-25)</sup> The BMCA only considers the self-declared quality of clocks and does not take network link quality into consideration.[\[16\]](#cite_note-26)

## Synchronization

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=7)]

Via BMCA, PTP selects a source of time for an IEEE 1588 domain and for each network segment in the domain.

Clocks determine the offset between themselves and their leader.<sup>[\[17\]](#cite_note-IEC-27)</sup> Let the variable  represent physical time. For a given follower device, the offset  at time  is defined by:

where represents the time measured by the follower clock at physical time , and represents the time measured by the leader clock at physical time .

The leader periodically broadcasts the current time as a message to the other clocks. Under IEEE 1588-2002 broadcasts are up to once per second. Under IEEE 1588-2008, up to 10 per second are permitted.

Each broadcast begins at time  with a *Sync* message sent by the leader to all the clocks in the domain. A clock receiving this message takes note of the local time  when this message is received.

The leader may subsequently send a multicast *Follow_Up* with accurate  timestamp. Not all leaders have the ability to present an accurate timestamp in the *Sync* message. It is only after the transmission is complete that they are able to retrieve an accurate timestamp for the *Sync* transmission from their network hardware. Leaders with this limitation use the *Follow_Up* message to convey . Leaders with PTP capabilities built into their network hardware are able to present an accurate timestamp in the *Sync* message and do not need to send Follow_Up messages.

In order to accurately synchronize to their leader, clocks must individually determine the network transit time of the *Sync* messages. The transit time is determined indirectly by measuring round-trip time from each clock to its leader. The clocks initiate an exchange with their leader designed to measure the transit time . The exchange begins with a clock sending a *Delay_Req* message at time  to the leader. The leader receives and timestamps the *Delay_Req* at time  and responds with a *Delay_Resp* message. The leader includes the timestamp  in the *Delay_Resp* message.

Through these exchanges a clock learns , , and .

If  is the transit time for the *Sync* message, and  is the constant offset between leader and follower clocks, then

Combining the above two equations, we find that

The clock now knows the offset during this transaction and can correct itself by this amount to bring it into agreement with their leader.

One assumption is that this exchange of messages happens over a period of time so small that this offset can safely be considered constant over that period. Another assumption is that the transit time of a message going from the leader to a follower is equal to the transit time of a message going from the follower to the leader. Finally, it is assumed that both the leader and follower can accurately measure the time they send or receive a message. The degree to which these assumptions hold true determines the accuracy of the clock at the follower device.[\[13\]](#cite_note-1588-2008-13)<sup>: Clause 6.2</sup> 

## Optional features

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=8)]

IEEE 1588-2008 standard lists the following set of features that implementations may choose to support:

- Alternate Time-Scale
- Grand Master Cluster
- Unicast Masters
- Alternate Master
- Path Trace

IEEE 1588-2019 adds additional optional and backward-compatible features:[\[9\]](#cite_note-Arnold_2017-9)

- Modular transparent clocks
- Special PTP ports to interface with transports with built-in time distribution
- Unicast *Delay_Req* and*Delay_Resp* messages
- Manual port configuration overriding [BMCA](#Best_master_clock_algorithm)
- Asymmetry calibration
- Ability to utilize a physical layer frequency reference (e.g. [Synchronous Ethernet](https://en.wikipedia.org/wiki/Synchronous_Ethernet) )
- Profile isolation
- Inter-domain interactions
- Security TLV for integrity checking
- Standard performance reporting metrics
- Slave port monitoring

## Related initiatives

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=9)]

- The *International IEEE Symposium on Precision Clock Synchronization for Measurement, Control and Communication* (ISPCS) is an IEEE-organized annual event that includes a[plugtest](https://en.wikipedia.org/wiki/Plugtest) and a conference program with paper and poster presentations, tutorials and discussions covering several aspects of PTP.<sup>[\[18\]](#cite_note-28)</sup>
- The Institute of Embedded Systems (InES) of the [Zurich University of Applied Sciences/ZHAW](https://en.wikipedia.org/wiki/Zurich_University_of_Applied_Sciences/ZHAW) is addressing the practical implementation and application of PTP.
- IEEE 1588 is a key technology in the [LXI](https://en.wikipedia.org/wiki/LXI) Standard for Test and Measurement communication and control.
- IEEE 802.1AS-2011 is part of the IEEE [Audio Video Bridging](https://en.wikipedia.org/wiki/Audio_Video_Bridging) (AVB) group of standards.<sup>[\[k\]](#cite_note-29)</sup> It specifies a profile for the use of IEEE 1588-2008 for time synchronization over a virtual bridged local area network as defined by[IEEE 802.1Q](https://en.wikipedia.org/wiki/IEEE_802.1Q) . In particular, 802.1AS defines how[IEEE 802.3](https://en.wikipedia.org/wiki/IEEE_802.3) ([Ethernet](https://en.wikipedia.org/wiki/Ethernet) ),[IEEE 802.11](https://en.wikipedia.org/wiki/IEEE_802.11) ([Wi-Fi](https://en.wikipedia.org/wiki/Wi-Fi) ), and[MoCA](https://en.wikipedia.org/wiki/Multimedia_over_Coax_Alliance) can all be parts of the same PTP timing domain.<sup>[\[19\]](#cite_note-30)</sup>
- [SMPTE 2059](https://en.wikipedia.org/wiki/SMPTE_2059) -2 is a PTP profile for use in synchronization of broadcast media systems.<sup>[\[20\]](#cite_note-31)</sup>
- The [AES67](https://en.wikipedia.org/wiki/AES67) audio networking interoperability standard includes a PTPv2 profile compatible with SMPTE ST2059-2.<sup>[\[21\]](#cite_note-32)</sup>
- [Dante](<https://en.wikipedia.org/wiki/Dante_(networking)>) uses PTPv1 for synchronization.<sup>[\[22\]](#cite_note-coveloz2016-33)</sup>
- [Q-LAN](https://en.wikipedia.org/wiki/Q-LAN)<sup>[\[23\]](#cite_note-34)</sup> and[RAVENNA](<https://en.wikipedia.org/wiki/Ravenna_(networking)>)<sup>[\[22\]](#cite_note-coveloz2016-33)</sup> use PTPv2 for time synchronization.
- [The White Rabbit Project](https://en.wikipedia.org/wiki/The_White_Rabbit_Project) combines[Synchronous Ethernet](https://en.wikipedia.org/wiki/Synchronous_Ethernet) and PTP.
- [Precision Time Protocol Industry Profile](https://en.wikipedia.org/wiki/Precision_Time_Protocol_Industry_Profile) PTP profiles (L2P2P and L3E2E) for industrial automation in IEC 62439-3
- [IEC/IEEE 61850-9-3](https://en.wikipedia.org/wiki/IEC/IEEE_61850-9-3) PTP profile for substation automation adopted by IEC 61850
- [Parallel Redundancy Protocol](https://en.wikipedia.org/wiki/Parallel_Redundancy_Protocol) use of PTP profiles (L2P2P and L3E2E) for industrial automation in parallel networks
- PTP is being studied to be applied as a secure time synchronization protocol in power systems' Wide Area Monitoring<sup>[\[24\]](#cite_note-35)</sup>

## See also

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=10)]

- [List of PTP implementations](https://en.wikipedia.org/wiki/List_of_PTP_implementations) – Systems supporting Precision Time Protocol
- [Real-time communication](https://en.wikipedia.org/wiki/Real-time_communication) – Protocols and communication hardware that give real-time guarantees

## Notes

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=11)]

1. [↑](#cite_ref-14) The profile capability under IEEE 1588-2008 allows the use of application-specific epochs.<sup>[\[13\]](#cite_note-1588-2008-13)</sup><sup>: Annex B</sup> 
2. [↑](#cite_ref-15) In IEEE 1588-2002, information carried by*Announce* messages is carried in the*Sync* messages. In IEEE 1588-2008, the*Sync* message has been optimized and this information is no longer carried here.
3. [↑](#cite_ref-17) PTP over bare IEEE 802.3 Ethernet using[Ethertype](https://en.wikipedia.org/wiki/Ethertype) 0x88F7
4. [↑](#cite_ref-18) IEEE 1588-2002 non-default domains use destination addresses 224.0.1.130 through 224.0.1.132 (see[#Domains](#Domains) ).
5. [↑](#cite_ref-19) Where*x* is the address scope (2 for link-local) as per RFC 2373 (see[IPv6 multicast address](https://en.wikipedia.org/wiki/Multicast_address#IPv6) )
6. [↑](#cite_ref-20) In some PTP applications, it is permissible to send all PTP messages to 01-1B-19-00-00-00
7. [↑](#cite_ref-21) Peer delay messages are intended to propagate to the immediately connected neighbor. The multicast addresses for these messages are designed to be link-local in scope and are not passed through a[router](<https://en.wikipedia.org/wiki/Router_(computing)>) . IEEE 1588-2008 also recommends setting[time to live](https://en.wikipedia.org/wiki/Time_to_live) to 1 (IPv4) or hop limit to 0 (IPv6) as further insurance that the messages will not be routed.
8. [↑](#cite_ref-22) Peer delay messaging is not present in IEEE 1588-2002
9. [↑](#cite_ref-23) IEEE 1588-2002 defines a*domain* as any interconnected set of clocks (regardless of whether they are synchronized to one another) and uses*subdomain* to refer to what is known as a*domain* in IEEE 1588-2008.
10. [↑](#cite_ref-24) IEEE 1588-2008 uses 224.0.1.129 as the address for all multicast messages.
11. [↑](#cite_ref-29) AVB is further extended by the IEEE 802.1[Time-Sensitive Networking](https://en.wikipedia.org/wiki/Time-Sensitive_Networking) (TSN) Task Group.

## References

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=12)]

1. [↑](#cite_ref-1) Eidson, John (10 October 2005).["IEEE-1588 Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems, a Tutorial"](https://www.nist.gov/document/tutorial-basicpdf) . National Institute of Standards and Technology (NIST).
2. [↑](#cite_ref-2) Oehler, Erik (19 July 2023).["The Significance of Accurate Timekeeping and Synchronization in Trading Systems"](https://safran-navigation-timing.com/timekeeping-and-synchronization-in-trading-systems/) .*Safran - Navigation & Timing* . Retrieved 3 December 2025.
3. [↑](#cite_ref-3)["Celona PTP Guidelines and Best Practices | Celona Help Center"](https://docs.celona.io/en/articles/10581128-celona-ptp-guidelines-and-best-practices) .*docs.celona.io* . Retrieved 3 December 2025.
4. [↑](#cite_ref-4) Wei, Zhengrong; Pei, Yanliang; Zhu, Xiangqian; Liu, Kai; Zhang, Xiaobo; Zong, Le; Li, Xinyu (29 July 2024).["A high-precision positioning method for deep-towed multichannel seismic arrays"](https://doi.org/10.3389%2Ffmars.2024.1351327) .*Frontiers in Marine Science* .**11** 1351327.[Bibcode](<https://en.wikipedia.org/wiki/Bibcode_(identifier)>) :[2024FrMaS..1151327W](https://ui.adsabs.harvard.edu/abs/2024FrMaS..1151327W) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.3389/fmars.2024.1351327](https://doi.org/10.3389%2Ffmars.2024.1351327) .[ISSN](<https://en.wikipedia.org/wiki/ISSN_(identifier)>)[2296-7745](https://search.worldcat.org/issn/2296-7745) .
5. [↑](#cite_ref-5) Austin (18 February 2025).["Nanosecond accurate PTP server (grandmaster) and client tutorial for Raspberry Pi"](https://austinsnerdythings.com/2025/02/18/nanosecond-accurate-ptp-server-grandmaster-and-client-tutorial-for-raspberry-pi/) .*Austin's Nerdy Things* . Retrieved 3 December 2025.
6. [↑](#cite_ref-Eidson_6-0) Eidson, John C. (April 2006).*Measurement, Control and Communication Using IEEE 1588* .[Springer](https://en.wikipedia.org/wiki/Springer_Science+Business_Media) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-1-84628-250-8](https://en.wikipedia.org/wiki/Special:BookSources/978-1-84628-250-8) .
7. [↑](#cite_ref-Eidson2_7-0) Eidson, John (2 October 2006).["IEEE 1588 Standard Version 2 - A Tutorial"](https://web.archive.org/web/20100331083017/http://ieee1588.nist.gov/2006%20IEEE1588%20Agenda/Eidson_1588_Version%202.pdf) (PDF). Archived from[the original](http://ieee1588.nist.gov/2006%20IEEE1588%20Agenda/Eidson_1588_Version%202.pdf) (PDF) on 31 March 2010. Retrieved 12 June 2008.
8. [↑](#cite_ref-8)["1588-2019 - IEEE Approved Draft Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems"](https://standards.ieee.org/ieee/1588/6825/) . IEEE. Retrieved 15 February 2020.
9. [1](#cite_ref-Arnold_2017_9-0)[2](#cite_ref-Arnold_2017_9-1) Douglas Arnold (24 September 2017).["What's coming In the Next Edition of IEEE 1588?"](https://blog.meinbergglobal.com/2017/09/24/whats-coming-next-edition-ieee-1588/) . Retrieved 15 February 2020.
10. [1](#cite_ref-IEEE_1588g_10-0)[2](#cite_ref-IEEE_1588g_10-1)*IEEE 1588g-2022 Amendment 2: Master-Slave Optional Alternative Terminology* ,[IEEE](https://en.wikipedia.org/wiki/IEEE) , 3 December 2022
11. [↑](#cite_ref-11)["Meanings of common terms used in IEEE 1588"](https://web.archive.org/web/20100527161310/http://ieee1588.nist.gov/terms.htm) . National Institute of Standards and Technology. Archived from[the original](http://ieee1588.nist.gov/terms.htm) on 27 May 2010. Retrieved 19 May 2006.
12. [↑](#cite_ref-TI2013_12-0)["AN-1838 IEEE 1588 Boundary Clock and Transparent Clock Implementation Using the DP83640"](http://www.ti.com/lit/an/snla104a/snla104a.pdf) (PDF).*ti.com* . Texas Instruments. Retrieved 17 July 2019.
13. [1](#cite_ref-1588-2008_13-0)[2](#cite_ref-1588-2008_13-1)[3](#cite_ref-1588-2008_13-2)[4](#cite_ref-1588-2008_13-3)[5](#cite_ref-1588-2008_13-4)[6](#cite_ref-1588-2008_13-5)[7](#cite_ref-1588-2008_13-6)[8](#cite_ref-1588-2008_13-7)[9](#cite_ref-1588-2008_13-8)[10](#cite_ref-1588-2008_13-9)[11](#cite_ref-1588-2008_13-10)[12](#cite_ref-1588-2008_13-11)*IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems* ,[IEEE](https://en.wikipedia.org/wiki/IEEE) , 24 July 2008,[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/IEEESTD.2008.4579760](https://doi.org/10.1109%2FIEEESTD.2008.4579760) ,[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-7381-5400-8](https://en.wikipedia.org/wiki/Special:BookSources/978-0-7381-5400-8)
14. [1](#cite_ref-1588-2002_16-0)[2](#cite_ref-1588-2002_16-1)[3](#cite_ref-1588-2002_16-2)*IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems* ,[IEEE](https://en.wikipedia.org/wiki/IEEE) , 8 November 2002,[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/IEEESTD.2002.94144](https://doi.org/10.1109%2FIEEESTD.2002.94144) ,[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-7381-3369-0](https://en.wikipedia.org/wiki/Special:BookSources/978-0-7381-3369-0)
15. [↑](#cite_ref-25) Watt, Steve T.; Achanta, Shankar; Abubakari, Hamza; Sagen, Eric (March 2014),[*Understanding and Applying Precision Time Protocol*](https://cdn.selinc.com/assets/Literature/Publications/Technical%20Papers/6650_UnderstandingApplying_SA_20140206_Web3.pdf) (PDF), retrieved 9 September 2017
16. [↑](#cite_ref-26) FSMLabs Technical Staff (September 2015),[*Smart and Dumb PTP Client and the "so-called" Best Master Clock Algorithm*](http://www.fsmlabs.com/news/2015/09/18/socalledbestmasterclock.html) , retrieved 17 May 2018
17. [↑](#cite_ref-IEC_27-0)[International standard](https://en.wikipedia.org/wiki/International_standard)[IEC](https://en.wikipedia.org/wiki/IEC) 61588: Precision clock synchronization protocol for networked measurement and control systems. 2004.
18. [↑](#cite_ref-28)[ISPCS website](http://www.ispcs.org)
19. [↑](#cite_ref-30) Geoffrey M. Garner (28 May 2010),[*IEEE 802.1AS and IEEE 1588*](https://www.itu.int/dms_pub/itu-t/oth/06/38/T06380000040002PDFE.pdf) (PDF)
20. [↑](#cite_ref-31)[*SMPTE Publishes First Two Parts of Standard Enabling Deployment of PTP-Timed Equipment in Existing SDI Plants*](https://www.smpte.org/news-events/news-releases/smpte%C2%AE-publishes-first-two-parts-standard-enabling-deployment-ptp-timed) ,[Society of Motion Picture and Television Engineers](https://en.wikipedia.org/wiki/Society_of_Motion_Picture_and_Television_Engineers) , 13 April 2015, retrieved 21 May 2015
21. [↑](#cite_ref-32)[*AES-R16-2016: AES Standards Report - PTP parameters for AES67 and SMPTE ST 2059-2 interoperability*](http://www.aes.org/publications/standards/search.cfm?docID=105) ,[Audio Engineering Society](https://en.wikipedia.org/wiki/Audio_Engineering_Society) , 2 May 2016
22. [1](#cite_ref-coveloz2016_33-0)[2](#cite_ref-coveloz2016_33-1)[https://www.smpte.org/sites/default/files/users/user27446/AES67%20for%20Audio%20Production-Background%20Applications%20and%20Challenges.pdf](https://www.smpte.org/sites/default/files/users/user27446/AES67%20for%20Audio%20Production-Background%20Applications%20and%20Challenges.pdf)<sup>[*[dead link](https://en.wikipedia.org/wiki/Wikipedia:Link_rot)*]</sup>
23. [↑](#cite_ref-34) Oyen, Seppe (6 June 2017).["PTPv2 Timing protocol in AV networks"](https://web.archive.org/web/20190825154107/https://www.luminex.be/improve-your-timekeeping-with-ptpv2/) .*Luminex* . Archived from[the original](https://www.luminex.be/improve-your-timekeeping-with-ptpv2/) on 25 August 2019. Retrieved 10 January 2019.Q-LAN updated to PTPv2 approximately two years ago.
24. [↑](#cite_ref-35) Pepiciello, Antonio; Vaccaro, Alfredo (17 December 2018), "A reliable architecture based on Precision Time Protocol for WAMPAC synchronization",*2018 AEIT International Annual Conference* ,[IEEE](https://en.wikipedia.org/wiki/IEEE) , pp. 1–5,[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.23919/AEIT.2018.8577414](https://doi.org/10.23919%2FAEIT.2018.8577414) ,[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-8-8872-3740-5](https://en.wikipedia.org/wiki/Special:BookSources/978-8-8872-3740-5) ,[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[58819556](https://api.semanticscholar.org/CorpusID:58819556)

## External links

[
[edit](/w/index.php?title=Precision_Time_Protocol&action=edit§ion=13)]

- [NIST IEEE 1588 site](https://www.nist.gov/el/intelligent-systems-division-73500/ieee-1588)
- [PTP documentation at InES](https://web.archive.org/web/20131206102327/http://www.zhaw.ch/en/engineering/institutes-centres/ines/downloads/documents.html)
- [PTP and Synchronization of LTE mobile networks](https://www.albedotelecom.com/src/lib/WP-Mobile-PTP.pdf)
- [PTP explained under the installation / maintenance point of view](https://www.albedotelecom.com/src/lib/WP-PTP.pdf)
- [Hirschmann PTP Whitepaper](https://web.archive.org/web/20110818184219/http://www.belden.com/pdfs/Techpprs/Precision_Clock_Synchronization_WP.pdf)
- [PTP overview in Cisco CGS 2520 Switch Software Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/connectedgrid/cgs2520/software/release/12_2_58_ey/configuration/cgs_2520_swcg.html#wp1988925)
- [Perspectives and priorities on RuggedCom Smart Grid Research IEC 61850 Technologies](https://web.archive.org/web/20160304192052/http://www.bcit.ca/files/appliedresearch/pdf/ruggedcom_industry.pdf)
- [Projects with Smart Substation Solution](https://web.archive.org/web/20120114222001/http://xn--61850-txen0l.xn--p1ai/wp-content/plugins/downloads-manager/upload/Introduction%20of%20Smart%20Subsltation%20Projects.pdf)
- McGhee, Jim; Goraj, Maciej (2010), "Smart High Voltage Substation Based on IEC 61850 Process Bus and IEEE 1588 Time Synchronization", *2010 First IEEE International Conference on Smart Grid Communications* , pp. 489–494,[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/SMARTGRID.2010.5622092](https://doi.org/10.1109%2FSMARTGRID.2010.5622092) ,[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-1-4244-6510-1](https://en.wikipedia.org/wiki/Special:BookSources/978-1-4244-6510-1) ,[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[30638718](https://api.semanticscholar.org/CorpusID:30638718)
- Ingram, D.M.E; Campbell, D.A.; Schaub, P.; Ledwich, G.F. (2011). ["Test and evaluation system for multi-protocol sampled value protection schemes"](https://eprints.qut.edu.au/41257/) .*2011 IEEE Trondheim PowerTech* . Trondheim, Norway: IEEE. pp. 1–7.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/PTC.2011.6019243](https://doi.org/10.1109%2FPTC.2011.6019243) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-1-4244-8419-5](https://en.wikipedia.org/wiki/Special:BookSources/978-1-4244-8419-5) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[42991214](https://api.semanticscholar.org/CorpusID:42991214) .
- [The White Rabbit Project PTP](https://safran-navigation-timing.com/solution/white-rabbit-solutions/)
- [IEC&IEEE Precision Time Protocol](https://web.archive.org/web/20170205095756/http://lamspeople.epfl.ch/kirrmann/Pubs/IEC_62439-3/PacWorld_038_043_IEC_IEEE_61850-9-3_September_2016_HK.pdf)*, Pacworld, September 2016*
- [IEC 62439-3 Annexes A-E Redundant attachment of clocks and network management](https://webstore.iec.ch/publication/24447)
- [PTPv2 Timing protocol in AV networks](https://www.luminex.be/improve-your-timekeeping-with-ptpv2-2/)
- [FSMLabs: Single source IEEE PTP 1588 cannot meet financial regulatory standards](https://www.fsmlabs.com/news/2016/03/31/singlesource.html)
- [A PTP Testing Guide for Reliable and Accurate Verification](https://blog.albedotelecom.com/ptp-testing-guide/) by Fran Hens (ALBEDO 2019)
