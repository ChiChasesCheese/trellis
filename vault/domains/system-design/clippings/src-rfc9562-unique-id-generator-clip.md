---
title: Universally Unique IDentifiers (UUIDs)
source: https://www.rfc-editor.org/rfc/rfc9562.html
author: Kyzer R Davis; Brad G Peabody; Paul J Leach
published: '1997-03-20'
site: rfc-editor.org
clipped: '2026-09-20'
---

# Universally Unique IDentifiers (UUIDs)

| RFC 9562 | UUIDs | May 2024 | 
| Davis, et al. | Standards Track | [Page] | 

This specification defines UUIDs (Universally Unique IDentifiers) --
      also known as GUIDs (Globally Unique IDentifiers) -- and a Uniform
      Resource Name namespace for UUIDs. A UUID is 128 bits long and is intended to
      guarantee uniqueness across space and time.  UUIDs were originally used
      in the Apollo Network Computing System (NCS), later in the Open Software
      Foundation's (OSF's) Distributed Computing Environment (DCE), and then
      in Microsoft Windows platforms.[¶](#section-abstract-1)

This specification is derived from the OSF DCE specification with the
      kind permission of the OSF (now known as "The Open Group").  Information
      from earlier versions of the OSF DCE specification have been incorporated
      into this document. This document obsoletes RFC 4122.[¶](#section-abstract-2)

            This is an Internet Standards Track document.[¶](#section-boilerplate.1-1)

            This document is a product of the Internet Engineering Task Force
            (IETF).  It represents the consensus of the IETF community.  It has
            received public review and has been approved for publication by
            the Internet Engineering Steering Group (IESG).  Further
            information on Internet Standards is available in Section 2 of 
            RFC 7841.[¶](#section-boilerplate.1-2)

            Information about the current status of this document, any
            errata, and how to provide feedback on it may be obtained at
            [https://www.rfc-editor.org/info/rfc9562](https://www.rfc-editor.org/info/rfc9562).[¶](#section-boilerplate.1-3)

            Copyright (c) 2024 IETF Trust and the persons identified as the
            document authors. All rights reserved.[¶](#section-boilerplate.2-1)

            This document is subject to BCP 78 and the IETF Trust's Legal
            Provisions Relating to IETF Documents
            ([https://trustee.ietf.org/license-info](https://trustee.ietf.org/license-info)) in effect on the date of
            publication of this document. Please review these documents
            carefully, as they describe your rights and restrictions with
            respect to this document. Code Components extracted from this
            document must include Revised BSD License text as described in
            Section 4.e of the Trust Legal Provisions and are provided without
            warranty as described in the Revised BSD License.[¶](#section-boilerplate.2-2)

This specification defines a Uniform Resource Name namespace for
   Universally Unique IDentifiers (UUIDs), also known as Globally
   Unique IDentifiers (GUIDs).  A UUID is 128 bits long and
      requires no central registration process.[¶](#section-1-1)

The use of UUIDs is extremely pervasive in computing.  They comprise
      the core identifier infrastructure for many operating systems such as
      Microsoft Windows and applications such as the Mozilla Web browser;
      in many cases, they can become exposed in many non-standard ways.[¶](#section-1-2)

This specification attempts to standardize that practice as openly as
      possible and in a way that attempts to benefit the entire Internet.  The information
      here is meant to be a concise guide for those wishing to implement
      services using UUIDs either in combination with URNs [[RFC8141](#RFC8141)] or otherwise.[¶](#section-1-3)

There is an ITU-T Recommendation and an ISO/IEC Standard [[X667](#X667)] that are derived from [[RFC4122](#RFC4122)].  Both
      sets of specifications have been aligned and are fully technically
      compatible.  Nothing in this document should be construed to override
      the DCE standards that defined UUIDs.[¶](#section-1-4)

One of the main reasons for using UUIDs is that no centralized
      authority is required to administer them (although two formats may
      leverage optional IEEE 802 Node IDs, others do not).  As a
      result, generation on demand can be completely automated and used for a
      variety of purposes.  The UUID generation algorithm described here
      supports very high allocation rates of 10 million per second per machine
      or more, if necessary, so that they could even be used as transaction
      IDs.[¶](#section-2-1)

UUIDs are of a fixed size (128 bits), which is reasonably small
      compared to other alternatives.  This lends itself well to sorting,
      ordering, and hashing of all sorts; storing in databases; simple
      allocation; and ease of programming in general.[¶](#section-2-2)

Since UUIDs are unique and persistent, they make excellent URNs. 
      The unique ability to generate a new UUID without a
      registration process allows for UUIDs to be one of the URNs with the
      lowest minting cost.[¶](#section-2-3)

Many things have changed in the time since UUIDs were originally
        created.  Modern applications have a need to create and utilize UUIDs
        as the primary identifier for a variety of different items in complex
        computational systems, including but not limited to database keys,
        file names, machine or system names, and identifiers for event-driven
        transactions.[¶](#section-2.1-1)

One area in which UUIDs have gained popularity is database keys.
        This stems from the increasingly distributed nature of modern
        applications.  In such cases, "auto-increment" schemes that are often
        used by databases do not work well: the effort required to
        coordinate sequential numeric identifiers across a network can easily
        become a burden.  The fact that UUIDs can be used to create unique,
        reasonably short values in distributed systems without requiring
        coordination makes them a good alternative, but UUID versions 1-5,
        which were originally defined by [[RFC4122](#RFC4122)], lack
        certain other desirable characteristics, such as:[¶](#section-2.1-2)

Due to the aforementioned issues, many widely distributed database
        applications and large application vendors have sought to solve the
        problem of creating a better time-based, sortable unique identifier
        for use as a database key. This has led to numerous implementations
        over the past 10+ years solving the same problem in slightly different
        ways.[¶](#section-2.1-4)

While preparing this specification, the following 16 different
        implementations were analyzed for trends in total ID length, bit
        layout, lexical formatting and encoding, timestamp type, timestamp
        format, timestamp accuracy, node format and components, collision
        handling, and multi-timestamp tick generation sequencing:[¶](#section-2.1-5)

An inspection of these implementations and the issues described
        above has led to this document, in which new UUIDs are adapted to
        address these issues.[¶](#section-2.1-7)

Further, [[RFC4122](#RFC4122)] itself was in need of an overhaul to
        address a number of topics such as, but not limited to, the
        following:[¶](#section-2.1-8)

The key words "MUST", "MUST NOT",
        "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
        "RECOMMENDED", "NOT RECOMMENDED",
        "MAY", and "OPTIONAL" in this document
        are to be interpreted as described in BCP 14 [[RFC2119](#RFC2119)] [[RFC8174](#RFC8174)] when, and only when, they
        appear in all capitals, as shown here.[¶](#section-3.1-1)

The following abbreviations are used in this document:[¶](#section-3.2-1)

The UUID format is 16 octets (128 bits) in size; the variant bits in
      conjunction with the version bits described in the next sections
      determine finer structure. In terms of these UUID formats and layout, bit
      definitions start at 0 and end at 127, while octet definitions start at 0
      and end at 15.[¶](#section-4-1)

In the absence of explicit application or presentation protocol
      specification to the contrary, each field is encoded with the most
      significant byte first (known as "network byte order").[¶](#section-4-2)

Saving UUIDs to binary format is done by sequencing all fields in
      big-endian format.  However, there is a known caveat that Microsoft's
      Component Object Model (COM) GUIDs leverage little-endian when saving
      GUIDs.  The discussion of this (see [[MS_COM_GUID](#MS_COM_GUID)]) is outside
      the scope of this specification.[¶](#section-4-3)

UUIDs MAY be represented as binary data or integers.
      When in use with URNs or as text in applications, any given UUID should
      be represented by the "hex-and-dash" string format consisting of
      multiple groups of uppercase or lowercase alphanumeric hexadecimal
      characters separated by single dashes/hyphens.  When used with databases,
      please refer to [Section 6.13](#database_considerations).[¶](#section-4-4)

The formal definition of the UUID string representation is provided by the following ABNF [[RFC5234](#RFC5234)]:[¶](#section-4-5)

```
UUID     = 4hexOctet "-"
           2hexOctet "-"
           2hexOctet "-"
           2hexOctet "-"
           6hexOctet
hexOctet = HEXDIG HEXDIG
DIGIT    = %x30-39
HEXDIG   = DIGIT / "A" / "B" / "C" / "D" / "E" / "F"
```
Note that the alphabetic characters may be all uppercase, all lowercase, or mixed case, as per [Section 2.3](https://rfc-editor.org/rfc/rfc5234#section-2.3) of [[RFC5234](#RFC5234)].
An example UUID using this textual representation from the above ABNF is shown in [Figure 1](#sampleStringUUID).[¶](#section-4-7)

The same UUID from [Figure 1](#sampleStringUUID) is represented in binary ([Figure 2](#sampleBinaryUUID)), as an unsigned integer ([Figure 3](#sampleIntegerUUID)), and as a URN ([Figure 4](#sampleURNUUID)) defined by [[RFC8141](#RFC8141)].[¶](#section-4-9)

There are many other ways to define a UUID format; some examples are detailed below.
Please note that this is not an exhaustive list and is only provided for informational purposes.[¶](#section-4-13)

The variant field determines the layout of the UUID.  That is, the
        interpretation of all other bits in the UUID depends on the setting of
        the bits in the variant field.  As such, it could more accurately be
        called a "type" field; we retain the original term for compatibility.
        The variant field consists of a variable number of the most
        significant bits of octet 8 of the UUID.[¶](#section-4.1-1)

[Table 1](#table1) lists the contents of the variant field,
        where the letter "x" indicates a "don't-care" value.[¶](#section-4.1-2)

| Table 1 :  UUID Variants |  |  |  |  |  | 
|---|---|---|---|---|---|
| MSB0 | MSB1 | MSB2 | MSB3 | Variant | Description | 
|---|---|---|---|---|---|
| 0 | x | x | x | 1-7 | Reserved. Network Computing System (NCS) backward compatibility, and               includes Nil UUID as per [Section 5.9](#niluuid) . | 
| 1 | 0 | x | x | 8-9,A-B | The variant specified in this document. | 
| 1 | 1 | 0 | x | C-D | Reserved. Microsoft Corporation backward compatibility. | 
| 1 | 1 | 1 | x | E-F | Reserved for future definition and includes Max UUID as per [Section 5.10](#maxuuid) . | 

Interoperability, in any form, with variants other than the one
defined here is not guaranteed but is not likely to be an issue in
practice.[¶](#section-4.1-4)

Specifically for UUIDs in this document, bits 64 and 65 of the UUID (bits 0 and 1 of octet 8) MUST be set to 1 and 0 as specified in row 2 of [Table 1](#table1).
Accordingly, all bit and field layouts avoid the use of these bits.[¶](#section-4.1-5)

The version number is in the most significant 4 bits of octet 6
(bits 48 through 51 of the UUID).[¶](#section-4.2-1)

[Table 2](#table2) lists all of the versions for this UUID variant 10xx specified in this document.[¶](#section-4.2-2)

| Table 2 :  UUID Variant 10xx Versions Defined by This Specification |  |  |  |  |  | 
|---|---|---|---|---|---|
| MSB0 | MSB1 | MSB2 | MSB3 | Version | Description | 
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | Unused. | 
| 0 | 0 | 0 | 1 | 1 | The Gregorian time-based UUID specified in this document. | 
| 0 | 0 | 1 | 0 | 2 | Reserved for DCE Security version, with embedded POSIX UUIDs. | 
| 0 | 0 | 1 | 1 | 3 | The name-based version specified in this document that uses MD5 hashing. | 
| 0 | 1 | 0 | 0 | 4 | The randomly or pseudorandomly generated version specified in this document. | 
| 0 | 1 | 0 | 1 | 5 | The name-based version specified in this document that uses SHA-1 hashing. | 
| 0 | 1 | 1 | 0 | 6 | Reordered Gregorian time-based UUID specified in this document. | 
| 0 | 1 | 1 | 1 | 7 | Unix Epoch time-based UUID specified in this document. | 
| 1 | 0 | 0 | 0 | 8 | Reserved for custom UUID formats specified in this document. | 
| 1 | 0 | 0 | 1 | 9 | Reserved for future definition. | 
| 1 | 0 | 1 | 0 | 10 | Reserved for future definition. | 
| 1 | 0 | 1 | 1 | 11 | Reserved for future definition. | 
| 1 | 1 | 0 | 0 | 12 | Reserved for future definition. | 
| 1 | 1 | 0 | 1 | 13 | Reserved for future definition. | 
| 1 | 1 | 1 | 0 | 14 | Reserved for future definition. | 
| 1 | 1 | 1 | 1 | 15 | Reserved for future definition. | 

An example version/variant layout for UUIDv4 follows the table
        where "M" represents the version placement for the hexadecimal
        representation of 0x4 (0b0100) and the "N" represents the variant
        placement for one of the four possible hexadecimal representation of
        variant 10xx: 0x8 (0b1000), 0x9 (0b1001), 0xA (0b1010), 0xB
        (0b1011).[¶](#section-4.2-4)

It should be noted that the other remaining UUID variants found in [Table 1](#table1) leverage different sub-typing or versioning mechanisms.
The recording and definition of the remaining UUID variant and sub-typing combinations are outside of the scope of this document.[¶](#section-4.2-6)

To minimize confusion about bit assignments within octets and among
      differing versions, the UUID record definition is provided as a grouping
      of fields within a bit layout consisting of four octets per row.  The
      fields are presented with the most significant one first.[¶](#section-5-1)

UUIDv1 is a time-based UUID featuring a 60-bit timestamp
        represented by Coordinated Universal Time (UTC) as a count of
        100-nanosecond intervals since 00:00:00.00, 15 October 1582 (the date
        of Gregorian reform to the Christian calendar).[¶](#section-5.1-1)

UUIDv1 also features a clock sequence field that is used to help
        avoid duplicates that could arise when the clock is set backwards in
        time or if the Node ID changes.[¶](#section-5.1-2)

The node field consists of an IEEE 802 MAC address, usually the
        host address or a randomly derived value per Sections [6.9](#unguessability) and [6.10](#unidentifiable).[¶](#section-5.1-3)

For systems that do not have UTC available but do have the local
        time, they may use that instead of UTC as long as they do so
        consistently throughout the system.  However, this is not recommended
        since generating the UTC from local time only needs a time-zone
        offset.[¶](#section-5.1-6)

If the clock is set backwards, or if it might have been set
        backwards (e.g., while the system was powered off), and the UUID
        generator cannot be sure that no UUIDs were generated with timestamps
        larger than the value to which the clock was set, then the clock
        sequence MUST be changed.  If the previous value of the
        clock sequence is known, it MAY be incremented;
        otherwise it SHOULD be set to a random or high-quality
        pseudorandom value.[¶](#section-5.1-7)

Similarly, if the Node ID changes (e.g., because a network card has
been moved between machines), setting the clock sequence to a random
number minimizes the probability of a duplicate due to slight
differences in the clock settings of the machines.  If the value of
the clock sequence associated with the changed Node ID were known, then
the clock sequence MAY be incremented, but that is unlikely.[¶](#section-5.1-8)

The clock sequence MUST be originally (i.e., once in the lifetime of
a system) initialized to a random number to minimize the correlation
across systems.  This provides maximum protection against Node
IDs that may move or switch from system to system rapidly.
The initial value MUST NOT be correlated to the Node ID.[¶](#section-5.1-9)

Notes about nodes derived from IEEE 802:[¶](#section-5.1-10)

UUIDv2 is for DCE Security UUIDs (see [[C309](#C309)] and
        [[C311](#C311)]).  As such, the definition of these UUIDs is
        outside the scope of this specification.[¶](#section-5.2-1)

UUIDv3 is meant for generating UUIDs from names that are
        drawn from, and unique within, some namespace as per [Section 6.5](#name_based_uuid_generation).[¶](#section-5.3-1)

UUIDv3 values are created by computing an MD5 hash [[RFC1321](#RFC1321)] over a given Namespace ID value ([Section 6.6](#namespaces)) concatenated with the desired name value after
        both have been converted to a canonical sequence of octets, as defined
        by the standards or conventions of its namespace, in network byte
        order.  This MD5 value is then used to populate all 128 bits of the
        UUID layout.  The UUID version and variant then replace the respective
        bits as defined by Sections [4.2](#version_field) and  [4.1](#variant_field). An example of this bit substitution can be found
        in [Appendix A.2](#uuidv3_example).[¶](#section-5.3-2)

Information around selecting a desired name's canonical format
        within a given namespace can be found in [Section 6.5](#name_based_uuid_generation) under the heading "A note on names".[¶](#section-5.3-3)

Where possible, UUIDv5 SHOULD be used in lieu of
        UUIDv3.  For more information on MD5 security considerations, see [[RFC6151](#RFC6151)].[¶](#section-5.3-4)

UUIDv4 is meant for generating UUIDs from truly random or
        pseudorandom numbers.[¶](#section-5.4-1)

An implementation may generate 128 bits of random data that is used
        to fill out the UUID fields in [Figure 8](#uuidv4fields). The UUID
        version and variant then replace the respective bits as defined by
        Sections  [4.1](#variant_field) and [4.2](#version_field).[¶](#section-5.4-2)

Alternatively, an implementation MAY choose to
        randomly generate the exact required number of bits for random_a,
        random_b, and random_c (122 bits total) and then concatenate the
        version and variant in the required position.[¶](#section-5.4-3)

For guidelines on random data generation, see [Section 6.9](#unguessability).[¶](#section-5.4-4)

UUIDv5 is meant for generating UUIDs from "names" that are
        drawn from, and unique within, some "namespace" as per [Section 6.5](#name_based_uuid_generation).[¶](#section-5.5-1)

UUIDv5 values are created by computing an SHA-1 hash [[FIPS180-4](#FIPS180-4)] over a given Namespace ID value ([Section 6.6](#namespaces)) concatenated with the desired name value after
        both have been converted to a canonical sequence of octets, as defined
        by the standards or conventions of its namespace, in network byte
        order.  The most significant, leftmost 128 bits of the SHA-1 value
        are then used to populate all 128 bits of the UUID layout, and the
        remaining 32 least significant, rightmost bits of SHA-1 output are
        discarded.  The UUID version and variant then replace the respective
        bits as defined by Sections [4.2](#version_field) and [4.1](#variant_field). An example of this bit substitution and discarding
        excess bits can be found in [Appendix A.4](#uuidv5_example).[¶](#section-5.5-2)

There may be scenarios, usually depending on organizational
        security policies, where SHA-1 libraries may not be available or may
        be deemed unsafe for use.  As such, it may be desirable to generate
        name-based UUIDs derived from SHA-256 or newer SHA methods. These
        name-based UUIDs MUST NOT utilize UUIDv5 and
        MUST be within the UUIDv8 space defined by [Section 5.8](#uuidv8).  An illustrative example of UUIDv8 for SHA-256
        name-based UUIDs is provided in [Appendix B.2](#uuidv8_example_name).[¶](#section-5.5-4)

For more information on SHA-1 security considerations, see [[RFC6194](#RFC6194)].[¶](#section-5.5-5)

UUIDv6 is a field-compatible version of UUIDv1 ([Section 5.1](#uuidv1)), reordered for improved DB locality.  It is expected
        that UUIDv6 will primarily be implemented in contexts where UUIDv1 is used.
        Systems that do not involve legacy UUIDv1 SHOULD use
        UUIDv7 ([Section 5.7](#uuidv7)) instead.[¶](#section-5.6-1)

Instead of splitting the timestamp into the low, mid, and high
        sections from UUIDv1, UUIDv6 changes this sequence so timestamp bytes
        are stored from most to least significant.  That is, given a 60-bit
        timestamp value as specified for UUIDv1 in [Section 5.1](#uuidv1),
        for UUIDv6 the first 48 most significant bits are stored first,
        followed by the 4-bit version (same position), followed by the
        remaining 12 bits of the original 60-bit timestamp.[¶](#section-5.6-2)

The clock sequence and node bits remain unchanged from their
        position in [Section 5.1](#uuidv1).[¶](#section-5.6-3)

The clock sequence and node bits SHOULD be reset to
        a pseudorandom value for each new UUIDv6 generated; however,
        implementations MAY choose to retain the old clock
        sequence and MAC address behavior from [Section 5.1](#uuidv1). For
        more information on MAC address usage within UUIDs, see the [Section 8](#Security).[¶](#section-5.6-4)

The format for the 16-byte, 128-bit UUIDv6 is shown in [Figure 10](#v6layout).[¶](#section-5.6-5)

With UUIDv6, the steps for splitting the timestamp into time_high and time_mid
are OPTIONAL
since the 48 bits of time_high and time_mid will remain in the same order.
An extra step of splitting the first 48 bits of the timestamp into the most
significant
32 bits and least significant 16 bits proves useful when reusing an existing
UUIDv1 implementation.[¶](#section-5.6-8)

UUIDv7 features a time-ordered value field derived from the widely
implemented and well-known Unix Epoch timestamp source, the number of milliseconds
since midnight 1 Jan 1970 UTC, leap seconds excluded.
Generally, UUIDv7 has improved entropy characteristics over UUIDv1 ([Section 5.1](#uuidv1)) or UUIDv6 ([Section 5.6](#uuidv6)).[¶](#section-5.7-1)

UUIDv7 values are created by allocating a Unix timestamp in milliseconds in the most significant 48 bits and filling the remaining 74 bits, excluding the required version and variant bits, with random bits for each new UUIDv7 generated to provide uniqueness as per [Section 6.9](#unguessability). Alternatively, implementations MAY fill the 74 bits, jointly, with a combination of the following subfields, in this order from the most significant bits to the least, to guarantee additional monotonicity within a millisecond:[¶](#section-5.7-2)

Implementations SHOULD utilize UUIDv7 instead of UUIDv1 and UUIDv6 if
possible.[¶](#section-5.7-4)

UUIDv8 provides a format for experimental
        or vendor-specific use cases.  The only requirement is that the
        variant and version bits MUST be set as defined in
        Sections [4.1](#variant_field) and [4.2](#version_field).  UUIDv8's uniqueness will be
        implementation specific and MUST NOT be assumed.[¶](#section-5.8-1)

The only explicitly defined bits are those of the version and
        variant fields, leaving 122 bits for implementation-specific UUIDs. To
        be clear, UUIDv8 is not a replacement for UUIDv4 ([Section 5.4](#uuidv4)) where all 122 extra bits are filled with random
        data.[¶](#section-5.8-2)

Some example situations in which UUIDv8 usage could occur:[¶](#section-5.8-3)

[Appendix B](#ill_examples) provides two illustrative examples of
        custom UUIDv8 algorithms to address two example scenarios.[¶](#section-5.8-5)

The Nil UUID is special form of UUID that is specified to have all
128 bits set to zero.[¶](#section-5.9-1)

A Nil UUID value can be useful to communicate the absence of any
        other UUID value in situations that otherwise require or use a 128-bit
        UUID.  A Nil UUID can express the concept "no such value here". Thus,
        it is reserved for such use as needed for implementation-specific
        situations.[¶](#section-5.9-3)

Note that the Nil UUID value falls within the range of the Apollo
        NCS variant as per the first row of [Table 1](#table1) rather
        than the variant defined by this document.[¶](#section-5.9-4)

The Max UUID is a special form of UUID that is specified to have
        all 128 bits set to 1. This UUID can be thought of as the inverse of
        the Nil UUID defined in [Section 5.9](#niluuid).[¶](#section-5.10-1)

A Max UUID value can be used as a sentinel value in situations
        where a 128-bit UUID is required, but a concept such as "end of UUID
        list" needs to be expressed and is reserved for such use as needed
        for implementation-specific situations.[¶](#section-5.10-3)

Note that the Max UUID value falls within the range of the "yet-to-be defined" future UUID variant as per the last row of [Table 1](#table1) rather than the variant defined by this
        document.[¶](#section-5.10-4)

The minimum requirements for generating UUIDs of each version are described in this
      document.  Everything else is an implementation detail,
      and it is up to the implementer to decide what is appropriate for a
      given implementation. Various relevant factors are covered below to help
      guide an implementer through the different trade-offs among differing
      UUID implementations.[¶](#section-6-1)

UUID timestamp source, precision, and length were topics of great
        debate while creating UUIDv7 for this specification. Choosing the
        right timestamp for your application is very important. This
        section will detail some of the most common points on this issue.[¶](#section-6.1-1)

Monotonicity (each subsequent value being greater than the last) is
        the backbone of time-based sortable UUIDs. Normally, time-based UUIDs
        from this document will be monotonic due to an embedded timestamp;
        however, implementations can guarantee additional monotonicity via the
        concepts covered in this section.[¶](#section-6.2-1)

Take care to ensure UUIDs generated in batches are also
        monotonic. That is, if one thousand UUIDs are generated for the same
        timestamp, there should be sufficient logic for organizing the
        creation order of those one thousand UUIDs.  Batch UUID creation
        implementations MAY utilize a monotonic counter that
        increments for each UUID created during a given timestamp.[¶](#section-6.2-2)

For single-node UUID implementations that do not need to create
        batches of UUIDs, the embedded timestamp within UUIDv6 and UUIDv7
        can provide sufficient monotonicity guarantees by simply ensuring that
        timestamp increments before creating a new UUID. Distributed nodes are
        discussed in [Section 6.4](#distributed_shared_knowledge).[¶](#section-6.2-3)

Implementations SHOULD employ the following methods
        for single-node UUID implementations that require batch UUID creation
        or are otherwise concerned about monotonicity with high-frequency UUID
        generation.[¶](#section-6.2-4)

For UUIDv7, which has millisecond timestamp precision, it is
          possible to use additional clock precision available on the system
          to substitute for up to 12 random bits immediately following the
          timestamp.  This can provide values that are time ordered with
          sub-millisecond precision, using however many bits are appropriate
          in the implementation environment.  With this method, the additional
          time precision bits MUST follow the timestamp as the
          next available bit in the rand_a field for UUIDv7.[¶](#section-6.2-5.6.1)

To calculate this value, start with the portion of the timestamp
          expressed as a fraction of the clock's tick value (fraction of a
          millisecond for UUIDv7).  Compute the count of possible values that
          can be represented in the available bit space, 4096 for the UUIDv7
          rand_a field.  Using floating point or scaled integer arithmetic,
          multiply this fraction of a millisecond value by 4096 and round down
          (toward zero) to an integer result to arrive at a number between 0
          and the maximum allowed for the indicated bits, which sorts
          monotonically based on time. Each increasing fractional value will
          result in an increasing bit field value to the precision available
          with these bits.[¶](#section-6.2-5.6.2)

For example, let's assume a system timestamp of 1 Jan 2023
          12:34:56.1234567.  Taking the precision greater than 1 ms gives us a
          value of 0.4567, as a fraction of a millisecond.  If we wish to
          encode this as 12 bits, we can take the count of possible values
          that fit in those bits (4096 or 2<sup>12</sup>), multiply it by our
          millisecond fraction value of 0.4567, and truncate the result to an
          integer, which gives an integer value of 1870. Expressed as
          hexadecimal, it is 0x74E or the binary bits 0b011101001110.  One can
          then use those 12 bits as the most significant (leftmost) portion of
          the random section of the UUID (e.g., the rand_a field in UUIDv7).
          This works for any desired bit length that fits into a UUID, and
          applications can decide the appropriate length based on available
          clock precision; for UUIDv7, it is limited to 12 bits at maximum to
          reserve sufficient space for random bits.[¶](#section-6.2-5.6.3)

The main benefit to encoding additional timestamp precision is
          that it utilizes additional time precision already available in the
          system clock to provide values that are more likely to be unique; thus, it may simplify certain implementations. This technique can
          also be used in conjunction with one of the other methods, where
          this additional time precision would immediately follow the
          timestamp. Then, if any bits are to be used as a clock sequence,
          they would follow next.[¶](#section-6.2-5.6.4)

The following sub-topics cover issues related solely to creating reliable
fixed bit-length dedicated counters:[¶](#section-6.2-6)

The following sub-topics cover rollover handling with either type of counter
method:[¶](#section-6.2-8)

Implementations MAY use the following logic to
        ensure UUIDs featuring embedded counters are monotonic in nature:[¶](#section-6.2-10)

The (optional) UUID generator state only needs to be read from
        stable storage once at boot time, if it is read into a system-wide
        shared volatile store (and updated whenever the stable store is
        updated).[¶](#section-6.3-1)

This stable storage MAY be used to record various
        portions of the UUID generation, which prove useful for batch UUID
        generation purposes and monotonic error checking with UUIDv6 and
        UUIDv7.  These stored values include but are not limited to last known
        timestamp, clock sequence, counters, and random data.[¶](#section-6.3-2)

If an implementation does not have any stable store available, then
        it MAY proceed with UUID generation as if this were the
        first UUID created within a batch.  This is the least desirable
        implementation because it will increase the frequency of creation of
        values such as clock sequence, counters, or random data, which
        increases the probability of duplicates. Further, frequent generation
        of random numbers also puts more stress on any entropy source and/or
        entropy pool being used as the basis for such random numbers.[¶](#section-6.3-3)

An implementation MAY also return an application
        error in the event that collision resistance is of the utmost concern.
        The semantics of this error are up to the application and
        implementation.  See [Section 6.7](#collision_resistance) for more
        information on weighting collision tolerance in applications.[¶](#section-6.3-4)

For UUIDv1 and UUIDv6, if the Node ID can never change (e.g., the
        network interface card from which the Node ID is derived is
        inseparable from the system), or if any change also re-initializes the
        clock sequence to a random value, then instead of keeping it in stable
        store, the current Node ID may be returned.[¶](#section-6.3-5)

For UUIDv1 and UUIDv6, the state does not always need to be written
        to stable store every time a UUID is generated.  The timestamp in the
        stable store can periodically be set to a value larger than any yet
        used in a UUID.  As long as the generated UUIDs have timestamps less
        than that value, and the clock sequence and Node ID remain unchanged,
        only the shared volatile copy of the state needs to be updated.
        Furthermore, if the timestamp value in stable store is in the future
        by less than the typical time it takes the system to reboot, a crash
        will not cause a re-initialization of the clock sequence.[¶](#section-6.3-6)

If it is too expensive to access shared state each time a UUID is
        generated, then the system-wide generator can be implemented to
        allocate a block of timestamps each time it is called; a per-process
        generator can allocate from that block until it is exhausted.[¶](#section-6.3-7)

Although some prefer to use the word "hash-based" to describe UUIDs
 featuring hashing algorithms (MD5 or SHA-1), this document retains the
 usage of the term "name-based" in order to maintain consistency with
 previously published documents and existing implementations.[¶](#section-6.5-1)

The requirements for name-based UUIDs are as follows:[¶](#section-6.5-2)

A note on names:[¶](#section-6.5-4)

The concept of name (and namespace) should be broadly
          construed and not limited to textual names. A canonical sequence of
          octets is one that conforms to the specification for that name
          form's canonical representation. A name can have many usual forms,
          only one of which can be canonical. An implementer of new namespaces
          for UUIDs needs to reference the specification for the canonical
          form of names in that space or define such a canonical form for the
          namespace if it does not exist.  For example, at the time of
          writing, Domain Name System (DNS) [[RFC9499](#RFC9499)] has three
          conveyance formats: common (www.example.com), presentation
          (www.example.com.), and wire format (3www7example3com0).  Looking at
          [[X500](#X500)] Distinguished Names (DNs), [[RFC4122](#RFC4122)] allowed either text-based or
          binary DER-based names as inputs.  For Uniform Resource Locators
          (URLs) [[RFC1738](#RFC1738)], one could provide a Fully Qualified
          Domain Name (FQDN) with or without the protocol identifier
          www.example.com or https://www.example.com.  When it comes to Object
          Identifiers (OIDs) [[X660](#X660)], one could choose dot
          notation without the leading dot (2.999), choose to include the
          leading dot (.2.999), or select one of the many formats from [[X680](#X680)] such as OID Internationalized Resource Identifier
          (OID-IRI) (/Joint-ISO-ITU-T/Example).  While most users may default
          to the common format for DNS, FQDN format for a URL, text format for
          X.500, and dot notation without a leading dot for OID, name-based
          UUID implementations generally SHOULD allow arbitrary
          input that will compute name-based UUIDs for any of the
          aforementioned example names and others not defined here.  Each name
          format within a namespace will output different UUIDs.  As such, the
          mechanisms or conventions used for allocating names and ensuring
          their uniqueness within their namespaces are beyond the scope of
          this specification.[¶](#section-6.5-5)

This section details the namespace
        IDs for some potentially interesting namespaces such as those for DNS
        [[RFC9499](#RFC9499)], URLs [[RFC1738](#RFC1738)], OIDs [[X660](#X660)], and DNs [[X500](#X500)].[¶](#section-6.6-1)

Further, this section also details allocation, IANA registration,
        and other details pertinent to Namespace IDs.[¶](#section-6.6-2)

| Table 3 :  Namespace IDs |  |  |  | 
|---|---|---|---|
| Namespace | Namespace ID Value | Name Reference | Namespace ID Reference | 
|---|---|---|---|
| DNS | 6ba7b810-9dad-11d1-80b4-00c04fd430c8 | [ [RFC9499](#RFC9499) ] | [ [RFC4122](#RFC4122) ], RFC 9562 | 
| URL | 6ba7b811-9dad-11d1-80b4-00c04fd430c8 | [ [RFC1738](#RFC1738) ] | [ [RFC4122](#RFC4122) ], RFC 9562 | 
| OID | 6ba7b812-9dad-11d1-80b4-00c04fd430c8 | [ [X660](#X660) ] | [ [RFC4122](#RFC4122) ], RFC 9562 | 
| X500 | 6ba7b814-9dad-11d1-80b4-00c04fd430c8 | [ [X500](#X500) ] | [ [RFC4122](#RFC4122) ], RFC 9562 | 

Items may be added to this registry using the Specification Required
        policy as per [[RFC8126](#RFC8126)].[¶](#section-6.6-4)

For designated experts, generally speaking, Namespace IDs are
        allocated as follows:[¶](#section-6.6-5)

Note that the Namespace ID value
        "6ba7b813-9dad-11d1-80b4-00c04fd430c8" and its usage are not defined by
        this document or by [[RFC4122](#RFC4122)]; thus, it SHOULD NOT be used as a Namespace ID value.[¶](#section-6.6-7)

New Namespace ID values MUST be documented as per
        [Section 7](#IANA) if they are to be globally available and fully
        interoperable.  Implementations MAY continue to use
        vendor-specific, application-specific, and deployment-specific
        Namespace ID values; but know that interoperability is not guaranteed.
        These custom Namespace ID values MUST NOT use the logic
        above; instead, generating a
        UUIDv4 or UUIDv7 Namespace ID value is RECOMMENDED.  If collision probability ([Section 6.7](#collision_resistance)) and uniqueness ([Section 6.8](#global_local_uniqueness)) of the final name-based UUID are
        not a problem, an implementation MAY also leverage
        UUIDv8 instead to create a custom, application-specific Namespace ID
        value.[¶](#section-6.6-8)

Implementations SHOULD provide the ability to input
        a custom namespace to account for newly registered IANA Namespace ID
        values outside of those listed in this section or custom,
        application-specific Namespace ID values.[¶](#section-6.6-9)

Implementations should weigh the consequences of UUID collisions
        within their application and when deciding between UUID versions that
        use entropy (randomness) versus the other components such as those in
        Sections [6.1](#timestamp_considerations)
        and [6.2](#monotonicity_counters).  This is
        especially true for distributed node collision resistance as defined
        by [Section 6.4](#distributed_shared_knowledge).[¶](#section-6.7-1)

There are two example scenarios below that help illustrate the
        varying seriousness of a collision within an application.[¶](#section-6.7-2)

UUIDs created by this specification MAY be used to
        provide local uniqueness guarantees.  For example, ensuring UUIDs
        created within a local application context are unique within a
        database MAY be sufficient for some implementations
        where global uniqueness outside of the application context, in other
        applications, or around the world is not required.[¶](#section-6.8-1)

Although true global uniqueness is impossible to guarantee without
        a shared knowledge scheme, a shared knowledge scheme is not required
        by a UUID to provide uniqueness for practical implementation purposes.
        Implementations MAY use a shared knowledge
        scheme, introduced in [Section 6.4](#distributed_shared_knowledge),
        as they see fit to extend the uniqueness guaranteed by this
        specification.[¶](#section-6.8-2)

Implementations SHOULD utilize a cryptographically
        secure pseudorandom number generator (CSPRNG) to provide values that
        are both difficult to predict ("unguessable") and have a low
        likelihood of collision ("unique").  The exception is when a suitable
        CSPRNG is unavailable in the execution environment.  Take care to
        ensure the CSPRNG state is properly reseeded upon state changes, such
        as process forks, to ensure proper CSPRNG operation.  CSPRNG ensures
        the best of Sections [6.7](#collision_resistance) and [8](#Security) are
        present in modern UUIDs.[¶](#section-6.9-1)

Further advice on generating cryptographic-quality random numbers
        can be found in [[RFC4086](#RFC4086)], [[RFC8937](#RFC8937)],
        and [[RANDOM](#RANDOM)].[¶](#section-6.9-2)

This section describes how to generate a UUIDv1 or UUIDv6 value if
        an IEEE 802 address is not available or its use is not desired.[¶](#section-6.10-1)

Implementations MAY leverage MAC address
        randomization techniques [[IEEE802.11bh](#IEEE802.11bh)] as an alternative to the pseudorandom logic
        provided in this section.[¶](#section-6.10-2)

Alternatively, implementations MAY elect to obtain a
        48-bit cryptographic-quality random number as per [Section 6.9](#unguessability) to use as the Node ID.  After generating the
        48-bit fully randomized node value, implementations
        MUST set the least significant bit of the first octet
        of the Node ID to 1.  This bit is the unicast or multicast bit, which
        will never be set in IEEE 802 addresses obtained from network cards.
        Hence, there can never be a conflict between UUIDs generated by
        machines with and without network cards.  An example of generating a
        randomized 48-bit node value and the subsequent bit modification is
        detailed in [Appendix A](#test_vectors).  For more information about
        IEEE 802 address and the unicast or multicast or local/global bits,
        please review [[RFC9542](#RFC9542)].[¶](#section-6.10-3)

For compatibility with earlier specifications, note that this
        document uses the unicast or multicast bit instead of the arguably more
        correct local/global bit because MAC addresses with the local/global
        bit set or not set are both possible in a network.  This is not the case
        with the unicast or multicast bit.  One node cannot have a MAC address
        that multicasts to multiple nodes.[¶](#section-6.10-4)

In addition, items such as the computer's name and the name of the
        operating system, while not strictly speaking random, will help
        differentiate the results from those obtained by other systems.[¶](#section-6.10-5)

The exact algorithm to generate a Node ID using these data is
        system specific because both the data available and the functions to
        obtain them are often very system specific.  However, a generic approach
        is to accumulate as many sources as possible into a buffer, use a
        message digest (such as SHA-256 or SHA-512 defined by [[FIPS180-4](#FIPS180-4)]), take an arbitrary 6 bytes from the hash value,
        and set the multicast bit as described above.[¶](#section-6.10-6)

UUIDv6 and UUIDv7 are designed so that implementations that require
        sorting (e.g., database indexes) sort as opaque raw bytes without the
        need for parsing or introspection.[¶](#section-6.11-1)

Time-ordered monotonic UUIDs benefit from greater database-index
        locality because the new values are near each other in the index.  As
        a result, objects are more easily clustered together for better
        performance.  The real-world differences in this approach of index
        locality versus random data inserts can be one order of magnitude or
        more.[¶](#section-6.11-2)

UUID formats created by this specification are intended to be
        lexicographically sortable while in the textual representation.[¶](#section-6.11-3)

UUIDs created by this specification are crafted with big-endian
        byte order (network byte order) in mind. If little-endian style is
        required, UUIDv8 is available for custom UUID formats.[¶](#section-6.11-4)

As general guidance, avoiding parsing UUID values
        unnecessarily is recommended; instead, treat UUIDs as opaquely as possible.
        Although application-specific concerns could, of course, require some
        degree of introspection (e.g., to examine Sections [4.1](#variant_field) or [4.2](#version_field) or perhaps the timestamp of
        a UUID), the advice here is to avoid this or other parsing unless
        absolutely necessary.  Applications typically tend to be simpler, be more
        interoperable, and perform better when this advice is followed.[¶](#section-6.12-1)

For many applications, such as databases, storing UUIDs as text is
        unnecessarily verbose, requiring 288 bits to represent 128-bit UUID
        values.  Thus, where feasible, UUIDs SHOULD be stored
        within database applications as the underlying 128-bit binary
        value.[¶](#section-6.13-1)

For other systems, UUIDs MAY be stored in binary
        form or as text, as appropriate.  The trade-offs to both approaches
        are as follows:[¶](#section-6.13-2)

DBMS vendors are encouraged to provide functionality to generate
        and store UUID formats defined by this specification for use as
        identifiers or left parts of identifiers such as, but not limited to,
        primary keys, surrogate keys for temporal databases, foreign keys
        included in polymorphic relationships, and keys for key-value pairs in
        JSON columns and key-value databases.  Applications using a monolithic
        database may find using database-generated UUIDs (as opposed to
        client-generated UUIDs) provides the best UUID monotonicity.  In
        addition to UUIDs, additional identifiers MAY be used
        to ensure integrity and feedback.[¶](#section-6.13-4)

Designers of database schema are cautioned against using name-based
        UUIDs (see Sections [5.3](#uuidv3) and [5.5](#uuidv5)) as primary keys in tables.  A
        common issue observed in database schema design is the assumption that
        a particular value will never change, which later turns out to be
        an incorrect assumption.  Postal codes, license or other
        identification numbers, and numerous other such identifiers seem
        unique and unchanging at a given point time -- only later to have edge
        cases where they need to change.  The subsequent change of the
        identifier, used as a "name" input for name-based UUIDs, can
        invalidate a given database structure.  In such scenarios, it is
        observed that using any non-name-based UUID version would have
        resulted in the field in question being placed somewhere that would
        have been easier to adapt to such changes (primary key excluded from
        this statement).  The general advice is to avoid name-based UUID
        natural keys and, instead, to utilize time-based UUID surrogate keys
        based on the aforementioned problems detailed in this section.[¶](#section-6.13-5)

All references to [[RFC4122](#RFC4122)] in IANA registries
      (outside of those created by this document) have been replaced with
      references to this document, including the IANA URN namespace
      registration [[URNNamespaces](#URNNamespaces)] for UUID.  References to
      [Section 4.1.2](https://rfc-editor.org/rfc/rfc4122#section-4.1.2) of [[RFC4122](#RFC4122)] have been
      updated to refer to [Section 4](#format) of this document.[¶](#section-7-1)

Finally, IANA should track UUID Subtypes and Special Case "Namespace
      IDs Values" as specified in Sections [7.1](#iana2) and [7.2](#iana3) at the
      following location: <[https://www.iana.org/assignments/uuid](https://www.iana.org/assignments/uuid)>.[¶](#section-7-2)

When evaluating requests, the designated expert should consider
      community feedback, how well-defined the reference specification is, and
      this specification's requirements.  Vendor-specific,
      application-specific, and deployment-specific values are unable to be
      registered.  Specification documents should be published in a stable,
      freely available manner (ideally, located with a URL) but need not be
      standards.  The designated expert will either approve or deny the
      registration request and communicate this decision to IANA. Denials
      should include an explanation and, if applicable, suggestions as to how
      to make the request successful.[¶](#section-7-3)

This specification defines the "UUID Subtypes" registry for common
        widely used UUID standards.[¶](#section-7.1-1)

| Table 4 :  IANA UUID Subtypes |  |  |  |  | 
|---|---|---|---|---|
| Name | ID | Subtype | Variant | Reference | 
|---|---|---|---|---|
| Gregorian Time-based | 1 | version | OSF DCE / IETF | [ [RFC4122](#RFC4122) ], RFC 9562 | 
| DCE Security | 2 | version | OSF DCE / IETF | [ [C309](#C309) ], [[C311](#C311) ] | 
| MD5 Name-based | 3 | version | OSF DCE / IETF | [ [RFC4122](#RFC4122) ], RFC 9562 | 
| Random | 4 | version | OSF DCE / IETF | [ [RFC4122](#RFC4122) ], RFC 9562 | 
| SHA-1 Name-based | 5 | version | OSF DCE / IETF | [ [RFC4122](#RFC4122) ], RFC 9562 | 
| Reordered Gregorian Time-based | 6 | version | OSF DCE / IETF | RFC 9562 | 
| Unix Time-based | 7 | version | OSF DCE / IETF | RFC 9562 | 
| Custom | 8 | version | OSF DCE / IETF | RFC 9562 | 

This table may be extended by Standards Action as per
        [[RFC8126](#RFC8126)].[¶](#section-7.1-3)

For designated experts:[¶](#section-7.1-4)

This specification defines the "UUID Namespace IDs" registry for common, widely used Namespace ID values.[¶](#section-7.2-1)

The full details of this registration, including information for designated experts, can be found in [Section 6.6](#namespaces).[¶](#section-7.2-2)

Implementations SHOULD NOT assume that UUIDs are hard
      to guess.  For example, they MUST NOT be used as security
      capabilities (identifiers whose mere possession grants access).
      Discovery of predictability in a random number source will result in a
      vulnerability.[¶](#section-8-1)

Implementations MUST NOT assume that it is easy to
      determine if a UUID has been slightly modified in order to redirect a
      reference to another object.  Humans do not have the ability to easily
      check the integrity of a UUID by simply glancing at it.[¶](#section-8-2)

MAC addresses pose inherent security risks around privacy and
      SHOULD NOT be used within a UUID.  Instead CSPRNG data
      SHOULD be selected from a source with sufficient entropy
      to ensure guaranteed uniqueness among UUID generation. See Sections
      [6.9](#unguessability) and [6.10](#unidentifiable) for more information.[¶](#section-8-3)

Timestamps embedded in the UUID do pose a very small attack
      surface. The timestamp in conjunction with an embedded counter does
      signal the order of creation for a given UUID and its corresponding data
      but does not define anything about the data itself or the application as
      a whole.  If UUIDs are required for use with any security operation
      within an application context in any shape or form, then UUIDv4 ([Section 5.4](#uuidv4)) SHOULD be utilized.[¶](#section-8-4)

See [[RFC6151](#RFC6151)] for MD5 security considerations and
      [[RFC6194](#RFC6194)] for SHA-1 security considerations.[¶](#section-8-5)

Both UUIDv1 and UUIDv6 test vectors utilize the same 60-bit
      timestamp: 0x1EC9414C232AB00 (138648505420000000) Tuesday, February 22,
      2022 2:22:22.000000 PM GMT-05:00.[¶](#appendix-A-1)

Both UUIDv1 and UUIDv6 utilize the same values in clock_seq and
      node; all of which have been generated with random data.  For the
      randomized node, the least significant bit of the first octet is set to
      a value of 1 as per [Section 6.10](#unidentifiable).  Thus, the starting
      value 0x9E6BDECED846 was changed to 0x9F6BDECED846.[¶](#appendix-A-2)

The pseudocode used for converting from a 64-bit Unix timestamp to a
      100 ns Gregorian timestamp value has been left in the document for
      reference purposes.[¶](#appendix-A-3)

The MD5 computation from is detailed in [Figure 17](#v3md5)
        using the DNS Namespace ID value and the Name "www.example.com".
        The field mapping and all values are illustrated in [Figure 18](#v3fields).  Finally, to further illustrate the bit swapping
        for version and variant, see [Figure 19](#v3vervar).[¶](#appendix-A.2-1)

This UUIDv4 example was created by generating 16 bytes of random
        data resulting in the hexadecimal value of
        919108F752D133205BACF847DB4148A8. This is then used to fill out the
        fields as shown in [Figure 20](#v4fields).[¶](#appendix-A.3-1)

Finally, to further illustrate the bit swapping for version and
        variant, see [Figure 21](#v4vervar).[¶](#appendix-A.3-2)

The SHA-1 computation form is detailed in [Figure 22](#v5sha1),
        using the DNS Namespace ID value and the Name "www.example.com".  The
        field mapping and all values are illustrated in [Figure 23](#v5fields).  Finally, to further illustrate the bit swapping
        for version and variant and the unused/discarded part of the SHA-1
        value, see [Figure 24](#v5vervar).[¶](#appendix-A.4-1)

This example UUIDv7 test vector utilizes a well-known Unix Epoch
        timestamp with millisecond precision to fill the first 48 bits.[¶](#appendix-A.6-1)

rand_a and rand_b are filled with random data.[¶](#appendix-A.6-2)

The timestamp is Tuesday, February 22, 2022 2:22:22.00 PM
        GMT-05:00, represented as 0x017F22E279B0 or 1645557742000.[¶](#appendix-A.6-3)

The following sections contain illustrative examples that serve to
      show how one may use UUIDv8 ([Section 5.8](#uuidv8)) for custom and/or
      experimental application-based logic.  The examples below have not been
      through the same rigorous testing, prototyping, and feedback loop that
      other algorithms in this document have undergone.  The authors
      encourage implementers to create their own UUIDv8 algorithm rather than
      use the items defined in this section.[¶](#appendix-B-1)

This example UUIDv8 test vector utilizes a well-known 64-bit Unix
        Epoch timestamp with 10 ns precision, truncated to the
        least significant, rightmost bits to fill the first 60 bits of
        custom_a and custom_b, while setting the version bits between these two
        segments to the version value of 8.[¶](#appendix-B.1-1)

The variant bits are set; and the final segment, custom_c, is filled
        with random data.[¶](#appendix-B.1-2)

Timestamp is Tuesday, February 22, 2022 2:22:22.000000 PM
        GMT-05:00, represented as 0x2489E9AD2EE2E00 or 164555774200000000
        (10 ns-steps).[¶](#appendix-B.1-3)

As per [Section 5.5](#uuidv5), name-based UUIDs that want to use
        modern hashing algorithms MUST be created within the
        UUIDv8 space. These MAY leverage newer hashing
        algorithms such as SHA-256 or SHA-512 (as defined by [[FIPS180-4](#FIPS180-4)]), SHA-3 or SHAKE (as defined by [[FIPS202](#FIPS202)]), or even algorithms that have not been defined
        yet.[¶](#appendix-B.2-1)

A SHA-256 version of the SHA-1 computation in [Appendix A.4](#uuidv5_example) is detailed in [Figure 28](#v8sha256) as
        an illustrative example detailing how this can be achieved.  The
        creation of the name-based UUIDv8 value in this section follows the
        same logic defined in [Section 5.5](#uuidv5) with the difference
        being SHA-256 in place of SHA-1.[¶](#appendix-B.2-2)

The field mapping and all values are illustrated in [Figure 29](#v8fieldssha256).  Finally, to further illustrate the bit
        swapping for version and variant and the unused/discarded part of the
        SHA-256 value, see [Figure 30](#v8vervar).  An important note for
        secure hashing algorithms that produce outputs of an arbitrary size,
        such as those found in SHAKE, is that the output hash
        MUST be 128 bits or larger.[¶](#appendix-B.2-3)

The authors gratefully acknowledge the contributions of Rich Salz, Michael Mealling, Ben Campbell, Ben Ramsey, Fabio Lima, Gonzalo Salgueiro,
      Martin Thomson, Murray       S. Kucherawy, Rick van Rein, Rob Wilton, Sean Leonard, Theodore Y. Ts'o, Robert Kieffer,
      Sergey Prokhorenko, and LiosK.[¶](#appendix-C-1)

As well as all of those in the IETF community and on GitHub to who
      contributed to the discussions that resulted in this document.[¶](#appendix-C-2)

This document draws heavily on the OSF DCE specification (Appendix A
      of [[C309](#C309)]) for UUIDs.  Ted Ts'o provided helpful comments.[¶](#appendix-C-3)

We are also grateful to the careful reading and bit-twiddling of
      Ralf S. Engelschall, John       Larmouth, and Paul Thorpe.  Professor Larmouth was also invaluable in achieving
      coordination with ISO/IEC.[¶](#appendix-C-4)
