---
title: Remote direct memory access - Wikipedia
source: https://en.wikipedia.org/wiki/Remote_direct_memory_access
published: '2004-10-22'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Remote direct memory access - Wikipedia

# Remote direct memory access

In [computing](https://en.wikipedia.org/wiki/Computing), **remote direct memory access** (**RDMA**) is [direct memory access](https://en.wikipedia.org/wiki/Direct_memory_access) from the [memory](https://en.wikipedia.org/wiki/Computer_data_storage) of one computer into that of another without involving either computer's [operating system](https://en.wikipedia.org/wiki/Operating_system). This permits high-throughput, low-[latency](https://en.wikipedia.org/wiki/Network_latency) memory access over a network, which is especially useful in massively parallel [computer clusters](https://en.wikipedia.org/wiki/Computer_cluster).

## Overview

[
[edit](/w/index.php?title=Remote_direct_memory_access&action=edit§ion=1)]

RDMA supports [zero-copy](https://en.wikipedia.org/wiki/Zero-copy) networking by enabling the [network adapter](https://en.wikipedia.org/wiki/Network_adapter) to transfer data from the wire directly to application memory or from application memory directly to the wire, eliminating the need to copy data between application memory and the data buffers in the operating system. Such transfers require no work to be done by [CPUs](https://en.wikipedia.org/wiki/Central_processing_unit), [caches](https://en.wikipedia.org/wiki/CPU_cache), or [context switches](https://en.wikipedia.org/wiki/Context_switch), and transfers continue in parallel with other system operations. This reduces latency in message transfer.

However, this strategy presents several problems related to the fact that the target node is not notified of the completion of the request (single-sided communications).

## Acceptance

[
[edit](/w/index.php?title=Remote_direct_memory_access&action=edit§ion=2)]

As of 2018 RDMA had achieved broader acceptance as a result of implementation enhancements that enable good performance over ordinary networking infrastructure.<sup>[\[1\]](#cite_note-1)</sup> For example [RDMA over Converged Ethernet](https://en.wikipedia.org/wiki/RDMA_over_Converged_Ethernet) (RoCE) now is able to run over either lossy or lossless infrastructure. In addition [iWARP](https://en.wikipedia.org/wiki/IWARP) enables an [Ethernet](https://en.wikipedia.org/wiki/Ethernet) RDMA implementation at the physical layer using [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)/[IP](https://en.wikipedia.org/wiki/Internet_Protocol) as the transport, combining the performance and latency advantages of RDMA with a low-cost, standards-based solution.<sup>[\[2\]](#cite_note-2)</sup>  The RDMA Consortium and the DAT Collaborative<sup>[\[3\]](#cite_note-3)</sup> have played key roles in the development of RDMA protocols and [APIs](https://en.wikipedia.org/wiki/Application_programming_interface) for consideration by standards groups such as the [Internet Engineering Task Force](https://en.wikipedia.org/wiki/Internet_Engineering_Task_Force) and the Interconnect Software Consortium.[\[4\]](#cite_note-4)

Hardware vendors have started working on higher-capacity RDMA-based network adapters, with rates of 100 Gbit/s reported.[\[5\]](#cite_note-5)<sup>[\[6\]](#cite_note-chelsio-6)</sup> Software vendors, such as [IBM](https://en.wikipedia.org/wiki/IBM),[\[7\]](#cite_note-7)[Red Hat](https://en.wikipedia.org/wiki/Red_Hat) and [Oracle Corporation](https://en.wikipedia.org/wiki/Oracle_Corporation), support these APIs in their latest products,<sup>[\[8\]](#cite_note-8)</sup> and since 2013, engineers have been developing network adapters that implement RDMA over Ethernet.<sup>[\[9\]](#cite_note-9)</sup> 
Both [Red Hat Enterprise Linux](https://en.wikipedia.org/wiki/Red_Hat_Enterprise_Linux) and [Red Hat Enterprise MRG](https://en.wikipedia.org/wiki/Red_Hat_Enterprise_MRG)<sup>[\[10\]](#cite_note-10)</sup> have support for RDMA. Microsoft supports RDMA in [Windows Server 2012](https://en.wikipedia.org/wiki/Windows_Server_2012) via [SMB Direct](https://en.wikipedia.org/wiki/Server_Message_Block). [VMware ESXi](https://en.wikipedia.org/wiki/VMware_ESXi) also supports RDMA as of 2015.

Common RDMA implementations include the [Virtual Interface Architecture](https://en.wikipedia.org/wiki/Virtual_Interface_Architecture), [RDMA over Converged Ethernet](https://en.wikipedia.org/wiki/RDMA_over_Converged_Ethernet) (RoCE), [InfiniBand](https://en.wikipedia.org/wiki/InfiniBand), [Omni-Path](https://en.wikipedia.org/wiki/Omni-Path), [iWARP](https://en.wikipedia.org/wiki/IWARP) and Ultra Ethernet.

## Using RDMA

[
[edit](/w/index.php?title=Remote_direct_memory_access&action=edit§ion=3)]

Applications access control structures using well-defined APIs originally designed for the InfiniBand Protocol (although the APIs can be used for any of the underlying RDMA implementations). Using send and completion queues, applications perform RDMA operations by submitting work queue entries (WQEs) into the submission queue (SQ) and getting notified of responses from the completion queue (CQ).[\[11\]](#cite_note-11)

## Transport types

[
[edit](/w/index.php?title=Remote_direct_memory_access&action=edit§ion=4)]

RDMA can transport data reliably or unreliably over the Reliably Connected (RC) and Unreliable Datagram (UD) transport protocols, respectively. The former has the benefit of preserving requests (no requests are lost), while the latter requires fewer queue pairs when handling multiple connections. This is due to the fact that UD is connection-less, allowing a single host to communicate with any other using a single queue.[\[12\]](#cite_note-12)

## References

[
[edit](/w/index.php?title=Remote_direct_memory_access&action=edit§ion=5)]

1. [↑](#cite_ref-1) RoCE Rocks over Lossy Network:[https://dl.acm.org/citation.cfm?id=3098588&dl=ACM&coll=DL](https://dl.acm.org/citation.cfm?id=3098588&dl=ACM&coll=DL)
2. [↑](#cite_ref-2)["Understanding iWARP"](https://www.intel.com/content/dam/support/us/en/documents/network/sb/understanding_iwarp_final.pdf) (PDF). Intel Corporation. Retrieved 16 May 2018.
3. [↑](#cite_ref-3)["DAT Collaborative website"](https://web.archive.org/web/20150117180600/http://www.datcollaborative.org/) . Archived from[the original](http://www.datcollaborative.org/) on 17 January 2015. Retrieved 14 October 2014.
4. [↑](#cite_ref-4)[The Interconnect Software Consortium website](http://www.opengroup.org/icsc/)[Archived](https://web.archive.org/web/20050830201232/http://www.opengroup.org/icsc/) 2005-08-30 at the[Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine)
5. [↑](#cite_ref-5)["Microsoft Based Solutions - Mellanox Technologies"](http://www.mellanox.com/page/file_storage/) . Retrieved 14 October 2014.
6. [↑](#cite_ref-chelsio_6-0)["40Gbe SMB Direct RDMA Over Ethernet For Windows Server 2012 - Chelsio Communications"](http://www.chelsio.com/chelsio-to-demonstrate-40g-smb-direct-rdma-over-ethernet-for-windows-server-2012/) . 2 April 2013. Retrieved 14 October 2014.
7. [↑](#cite_ref-7)["SOFA-STORAGE: CREATING A VENDOR AGNOSTIC FRAMEWORK TO ENABLE SEAMLESS STORAGE OFFLOAD USING SMARTNICS"](https://www.openfabrics.org/wp-content/uploads/2022-workshop/2022-workshop-presentations/201_RPolig.pdf) (PDF).
8. [↑](#cite_ref-8)["What RDMA hardware is supported in Red Hat Enterprise Linux?"](https://access.redhat.com/solutions/22188) . 2 June 2016.
9. [↑](#cite_ref-9)["40Gbe SMB Direct RDMA Over Ethernet For Windows Server 2012 - Chelsio Communications"](http://www.chelsio.com/chelsio-to-demonstrate-40g-smb-direct-rdma-over-ethernet-for-windows-server-2012/) . Chelsio Communications. 2013-04-02. Retrieved 2016-07-15.The demonstration will show Microsoft's Windows Server 2012 SMB Direct running at line-rate 40Gb using RDMA over Ethernet (iWARP).
10. [↑](#cite_ref-10)["Red Hat Enterprise MRG 2.0 Now Available"](https://web.archive.org/web/20160825215016/https://investors.redhat.com/news-and-events/press-releases/2011/06-23-2011) . Archived from[the original](https://investors.redhat.com/news-and-events/press-releases/2011/06-23-2011) on 25 August 2016. Retrieved 23 June 2011.
11. [↑](#cite_ref-11) Storm: a fast transactional dataplane for remote data structures:[https://dl.acm.org/doi/abs/10.1145/3319647.3325827](https://dl.acm.org/doi/abs/10.1145/3319647.3325827)
12. [↑](#cite_ref-12) Storm: a fast transactional dataplane for remote data structures:[https://dl.acm.org/doi/pdf/10.1145/3319647.3325827](https://dl.acm.org/doi/pdf/10.1145/3319647.3325827)

## External links

[
[edit](/w/index.php?title=Remote_direct_memory_access&action=edit§ion=6)]

- [RDMA Consortium](http://www.rdmaconsortium.org/)
- [RFC](<https://en.wikipedia.org/wiki/RFC_(identifier)>)[5040](https://www.rfc-editor.org/rfc/rfc5040) : A Remote Direct Memory Access Protocol Specification
- [A Tutorial of the RDMA Model](http://www.hpcwire.com/2006/09/15/a_tutorial_of_the_rdma_model-1/)
- ["Why Compromise?"](https://www.hpcwire.com/2006/10/06/why_compromise-1/) // HPCwire, Gilad Shainer (Mellanox Technologies), 2006
- [A Critique of RDMA](http://www.hpcwire.com/hpcwire/2006-08-18/a_critique_of_rdma-1.html) for high-performance computing
- [RDMA Reads: To Use or Not to Use?](https://www.cs.utah.edu/~stutsman/cs6450/public/papers/rdma.pdf)
