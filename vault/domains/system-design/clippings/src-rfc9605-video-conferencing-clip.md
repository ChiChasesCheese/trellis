---
title: 'RFC 9605: Secure Frame (SFrame): Lightweight Authenticated Encryption for
  Real-Time Media | RFC Editor'
source: https://www.rfc-editor.org/rfc/rfc9605
author: E Omara; J Uberti; S G Murillo; R Barnes; Y Fablet
published: '2024-08-27'
site: rfc-editor.org
clipped: '2026-09-20'
---

# RFC 9605: Secure Frame (SFrame): Lightweight Authenticated Encryption for Real-Time Media | RFC Editor

- [Home](/)
- **RFC 9605**

# RFC 9605:      Secure Frame (SFrame): Lightweight Authenticated Encryption for Real-Time Media 

- E. Omara,
- J. Uberti,
- S. G. Murillo,
- R. Barnes, Ed.,
- Y. Fablet

## [Abstract](#abstract)

This document describes the Secure Frame (SFrame) end-to-end encryption and
authentication mechanism for media frames in a multiparty conference call, in
which central media servers (Selective Forwarding Units or SFUs) can access the
media metadata needed to make forwarding decisions without having access to the
actual media.[¶](#section-abstract-1)

This mechanism differs from the Secure Real-Time Protocol (SRTP) in that
it is independent of RTP (thus compatible with non-RTP media transport) and can
be applied to whole media frames in order to be more bandwidth efficient.[¶](#section-abstract-2)

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
            [https://](/info/rfc9605).[¶](#section-boilerplate.1-3)

## 
[Copyright Notice](#name-copyright-notice)
        

            Copyright (c) 2024 IETF Trust and the persons identified as the
            document authors. All rights reserved.[¶](#section-boilerplate.2-1)

            This document is subject to BCP 78 and the IETF Trust's Legal
            Provisions Relating to IETF Documents
            ([https://](https://trustee.ietf.org/license-info)) in effect on the date of
            publication of this document. Please review these documents
            carefully, as they describe your rights and restrictions with
            respect to this document. Code Components extracted from this
            document must include Revised BSD License text as described in
            Section 4.e of the Trust Legal Provisions and are provided without
            warranty as described in the Revised BSD License.[¶](#section-boilerplate.2-2)

## 
[1.](#section-1) [Introduction](#name-introduction)
      

Modern multiparty video call systems use Selective Forwarding Unit (SFU)
servers to efficiently route media streams to call endpoints based on factors such
as available bandwidth, desired video size, codec support, and other factors. An
SFU typically does not need access to the media content of the conference,
which allows the media to be encrypted "end to end" so that it cannot be
decrypted by the SFU. In order for the SFU to work properly, though, it usually
needs to be able to access RTP metadata and RTCP feedback messages, which is not
possible if all RTP/RTCP traffic is end-to-end encrypted.[¶](#section-1-1)

As such, two layers of encryption and authentication are required:[¶](#section-1-2)

1. 
          Hop-by-hop (HBH) encryption of media, metadata, and feedback messages between the endpoints and SFU [¶](#section-1-3.1.1)
2. 
          End-to-end (E2E) encryption (E2EE) of media between the endpoints [¶](#section-1-3.2.1)

The Secure Real-Time Protocol (SRTP) is already widely used for HBH encryption
[[RFC3711](#RFC3711)]. The SRTP "double encryption" scheme defines a way to do E2E
encryption in SRTP [[RFC8723](#RFC8723)]. Unfortunately, this scheme has poor efficiency
and high complexity, and its entanglement with RTP makes it unworkable in
several realistic SFU scenarios.[¶](#section-1-4)

This document proposes a new E2EE protection scheme known as SFrame,
specifically designed to work in group conference calls with SFUs. SFrame is a
general encryption framing that can be used to protect media payloads, agnostic
of transport.[¶](#section-1-5)

## 
[2.](#section-2) [Terminology](#name-terminology)
      

The key words "MUST", "MUST NOT",
        "REQUIRED", "SHALL", "SHALL NOT",
        "SHOULD", "SHOULD NOT",
        "RECOMMENDED", "NOT RECOMMENDED",
        "MAY", and "OPTIONAL" in this document are to be
        interpreted as described in BCP 14 [[RFC2119](#RFC2119)] [[RFC8174](#RFC8174)] when, and only when, they appear in all capitals, as
        shown here.[¶](#section-2-1)

We use "Selective Forwarding Unit (SFU)" and "media stream" in a less formal sense
than in [[RFC7656](#RFC7656)].  An SFU is a selective switching function for media
payloads, and a media stream is a sequence of media payloads,
regardless of whether those media payloads are transported over RTP or some
other protocol.[¶](#section-2-3)

## 
[3.](#section-3) [Goals](#name-goals)
      

SFrame is designed to be a suitable E2EE protection scheme for conference call
media in a broad range of scenarios, as outlined by the following goals:[¶](#section-3-1)

1. 
          Provide a secure E2EE mechanism for audio and video in conference calls that can be used with arbitrary SFU servers. [¶](#section-3-2.1.1)
2. 
          Decouple media encryption from key management to allow SFrame to be used with an arbitrary key management system. [¶](#section-3-2.2.1)
3. 
          Minimize packet expansion to allow successful conferencing in as many network conditions as possible. [¶](#section-3-2.3.1)
4. 
          Decouple the media encryption framework from the underlying transport, allowing use in non-RTP scenarios, e.g., WebTransport [ [WEBTRANSPORT](#I-D.ietf-webtrans-overview) ].[¶](#section-3-2.4.1)
5. 
          When used with RTP and its associated error- resilience mechanisms, i.e., RTX and Forward Error Correction (FEC), require no special handling for RTX and FEC packets. [¶](#section-3-2.5.1)
6. 
          Minimize the changes needed in SFU servers. [¶](#section-3-2.6.1)
7. 
          Minimize the changes needed in endpoints. [¶](#section-3-2.7.1)
8. 
          Work with the most popular audio and video codecs used in conferencing scenarios. [¶](#section-3-2.8.1)

## 
[4.](#section-4) [SFrame](#name-sframe)
      

This document defines an encryption mechanism that provides effective E2EE,
is simple to implement, has no dependencies on RTP, and minimizes
encryption bandwidth overhead. This section describes how the mechanism
works and includes details of how applications utilize SFrame for media protection
as well as the actual mechanics of E2EE for protecting media.[¶](#section-4-1)

### 
[4.1.](#section-4.1) [Application Context](#name-application-context)
        

SFrame is a general encryption framing, intended to be used as an E2EE
layer over an underlying HBH-encrypted transport such as SRTP or QUIC
[[RFC3711](#RFC3711)][[MOQ-TRANSPORT](#I-D.ietf-moq-transport)].[¶](#section-4.1-1)

The scale at which SFrame encryption is applied to media determines the overall
amount of overhead that SFrame adds to the media stream as well as the
engineering complexity involved in integrating SFrame into a particular
environment. Two patterns are common: using SFrame to encrypt either whole
media frames (per frame) or individual transport-[¶](#section-4.1-2)

For example, [Figure 1](#media-stack) shows a typical media sender stack that takes media
from some source, encodes it into frames, divides those frames into media
packets, and then sends those payloads in SRTP packets. The receiver stack
performs the reverse operations, reassembling frames from SRTP packets and
decoding.  Arrows indicate two different ways that SFrame protection could be
integrated into this media stack: to encrypt whole frames or individual media
packets.[¶](#section-4.1-3)

Applying SFrame per frame in this system offers higher efficiency but may
require a more complex integration in environments where depacketization relies
on the content of media packets. Applying SFrame per packet avoids this
complexity at the cost of higher bandwidth consumption.  Some quantitative
discussion of these trade-offs is provided in [Appendix B](#overhead-analysis).[¶](#section-4.1-4)

As noted above, however, SFrame is a general media encapsulation and can be
applied in other scenarios.  The important thing is that the sender and
receivers of an SFrame-[¶](#section-4.1-5)

Like SRTP, SFrame does not define how the keys used for SFrame are exchanged by
the parties in the conference.  Keys for SFrame might be distributed over an
existing E2E-secure channel (see [Section 5.1](#sender-keys)) or derived from an E2E-secure
shared secret (see [Section 5.2](#mls)).  The key management system MUST ensure that each
key used for encrypting media is used by exactly one media sender in order to
avoid reuse of nonces.[¶](#section-4.1-7)

### 
[4.2.](#section-4.2) [SFrame Ciphertext](#name-sframe-ciphertext)
        

An SFrame ciphertext comprises an SFrame header followed by the output of an
Authenticated Encryption with Associated Data (AEAD) encryption of the plaintext [[RFC5116](#RFC5116)], with the header provided as additional
authenticated data (AAD).[¶](#section-4.2-1)

The SFrame header is a variable-[Section 4.3](#sframe-header).  The structure of the encrypted data and authentication tag
are determined by the AEAD algorithm in use.[¶](#section-4.2-2)

When SFrame is applied per packet, the payload of each packet will be an SFrame
ciphertext.  When SFrame is applied per frame, the SFrame ciphertext
representing an encrypted frame will span several packets, with the header
appearing in the first packet and the authentication tag in the last packet.
It is the responsibility of the application to reassemble an encrypted frame from
individual packets, accounting for packet loss and reordering as necessary.[¶](#section-4.2-4)

### 
[4.3.](#section-4.3) [SFrame Header](#name-sframe-header)
        

The SFrame header specifies two values from which encryption parameters are
derived:[¶](#section-4.3-1)

- 
            A Key ID (KID) that determines which encryption key should be used [¶](#section-4.3-2.1.1)
- 
            A Counter (CTR) that is used to construct the nonce for the encryption [¶](#section-4.3-2.2.1)

Applications MUST ensure that each (KID, CTR) combination is used for exactly
one SFrame encryption operation. A typical approach to achieve this guarantee is
outlined in [Section 9.1](#header-value-uniqueness).[¶](#section-4.3-3)

The SFrame header has the overall structure shown in [Figure 3](#fig-sframe-header).  The
first byte is a "config byte", with the following fields:[¶](#section-4.3-5)

- Extended KID Flag (X, 1 bit):
- 
            Indicates if the K field contains the KID or the KID length. [¶](#section-4.3-6.2.1)
- KID or KID Length (K, 3 bits):
- 
            If the X flag is set to 0, this field contains the KID. If the X flag is set to 1, then it contains the length of the KID, minus one. [¶](#section-4.3-6.4.1)
- Extended CTR Flag (Y, 1 bit):
- 
            Indicates if the C field contains the CTR or the CTR length. [¶](#section-4.3-6.6.1)
- CTR or CTR Length (C, 3 bits):
- 
            This field contains the CTR if the Y flag is set to 0, or the CTR length, minus one, if set to 1. [¶](#section-4.3-6.8.1)

The KID and CTR fields are encoded as compact unsigned integers in
network (big-endian) byte order.  If the value of one of these fields is in the
range 0-7, then the value is carried in the corresponding bits of the config
byte (K or C) and the corresponding flag (X or Y) is set to zero.  Otherwise,
the value MUST be encoded with the minimum number of bytes required and
appended after the config byte, with the KID first and CTR second.
The header field (K or C) is set to the number of bytes in the encoded value,
minus one.  The value 000 represents a length of 1, 001 a length of 2, etc.
This allows a 3-bit length field to represent the value lengths 1-8.[¶](#section-4.3-7)

The SFrame header can thus take one of the four forms shown in
[Figure 4](#fig-sframe-header-cases), depending on which of the X and Y flags are set.[¶](#section-4.3-8)

### 
[4.4.](#section-4.4) [Encryption Schema](#name-encryption-schema)
        

SFrame encryption uses an AEAD encryption algorithm and hash function defined by
the cipher suite in use (see [Section 4.5](#cipher-suites)).  We will refer to the following
aspects of the AEAD and the hash algorithm below:[¶](#section-4.4-1)

- 
            `AEAD` and.Encrypt `AEAD` - The encryption and decryption functions
for the AEAD.  We follow the convention of RFC 5116 [.Decrypt [RFC5116](#RFC5116) ] and consider
the authentication tag part of the ciphertext produced by`AEAD` (as
opposed to a separate field as in SRTP [.Encrypt [RFC3711](#RFC3711) ]).[¶](#section-4.4-2.1.1)
- 
            `AEAD` - The size in bytes of a key for the encryption algorithm.Nk [¶](#section-4.4-2.2.1)
- 
            `AEAD` - The size in bytes of a nonce for the encryption algorithm.Nn [¶](#section-4.4-2.3.1)
- 
            `AEAD` - The overhead in bytes of the encryption algorithm (typically the
size of a "tag" that is added to the plaintext).Nt [¶](#section-4.4-2.4.1)
- 
            `AEAD` - For cipher suites using the compound AEAD described in.Nka [Section 4.5.1](#aes-ctr-with-sha2) , the size in bytes of a key for the underlying encryption
algorithm[¶](#section-4.4-2.5.1)
- 
            `Hash` - The size in bytes of the output of the hash function.Nh [¶](#section-4.4-2.6.1)

#### 
[4.4.1.](#section-4.4.1) [Key Selection](#name-key-selection)
          

Each SFrame encryption or decryption operation is premised on a single secret
`base_`, which is labeled with an integer KID value signaled in the SFrame
header.[¶](#section-4.4.1-1)

The sender and receivers need to agree on which `base_` should be used for a given
KID.  Moreover, senders and receivers need to agree on whether a `base_` will be used
for encryption or decryption only. The process for provisioning `base_` values and their KID
values is beyond the scope of this specification, but its security properties will
bound the assurances that SFrame provides.  For example, if SFrame is used to
provide E2E security against intermediary media nodes, then SFrame keys need to
be negotiated in a way that does not make them accessible to these intermediaries.[¶](#section-4.4.1-2)

For each known KID value, the client stores the corresponding symmetric key
`base_`.  For keys that can be used for encryption, the client also stores
the next CTR value to be used when encrypting (initially 0).[¶](#section-4.4.1-3)

When encrypting a plaintext, the application specifies which KID is to be used,
and the CTR value is incremented after successful encryption.  When decrypting,
the `base_` for decryption is selected from the available keys using the KID
value in the SFrame header.[¶](#section-4.4.1-4)

A given `base_` MUST NOT be used for encryption by multiple senders.  Such reuse
would result in multiple encrypted frames being generated with the same (key,
nonce) pair, which harms the protections provided by many AEAD algorithms.
Implementations MUST mark each `base_` as usable for encryption or decryption,
never both.[¶](#section-4.4.1-5)

Note that the set of available keys might change over the lifetime of a
real-time session.  In such cases, the client will need to manage key usage to
avoid media loss due to a key being used to encrypt before all receivers are
able to use it to decrypt.  For example, an application may make decryption-[¶](#section-4.4.1-6)

#### 
[4.4.2.](#section-4.4.2) [Key Derivation](#name-key-derivation)
          

SFrame encryption and decryption use a key and salt derived from the `base_`
associated with a KID.  Given a `base_` value, the key and salt are derived
using HMAC-based Key Derivation Function (HKDF) [[RFC5869](#RFC5869)] as follows:[¶](#section-4.4.2-1)

```
def derive_key_salt(KID, base_key):
  sframe_secret = HKDF-Extract("", base_key)
  sframe_key_label = "SFrame 1.0 Secret key " + KID + cipher_suite
  sframe_key =
    HKDF-Expand(sframe_secret, sframe_key_label, AEAD.Nk)
  sframe_salt_label = "SFrame 1.0 Secret salt " + KID + cipher_suite
  sframe_salt =
    HKDF-Expand(sframe_secret, sframe_salt_label, AEAD.Nn)
  return sframe_key, sframe_salt
```
[¶](#section-4.4.2-2)

In the derivation of `sframe_`:[¶](#section-4.4.2-3)

- 
              The `+` operator represents concatenation of byte strings.[¶](#section-4.4.2-4.1.1)
- 
              The KID value is encoded as an 8-byte big-endian integer, not the compressed form used in the SFrame header. [¶](#section-4.4.2-4.2.1)
- 
              The `cipher_` value is a 2-byte big-endian integer representing the
cipher suite in use (seesuite [Section 8.1](#sframe-cipher-suites) ).[¶](#section-4.4.2-4.3.1)

The hash function used for HKDF is determined by the cipher suite in use.[¶](#section-4.4.2-5)

#### 
[4.4.3.](#section-4.4.3) [Encryption](#name-encryption)
          

SFrame encryption uses the AEAD encryption algorithm for the cipher suite in use.
The key for the encryption is the `sframe_`.  The nonce is formed by first XORing
the `sframe_` with the current CTR value, and then encoding the result as a big-endian integer of
length `AEAD`.[¶](#section-4.4.3-1)

The encryptor forms an SFrame header using the CTR and KID values provided.
The encoded header is provided as AAD to the AEAD encryption operation, together
with application-[Section 9.4](#metadata)).[¶](#section-4.4.3-2)

def encrypt(CTR, KID, metadata, plaintext):
  sframe_key, sframe_salt = key_store[KID]
  # encode_big_endian(x, n) produces an n-byte string encoding the
  # integer x in big-endian byte order.
  ctr = encode_big_endian(CTR, AEAD.Nn)
  nonce = xor(sframe_salt, CTR)
  # encode_sframe_header produces a byte string encoding the
  # provided KID and CTR values into an SFrame header.
  header = encode_sframe_header(CTR, KID)
  aad = header + metadata
  ciphertext = AEAD.Encrypt(sframe_key, nonce, aad, plaintext)
  return header + ciphertext

[¶](#section-4.4.3-3)

For example, the metadata input to encryption allows for frame metadata to be
authenticated when SFrame is applied per frame.  After encoding the frame and
before packetizing it, the necessary media metadata will be moved out of the
encoded frame buffer to be sent in some channel visible to the SFU (e.g., an
RTP header extension).[¶](#section-4.4.3-4)

#### 
[4.4.4.](#section-4.4.4) [Decryption](#name-decryption)
          

Before decrypting, a receiver needs to assemble a full SFrame ciphertext. When
an SFrame ciphertext is fragmented into multiple parts for transport (e.g.,
a whole encrypted frame sent in multiple SRTP packets), the receiving client
collects all the fragments of the ciphertext, using appropriate sequencing
and start/end markers in the transport. Once all of the required fragments are
available, the client reassembles them into the SFrame ciphertext and passes
the ciphertext to SFrame for decryption.[¶](#section-4.4.4-1)

The KID field in the SFrame header is used to find the right key and salt for
the encrypted frame, and the CTR field is used to construct the nonce. The SFrame
decryption procedure is as follows:[¶](#section-4.4.4-2)

def decrypt(metadata, sframe_ciphertext):
  KID, CTR, header, ciphertext = parse_ciphertext(sframe_ciphertext)
  sframe_key, sframe_salt = key_store[KID]
  ctr = encode_big_endian(CTR, AEAD.Nn)
  nonce = xor(sframe_salt, ctr)
  aad = header + metadata
  return AEAD.Decrypt(sframe_key, nonce, aad, ciphertext)

[¶](#section-4.4.4-3)

If a ciphertext fails to decrypt because there is no key available for the KID
in the SFrame header, the client MAY buffer the ciphertext and retry decryption
once a key with that KID is received.  If a ciphertext fails to decrypt for any
other reason, the client MUST discard the ciphertext. Invalid ciphertexts SHOULD be
discarded in a way that is indistinguishable (to an external observer) from having
processed a valid ciphertext.  In other words, the SFrame decrypt operation
should take the same amount of time regardless of whether decryption succeeds or fails.[¶](#section-4.4.4-4)

### 
[4.5.](#section-4.5) [Cipher Suites](#name-cipher-suites)
        

Each SFrame session uses a single cipher suite that specifies the following
primitives:[¶](#section-4.5-1)

- 
            A hash function used for key derivation [¶](#section-4.5-2.1.1)
- 
            An AEAD encryption algorithm [ [RFC5116](#RFC5116) ] used for frame encryption, optionally
with a truncated authentication tag[¶](#section-4.5-2.2.1)

This document defines the following cipher suites, with the constants defined in
[Section 4.4](#encryption-schema):[¶](#section-4.5-3)

| Table 1 :  SFrame Cipher Suite Constants |  |  |  |  |  | 
|---|---|---|---|---|---|
| Name | Nh | Nka | Nk | Nn | Nt | 
|---|---|---|---|---|---|
| `AES_` | 32 | 16 | 48 | 12 | 10 | 
| `AES_` | 32 | 16 | 48 | 12 | 8 | 
| `AES_` | 32 | 16 | 48 | 12 | 4 | 
| `AES_` | 32 | n/a | 16 | 12 | 16 | 
| `AES_` | 64 | n/a | 32 | 12 | 16 | 

[Table 1](#table-1):

[SFrame Cipher Suite Constants](#name-sframe-cipher-suite-constan)

Numeric identifiers for these cipher suites are defined in the IANA registry
created in [Section 8.1](#sframe-cipher-suites).[¶](#section-4.5-5)

In the suite names, the length of the authentication tag is indicated by
the last value: "_128" indicates a 128-bit tag, "_80" indicates
an 80-bit tag, "_64" indicates a 64-bit tag, and "_32" indicates a
32-bit tag.[¶](#section-4.5-6)

In a session that uses multiple media streams, different cipher suites might be
configured for different media streams.  For example, in order to conserve
bandwidth, a session might use a cipher suite with 80-bit tags for video frames
and another cipher suite with 32-bit tags for audio frames.[¶](#section-4.5-7)

#### 
[4.5.1.](#section-4.5.1) [AES-CTR with SHA2](#name-aes-ctr-with-sha2)
          

In order to allow very short tag sizes, we define a synthetic AEAD function
using the authenticated counter mode of AES together with HMAC for
authentication.  We use an encrypt-[RFC3711](#RFC3711)].[¶](#section-4.5.1-1)

Before encryption or decryption, encryption and authentication subkeys are
derived from the single AEAD key.  The overall length of the AEAD key is ```
Nka +
Nh
```
, where `Nka` represents the key size for the AES block cipher in use and `Nh`
represents the output size of the hash function  (as in [Section 4.4](#encryption-schema)).
The encryption subkey comprises the first `Nka` bytes and the authentication
subkey comprises the remaining `Nh` bytes.[¶](#section-4.5.1-2)

def derive_subkeys(sframe_key):
  # The encryption key comprises the first Nka bytes
  enc_key = sframe_key[..Nka]
  # The authentication key comprises Nh remaining bytes
  auth_key = sframe_key[Nka..]
  return enc_key, auth_key

[¶](#section-4.5.1-3)

The AEAD encryption and decryption functions are then composed of individual
calls to the CTR encrypt function and HMAC.  The resulting MAC value is truncated
to a number of bytes `Nt` fixed by the cipher suite.[¶](#section-4.5.1-4)

```
def truncate(tag, n):
  # Take the first `n` bytes of `tag`
  return tag[..n]
def compute_tag(auth_key, nonce, aad, ct):
  aad_len = encode_big_endian(len(aad), 8)
  ct_len = encode_big_endian(len(ct), 8)
  tag_len = encode_big_endian(Nt, 8)
  auth_data = aad_len + ct_len + tag_len + nonce + aad + ct
  tag = HMAC(auth_key, auth_data)
  return truncate(tag, Nt)
def AEAD.Encrypt(key, nonce, aad, pt):
  enc_key, auth_key = derive_subkeys(key)
  initial_counter = nonce + 0x00000000 # append four zero bytes
  ct = AES-CTR.Encrypt(enc_key, initial_counter, pt)
  tag = compute_tag(auth_key, nonce, aad, ct)
  return ct + tag
def AEAD.Decrypt(key, nonce, aad, ct):
  inner_ct, tag = split_ct(ct, tag_len)
  enc_key, auth_key = derive_subkeys(key)
  candidate_tag = compute_tag(auth_key, nonce, aad, inner_ct)
  if !constant_time_equal(tag, candidate_tag):
    raise Exception("Authentication Failure")
  initial_counter = nonce + 0x00000000 # append four zero bytes
  return AES-CTR.Decrypt(enc_key, initial_counter, inner_ct)
```
[¶](#section-4.5.1-5)

## 
[5.](#section-5) [Key Management](#name-key-management)
      

SFrame must be integrated with an E2E key management framework to exchange and
rotate the keys used for SFrame encryption. The key management
framework provides the following functions:[¶](#section-5-1)

- 
          Provisioning KID / `base_` mappings to participating clientskey [¶](#section-5-2.1.1)
- 
          Updating the above data as clients join or leave [¶](#section-5-2.2.1)

It is the responsibility of the application to provide the key management
framework, as described in [Section 9.2](#key-management-framework).[¶](#section-5-3)

### 
[5.1.](#section-5.1) [Sender Keys](#name-sender-keys)
        

If the participants in a call have a preexisting E2E-secure channel, they can
use it to distribute SFrame keys.  Each client participating in a call generates
a fresh `base_` value that it will use to encrypt media. The client then uses
the E2E-secure channel to send their encryption key to the other participants.[¶](#section-5.1-1)

In this scheme, it is assumed that receivers have a signal outside of SFrame for
which client has sent a given frame (e.g., an RTP synchronization source (SSRC)).  SFrame KID
values are then used to distinguish between versions of the sender's `base_`.[¶](#section-5.1-2)

KID values in this scheme have two parts: a "key generation" and a "ratchet step".
Both are unsigned integers that begin at zero.  The key generation increments
each time the sender distributes a new key to receivers.  The ratchet step is
incremented each time the sender ratchets their key forward for forward secrecy:[¶](#section-5.1-3)

```
base_key[i+1] = HKDF-Expand(
                  HKDF-Extract("", base_key[i]),
                  "SFrame 1.0 Ratchet", CipherSuite.Nh)
```
[¶](#section-5.1-4)

For compactness, we do not send the whole ratchet step.  Instead, we send only
its low-order `R` bits, where `R` is a value set by the application.  Different
senders may use different values of `R`, but each receiver of a given sender
needs to know what value of `R` is used by the sender so that they can recognize
when they need to ratchet (vs. expecting a new key).  `R` effectively defines a
reordering window, since no more than 2<sup>`R`</sup> ratchet steps can be
active at a given time.  The key generation is sent in the remaining `64 - R`
bits of the KID.[¶](#section-5.1-5)

KID = (key_generation << R) + (ratchet_step % (1 << R))

[¶](#section-5.1-6)

The sender signals such a ratchet step update by sending with a KID value in
which the ratchet step has been incremented.  A receiver who receives from a
sender with a new KID computes the new key as above.  The old key may be kept
for some time to allow for out-of-order delivery, but should be deleted
promptly.[¶](#section-5.1-8)

If a new participant joins in the middle of a session, they will need to receive
from each sender (a) the current sender key for that sender and (b) the current
KID value for the sender. Evicting a participant requires each sender to send
a fresh sender key to all receivers.[¶](#section-5.1-9)

It is the application's responsibility to decide when sender keys are updated.  A sender
key may be updated by sending a new `base_` (updating the key generation) or
by hashing the current `base_` (updating the ratchet step).  Ratcheting the
key forward is useful when adding new receivers to an SFrame-based interaction,
since it ensures that the new receivers can't decrypt any media encrypted before
they were added.  If a sender wishes to assure the opposite property when
removing a receiver (i.e., ensuring that the receiver can't decrypt media after
they are removed), then the sender will need to distribute a new sender key.[¶](#section-5.1-10)

### 
[5.2.](#section-5.2) [MLS](#name-mls)
        

The Messaging Layer Security (MLS) protocol provides group authenticated key
exchange [[MLS-ARCH](#I-D.ietf-mls-architecture)] [[MLS-PROTO](#RFC9420)].  In
principle, it could be used to instantiate the sender key scheme above, but it
can also be used more efficiently directly.[¶](#section-5.2-1)

MLS creates a linear sequence of keys, each of which is shared among the members
of a group at a given point in time.  When a member joins or leaves the group, a
new key is produced that is known only to the augmented or reduced group.  Each
step in the lifetime of the group is known as an "epoch", and each member of the
group is assigned an "index" that is constant for the time they are in the
group.[¶](#section-5.2-2)

To generate keys and nonces for SFrame, we use the MLS exporter function to
generate a `base_` value for each MLS epoch.  Each member of the group is
assigned a set of KID values so that each member has a unique `sframe_` and
`sframe_` that it uses to encrypt with.  Senders may choose any KID value
within their assigned set of KID values, e.g., to allow a single sender to send
multiple, uncoordinated outbound media streams.[¶](#section-5.2-3)

```
base_key = MLS-Exporter("SFrame 1.0 Base Key", "", AEAD.Nk)
```
[¶](#section-5.2-4)

For compactness, we do not send the whole epoch number.  Instead, we send only
its low-order `E` bits, where `E` is a value set by the application.  `E`
effectively defines a reordering window, since no more than 2<sup>`E`</sup>
epochs can be active at a given time.  To handle rollover of the epoch counter,
receivers MUST remove an old epoch when a new epoch with the same low-order
E bits is introduced.[¶](#section-5.2-5)

Let `S` be the number of bits required to encode a member index in the group,
i.e., the smallest value such that `group_`.  The sender index
is encoded in the `S` bits above the epoch.  The remaining `64 - S - E` bits of
the KID value are a `context` value chosen by the sender (`context` value `0` will
produce the shortest encoded KID).[¶](#section-5.2-6)

KID = (context << (S + E)) + (sender_index << E) + (epoch % (1 << E))

[¶](#section-5.2-7)

Once an SFrame stack has been provisioned with the `sframe_` for an
epoch, it can compute the required KID values on demand (as well as the
resulting SFrame keys/nonces derived from the `base_` and KID) as it needs
to encrypt or decrypt for a given member.[¶](#section-5.2-9)

## 
[6.](#section-6) [Media Considerations](#name-media-considerations)
      

### 
[6.1.](#section-6.1) [Selective Forwarding Units](#name-selective-forwarding-units)
        

SFUs (e.g., those described in [Section 3.7](https://rfc-editor.org/rfc/rfc7667#section-3.7) of [[RFC7667](#RFC7667)]) receive the media streams from each participant and select which
ones should be forwarded to each of the other participants.  There are several
approaches for stream selection, but in general, the SFU needs to access
metadata associated with each frame and modify the RTP information of the incoming
packets when they are transmitted to the received participants.[¶](#section-6.1-1)

This section describes how these normal SFU modes of operation interact with the
E2EE provided by SFrame.[¶](#section-6.1-2)

#### 
[6.1.1.](#section-6.1.1) [RTP Stream Reuse](#name-rtp-stream-reuse)
          

The SFU may choose to send only a certain number of streams based on the voice
activity of the participants. To avoid the overhead involved in establishing new
transport streams, the SFU may decide to reuse previously existing streams or
even pre-allocate a predefined number of streams and choose in each moment in
time which participant media will be sent through it.[¶](#section-6.1.1-1)

This means that the same transport-[¶](#section-6.1.1-2)

Note that in order to prevent impersonation by a malicious participant (not the
SFU), a mechanism based on digital signature would be required. SFrame does not
protect against such attacks.[¶](#section-6.1.1-3)

#### 
[6.1.2.](#section-6.1.2) [Simulcast](#name-simulcast)
          

When using simulcast, the same input image will produce N different encoded
frames (one per simulcast layer), which would be processed independently by the
frame encryptor and assigned an unique CTR value for each.[¶](#section-6.1.2-1)

#### 
[6.1.3.](#section-6.1.3) [Scalable Video Coding (SVC)](#name-scalable-video-coding-svc)
          

In both temporal and spatial scalability, the SFU may choose to drop layers in
order to match a certain bitrate or to forward specific media sizes or frames per
second. In order to support the SFU selectively removing layers, the sender MUST
encapsulate each layer in a different SFrame ciphertext.[¶](#section-6.1.3-1)

### 
[6.2.](#section-6.2) [Video Key Frames](#name-video-key-frames)
        

Forward security and post-[¶](#section-6.2-1)

The key exchange happens asynchronously and on a different path than the SFU signaling
and media. So it may happen that when a new participant joins the call and the
SFU side requests a key frame, the sender generates the E2EE frame
with a key that is not known by the receiver, so it will be discarded. When the sender
updates his sending key with the new key, it will send it in a non-key frame, so
the receiver will be able to decrypt it, but not decode it.[¶](#section-6.2-2)

The new receiver will then re-request a key frame, but due to sender and SFU
policies, that new key frame could take some time to be generated.[¶](#section-6.2-3)

If the sender sends a key frame after the new E2EE key is in use, the time
required for the new participant to display the video is minimized.[¶](#section-6.2-4)

Note that this issue does not arise for media streams that do not have
dependencies among frames, e.g., audio streams.  In these streams, each frame is
independently decodable, so a frame never depends on another frame that might be
on the other side of a key rotation.[¶](#section-6.2-5)

### 
[6.3.](#section-6.3) [Partial Decoding](#name-partial-decoding)
        

Some codecs support partial decoding, where individual packets can be decoded
without waiting for the full frame to arrive.  When SFrame is applied per frame,
partial decoding is not possible because the decoder cannot access data until an entire
frame has arrived and has been decrypted.[¶](#section-6.3-1)

## 
[7.](#section-7) [Security Considerations](#name-security-considerations)
      

### 
[7.1.](#section-7.1) [No Header Confidentiality](#name-no-header-confidentiality)
        

SFrame provides integrity protection to the SFrame header (the KID and
CTR values), but it does not provide confidentiality protection.  Parties that
can observe the SFrame header may learn, for example, which parties are sending
SFrame payloads (from KID values) and at what rates (from CTR values).  In cases
where SFrame is used for end-to-end security on top of hop-by-hop protections
(e.g., running over SRTP as described in [Appendix B.5](#sframe-over-rtp)), the hop-by-hop security
mechanisms provide confidentiality protection of the SFrame header between hops.[¶](#section-7.1-1)

### 
[7.2.](#section-7.2) [No Per-Sender Authentication](#name-no-per-sender-authenticatio)
        

SFrame does not provide per-sender authentication of media data.  Any sender in
a session can send media that will be associated with any other sender.  This is
because SFrame uses symmetric encryption to protect media data, so that any
receiver also has the keys required to encrypt packets for the sender.[¶](#section-7.2-1)

### 
[7.3.](#section-7.3) [Key Management](#name-key-management-2)
        

The specifics of key management are beyond the scope of this document. However, every client
SHOULD change their keys when new clients join or leave the call for forward
secrecy and post-[¶](#section-7.3-1)

### 
[7.4.](#section-7.4) [Replay](#name-replay)
        

The handling of replay is out of the scope of this document. However, senders
MUST reject requests to encrypt multiple times with the same key and nonce
since several AEAD algorithms fail badly in such cases (see, e.g., [Section 5.1.1](https://rfc-editor.org/rfc/rfc5116#section-5.1.1) of [[RFC5116](#RFC5116)]).[¶](#section-7.4-1)

## 
[8.](#section-8) [IANA Considerations](#name-iana-considerations)
      

IANA has created a new registry called "SFrame Cipher Suites" ([Section 8.1](#sframe-cipher-suites))
under the "SFrame" group registry heading.[¶](#section-8-1)

### 
[8.1.](#section-8.1) [SFrame Cipher Suites](#name-sframe-cipher-suites)
        

The "SFrame Cipher Suites" registry lists identifiers for SFrame cipher suites as defined in
[Section 4.5](#cipher-suites).  The cipher suite field is two bytes wide, so the valid cipher
suites are in the range 0x0000 to 0xFFFF.  Except as noted below, assignments are made
via the Specification Required policy [[RFC8126](#RFC8126)].[¶](#section-8.1-1)

The registration template is as follows:[¶](#section-8.1-2)

- 
            Value: The numeric value of the cipher suite [¶](#section-8.1-3.1.1)
- 
            Name: The name of the cipher suite [¶](#section-8.1-3.2.1)
- 
            Recommended: Whether support for this cipher suite is recommended by the IETF. Valid values are "Y", "N", and "D" as described in [Section 17.1](https://rfc-editor.org/rfc/rfc9420#section-17.1) of [[MLS-PROTO](#RFC9420) ]. The default value of the "Recommended" column is "N". Setting the
Recommended item to "Y" or "D", or changing an item whose current value is "Y"
or "D", requires Standards Action [[RFC8126](#RFC8126) ].[¶](#section-8.1-3.3.1)
- 
            Reference: The document where this cipher suite is defined [¶](#section-8.1-3.4.1)
- 
            Change Controller: Who is authorized to update the row in the registry [¶](#section-8.1-3.5.1)

Initial contents:[¶](#section-8.1-4)

| Table 2 :  SFrame Cipher Suites |  |  |  |  | 
|---|---|---|---|---|
| Value | Name | R | Reference | Change Controller | 
|---|---|---|---|---|
| 0x0000 | Reserved | - | RFC 9605 | IETF | 
| 0x0001 | `AES_` | Y | RFC 9605 | IETF | 
| 0x0002 | `AES_` | Y | RFC 9605 | IETF | 
| 0x0003 | `AES_` | Y | RFC 9605 | IETF | 
| 0x0004 | `AES_` | Y | RFC 9605 | IETF | 
| 0x0005 | `AES_` | Y | RFC 9605 | IETF | 
| 0xF000 - 0xFFFF | Reserved for Private Use | - | RFC 9605 | IETF | 

[Table 2](#table-2):

[SFrame Cipher Suites](#name-sframe-cipher-suites-2)

## 
[9.](#section-9) [Application Responsibilities](#name-application-responsibilitie)
      

To use SFrame, an application needs to define the inputs to the SFrame
encryption and decryption operations, and how SFrame ciphertexts are delivered
from sender to receiver (including any fragmentation and reassembly).  In this
section, we lay out additional requirements that an application must meet in
order for SFrame to operate securely.[¶](#section-9-1)

In general, an application using SFrame is responsible for configuring SFrame.
The application must first define when SFrame is applied at all.  When SFrame is
applied, the application must define which cipher suite is to be used.  If new
versions of SFrame are defined in the future, it will be the application's responsibility
to determine which version should be used.[¶](#section-9-2)

This division of responsibilities is similar to the way other media parameters
(e.g., codecs) are typically handled in media applications, in the sense that
they are set up in some signaling protocol and not described in the media.
Applications might find it useful to extend the protocols used for negotiating
other media parameters (e.g., Session Description Protocol (SDP) [[RFC8866](#RFC8866)]) to also negotiate parameters for
SFrame.[¶](#section-9-3)

### 
[9.1.](#section-9.1) [Header Value Uniqueness](#name-header-value-uniqueness)
        

Applications MUST ensure that each (`base_`, KID, CTR) combination is used
for at most one SFrame encryption operation. This ensures that the (key, nonce)
pairs used by the underlying AEAD algorithm are never reused. Typically this is
done by assigning each sender a KID or set of KIDs, then having each sender use
the CTR field as a monotonic counter, incrementing for each plaintext that is
encrypted. In addition to its simplicity, this scheme minimizes overhead by
keeping CTR values as small as possible.[¶](#section-9.1-1)

In applications where an SFrame context might be written to persistent storage,
this context needs to include the last-used CTR value.  When the context is used
later, the application should use the stored CTR value to determine the next CTR
value to be used in an encryption operation, and then write the next CTR value
back to storage before using the CTR value for encryption.  Storing the CTR
value before usage (vs. after) helps ensure that a storage failure will not
cause reuse of the same (`base_`, KID, CTR) combination.[¶](#section-9.1-2)

### 
[9.2.](#section-9.2) [Key Management Framework](#name-key-management-framework)
        

The application is responsible for provisioning SFrame with a mapping of KID values to
`base_` values and the resulting keys and salts.  More importantly, the
application specifies which KID values are used for which purposes (e.g., by
which senders).  An application's KID assignment strategy MUST be structured to
assure the non-reuse properties discussed in [Section 9.1](#header-value-uniqueness).[¶](#section-9.2-1)

The application is also responsible for defining a rotation schedule for keys.  For
example, one application might have an ephemeral group for every call and keep
rotating keys when endpoints join or leave the call, while another application
could have a persistent group that can be used for multiple calls and simply
derives ephemeral symmetric keys for a specific call.[¶](#section-9.2-2)

It should be noted that KID values are not encrypted by SFrame and are thus
visible to any application-[Section 5.1](#sender-keys), the number of ratchet steps per sender is exposed, and in
the scheme of [Section 5.2](#mls), the number of epochs and the MLS sender ID of the SFrame
sender are exposed.[¶](#section-9.2-3)

### 
[9.3.](#section-9.3) [Anti-Replay](#name-anti-replay)
        

It is the responsibility of the application to handle anti-replay. Replay by network
attackers is assumed to be prevented by network-layer facilities (e.g., TLS, SRTP).
As mentioned in [Section 7.4](#replay), senders MUST reject requests to encrypt multiple times
with the same key and nonce.[¶](#section-9.3-1)

It is not mandatory to implement anti-replay on the receiver side. Receivers MAY
apply time- or counter-based anti-replay mitigations.  For example, [Section 3.3.2](https://rfc-editor.org/rfc/rfc3711#section-3.3.2) of [[RFC3711](#RFC3711)] specifies a counter-based anti-replay mitigation, which
could be adapted to use with SFrame, using the CTR field as the counter.[¶](#section-9.3-2)

### 
[9.4.](#section-9.4) [Metadata](#name-metadata)
        

The `metadata` input to SFrame operations is an opaque byte string specified by the application. As
such, the application needs to define what information should go in the
`metadata` input and ensure that it is provided to the encryption and decryption
functions at the appropriate points.  A receiver MUST NOT use SFrame-[¶](#section-9.4-1)

For example, consider an application where SFrame is used to encrypt audio
frames that are sent over SRTP, with some application data included in the RTP
header extension. Suppose the application also includes this application data in
the SFrame metadata, so that the SFU is allowed to read, but not modify, the
application data.  A receiver can use the application data in the RTP header
extension as part of the standard SRTP decryption process since this is
required to recover the SFrame ciphertext carried in the SRTP payload.  However,
the receiver MUST NOT use the application data for other purposes before SFrame
decryption has authenticated the application data.[¶](#section-9.4-2)

## 
[10.](#section-10) [References](#name-references)
      

### 
[10.1.](#section-10.1) [Normative References](#name-normative-references)
        

- [MLS-PROTO]
- 
Barnes, R., Beurdouche, B., Robert, R., Millican, J., Omara, E., and K. Cohn-Gordon, "The Messaging Layer Security (MLS) Protocol", RFC 9420, DOI 10.17487/RFC9420 , , <[https://](/info/rfc9420) >.www .rfc- editor .org /info /rfc9420
- [RFC2119]
- 
Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119 , , <[https://](/info/rfc2119) >.www .rfc- editor .org /info /rfc2119
- [RFC5116]
- 
McGrew, D., "An Interface and Algorithms for Authenticated Encryption", RFC 5116, DOI 10.17487/RFC5116 , , <[https://](/info/rfc5116) >.www .rfc- editor .org /info /rfc5116
- [RFC5869]
- 
Krawczyk, H. and P. Eronen, "HMAC-based Extract-and- , RFC 5869, DOI 10.17487Expand Key Derivation Function (HKDF)" /RFC5869 , , <[https://](/info/rfc5869) >.www .rfc- editor .org /info /rfc5869
- [RFC8126]
- 
Cotton, M., Leiba, B., and T. Narten, "Guidelines for Writing an IANA Considerations Section in RFCs", BCP 26, RFC 8126, DOI 10.17487/RFC8126 , , <[https://](/info/rfc8126) >.www .rfc- editor .org /info /rfc8126
- [RFC8174]
- 
Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174 , , <[https://](/info/rfc8174) >.www .rfc- editor .org /info /rfc8174

### 
[10.2.](#section-10.2) [Informative References](#name-informative-references)
        

- [MLS-ARCH]
- 
Beurdouche, B., Rescorla, E., Omara, E., Inguva, S., and A. Duric, "The Messaging Layer Security (MLS) Architecture", Work in Progress, Internet-Draft, draft- , , <ietf- mls- architecture-15 [https://](https://datatracker.ietf.org/doc/html/draft-ietf-mls-architecture-15) >.datatracker .ietf .org /doc /html /draft- ietf- mls- architecture-15
- [MOQ-TRANSPORT]
- 
Curley, L., Pugin, K., Nandakumar, S., Vasiliev, V., and I. Swett, Ed., "Media over QUIC Transport", Work in Progress, Internet-Draft, draft- , , <ietf- moq- transport-05 [https://](https://datatracker.ietf.org/doc/html/draft-ietf-moq-transport-05) >.datatracker .ietf .org /doc /html /draft- ietf- moq- transport-05
- [RFC3711]
- 
Baugher, M., McGrew, D., Naslund, M., Carrara, E., and K. Norrman, "The Secure Real-time Transport Protocol (SRTP)", RFC 3711, DOI 10.17487/RFC3711 , , <[https://](/info/rfc3711) >.www .rfc- editor .org /info /rfc3711
- [RFC6716]
- 
Valin, JM., Vos, K., and T. Terriberry, "Definition of the Opus Audio Codec", RFC 6716, DOI 10.17487/RFC6716 , , <[https://](/info/rfc6716) >.www .rfc- editor .org /info /rfc6716
- [RFC7656]
- 
Lennox, J., Gross, K., Nandakumar, S., Salgueiro, G., and B. Burman, Ed., "A Taxonomy of Semantics and Mechanisms for Real-Time Transport Protocol (RTP) Sources", RFC 7656, DOI 10.17487/RFC7656 , , <[https://](/info/rfc7656) >.www .rfc- editor .org /info /rfc7656
- [RFC7667]
- 
Westerlund, M. and S. Wenger, "RTP Topologies", RFC 7667, DOI 10.17487/RFC7667 , , <[https://](/info/rfc7667) >.www .rfc- editor .org /info /rfc7667
- [RFC8723]
- 
Jennings, C., Jones, P., Barnes, R., and A.B. Roach, "Double Encryption Procedures for the Secure Real-Time Transport Protocol (SRTP)", RFC 8723, DOI 10.17487/RFC8723 , , <[https://](/info/rfc8723) >.www .rfc- editor .org /info /rfc8723
- [RFC8866]
- 
Begen, A., Kyzivat, P., Perkins, C., and M. Handley, "SDP: Session Description Protocol", RFC 8866, DOI 10.17487/RFC8866 , , <[https://](/info/rfc8866) >.www .rfc- editor .org /info /rfc8866
- [RTP-PAYLOAD]
- 
Murillo, S. G., Fablet, Y., and A. Gouaillard, "Codec agnostic RTP payload format for video", Work in Progress, Internet-Draft, draft- , , <gouaillard- avtcore- codec- agn- rtp- payload-01 [https://](https://datatracker.ietf.org/doc/html/draft-gouaillard-avtcore-codec-agn-rtp-payload-01) >.datatracker .ietf .org /doc /html /draft- gouaillard- avtcore- codec- agn- rtp- payload-01
- [TestVectors]
- 
"SFrame Test Vectors", commit 025d568, , <[https://](https://github.com/sframe-wg/sframe/blob/025d568/test-vectors/test-vectors.json) >.github .com /sframe-wg /sframe /blob /025d568 /test- vectors /test- vectors .json
- [WEBTRANSPORT]
- 
Vasiliev, V., "The WebTransport Protocol Framework", Work in Progress, Internet-Draft, draft- , , <ietf- webtrans- overview-08 [https://](https://datatracker.ietf.org/api/v1/doc/document/draft-ietf-webtrans-overview/) >.datatracker .ietf .org /api /v1 /doc /document /draft- ietf- webtrans- overview/

## 
[Appendix A.](#appendix-A) [Example API](#name-example-api)
      

**This section is not normative.**[¶](#appendix-A-1)

This section describes a notional API that an SFrame implementation might
expose.  The core concept is an "SFrame context", within which KID values are
meaningful.  In the key management scheme described in [Section 5.1](#sender-keys), each
sender has a different context; in the scheme described in [Section 5.2](#mls), all senders
share the same context.[¶](#appendix-A-2)

An SFrame context stores mappings from KID values to "key contexts", which are
different depending on whether the KID is to be used for sending or receiving
(an SFrame key should never be used for both operations).  A key context tracks
the key and salt associated to the KID, and the current CTR value.  A key
context to be used for sending also tracks the next CTR value to be used.[¶](#appendix-A-3)

The primary operations on an SFrame context are as follows:[¶](#appendix-A-4)

- 
          **Create an SFrame context:** The context is initialized with a cipher suite and
no KID mappings.[¶](#appendix-A-5.1.1)
- 
          **Add a key for sending:** The key and salt are derived from the base key and
used to initialize a send context, together with a zero CTR value.[¶](#appendix-A-5.2.1)
- 
          **Add a key for receiving:** The key and salt are derived from the base key and
used to initialize a send context.[¶](#appendix-A-5.3.1)
- 
          **Encrypt a plaintext:** Encrypt a given plaintext using the key for a given KID,
including the specified metadata.[¶](#appendix-A-5.4.1)
- 
          **Decrypt an SFrame ciphertext:** Decrypt an SFrame ciphertext with the KID
and CTR values specified in the SFrame header, and the provided metadata.[¶](#appendix-A-5.5.1)

[Figure 10](#rust-api) shows an example of the types of structures and methods that could
be used to create an SFrame API in Rust.[¶](#appendix-A-6)

## 
[Appendix B.](#appendix-B) [Overhead Analysis](#name-overhead-analysis)
      

Any use of SFrame will impose overhead in terms of the amount of bandwidth
necessary to transmit a given media stream.  Exactly how much overhead will be added
depends on several factors:[¶](#appendix-B-1)

- 
          The number of senders involved in a conference (length of KID) [¶](#appendix-B-2.1.1)
- 
          The duration of the conference (length of CTR) [¶](#appendix-B-2.2.1)
- 
          The cipher suite in use (length of authentication tag) [¶](#appendix-B-2.3.1)
- 
          Whether SFrame is used to encrypt packets, whole frames, or some other unit [¶](#appendix-B-2.4.1)

Overall, the overhead rate in kilobits per second can be estimated as:[¶](#appendix-B-3)

```
OverheadKbps = (1 + |CTR| + |KID| + |TAG|) * 8 * CTPerSecond / 1024
```
[¶](#appendix-B-4)

Here the constant value `1` reflects the fixed SFrame header; `|CTR|` and
`|KID|` reflect the lengths of those fields; `|TAG|` reflects the cipher
overhead; and `CTPerSecond` reflects the number of SFrame ciphertexts
sent per second (e.g., packets or frames per second).[¶](#appendix-B-5)

In the remainder of this section, we compute overhead estimates for a collection
of common scenarios.[¶](#appendix-B-6)

### 
[B.1.](#appendix-B.1) [Assumptions](#name-assumptions)
        

In the below calculations, we make conservative assumptions about SFrame
overhead so that the overhead amounts we compute here are likely to be an upper
bound of those seen in practice.[¶](#appendix-B.1-1)

| Table 3 :  Overhead Analysis Assumptions |  |  | 
|---|---|---|
| Field | Bytes | Explanation | 
|---|---|---|
| Config byte | 1 | Fixed | 
| Key ID (KID) | 2 | >255 senders; or MLS epoch (E=4) and >16 senders | 
| Counter (CTR) | 3 | More than 24 hours of media in common cases | 
| Cipher overhead | 16 | Full authentication tag (longest defined here) | 

[Table 3](#table-3):

[Overhead Analysis Assumptions](#name-overhead-analysis-assumptio)

In total, then, we assume that each SFrame encryption will add 22 bytes of
overhead.[¶](#appendix-B.1-3)

We consider two scenarios: applying SFrame per frame and per packet.  In each
scenario, we compute the SFrame overhead in absolute terms (kbps) and as a
percentage of the base bandwidth.[¶](#appendix-B.1-4)

### 
[B.2.](#appendix-B.2) [Audio](#name-audio)
        

In audio streams, there is typically a one-to-one relationship between frames
and packets, so the overhead is the same whether one uses SFrame at a per-packet
or per-frame level.[¶](#appendix-B.2-1)

[Table 4](#audio-overhead) considers three scenarios that are based on recommended configurations
of the Opus codec [[RFC6716](#RFC6716)] (where "fps" stands for "frames per second"):[¶](#appendix-B.2-2)

| Table 4 :  SFrame Overhead for Audio Streams |  |  |  |  |  | 
|---|---|---|---|---|---|
| Scenario | Frame length | fps | Base kbps | Overhead kbps | Overhead % | 
|---|---|---|---|---|---|
| Narrow-band speech | 120 ms | 8.3 | 8 | 1.4 | 17.9% | 
| Full-band speech | 20 ms | 50 | 32 | 8.6 | 26.9% | 
| Full-band stereo music | 10 ms | 100 | 128 | 17.2 | 13.4% | 

[Table 4](#table-4):

[SFrame Overhead for Audio Streams](#name-sframe-overhead-for-audio-s)

### 
[B.3.](#appendix-B.3) [Video](#name-video)
        

Video frames can be larger than an MTU and thus are commonly split across
multiple frames.  Tables [5](#video-overhead-per-frame)
and [6](#video-overhead-per-packet)
show the estimated overhead of encrypting a video stream, where SFrame is
applied per frame and per packet, respectively.  The choices of resolution,
frames per second, and bandwidth roughly reflect the capabilities of
modern video codecs across a range from very low to very high quality.[¶](#appendix-B.3-1)

| Table 5 :  SFrame Overhead for a Video Stream Encrypted per Frame |  |  |  |  | 
|---|---|---|---|---|
| Scenario | fps | Base kbps | Overhead kbps | Overhead % | 
|---|---|---|---|---|
| 426 x 240 | 7.5 | 45 | 1.3 | 2.9% | 
| 640 x 360 | 15 | 200 | 2.6 | 1.3% | 
| 640 x 360 | 30 | 400 | 5.2 | 1.3% | 
| 1280 x 720 | 30 | 1500 | 5.2 | 0.3% | 
| 1920 x 1080 | 60 | 7200 | 10.3 | 0.1% | 

[Table 5](#table-5):

[SFrame Overhead for a Video Stream Encrypted per Frame](#name-sframe-overhead-for-a-video)

| Table 6 :  SFrame Overhead for a Video Stream Encrypted per Packet |  |  |  |  |  | 
|---|---|---|---|---|---|
| Scenario | fps | Packets per Second (pps) | Base kbps | Overhead kbps | Overhead % | 
|---|---|---|---|---|---|
| 426 x 240 | 7.5 | 7.5 | 45 | 1.3 | 2.9% | 
| 640 x 360 | 15 | 30 | 200 | 5.2 | 2.6% | 
| 640 x 360 | 30 | 60 | 400 | 10.3 | 2.6% | 
| 1280 x 720 | 30 | 180 | 1500 | 30.9 | 2.1% | 
| 1920 x 1080 | 60 | 780 | 7200 | 134.1 | 1.9% | 

[Table 6](#table-6):

[SFrame Overhead for a Video Stream Encrypted per Packet](#name-sframe-overhead-for-a-video-)

In the per-frame case, the SFrame percentage overhead approaches zero as the
quality of the video improves since bandwidth is driven more by picture size
than frame rate.  In the per-packet case, the SFrame percentage overhead
approaches the ratio between the SFrame overhead per packet and the MTU (here 22
bytes of SFrame overhead divided by an assumed 1200-byte MTU, or about 1.8%).[¶](#appendix-B.3-4)

### 
[B.4.](#appendix-B.4) [Conferences](#name-conferences)
        

Real conferences usually involve several audio and video streams.  The overhead
of SFrame in such a conference is the aggregate of the overhead across all the
individual streams.  Thus, while SFrame incurs a large percentage overhead on an
audio stream, if the conference also involves a video stream, then the audio
overhead is likely negligible relative to the overall bandwidth of the
conference.[¶](#appendix-B.4-1)

For example, [Table 7](#conference-overhead) shows the overhead estimates for a two-person
conference where one person is sending low-quality media and the other is
sending high-quality media.  (And we assume that SFrame is applied per frame.)  The
video streams dominate the bandwidth at the SFU, so the total bandwidth overhead
is only around 1%.[¶](#appendix-B.4-2)

| Table 7 :  SFrame Overhead for a Two-Person Conference |  |  |  | 
|---|---|---|---|
| Stream | Base Kbps | Overhead Kbps | Overhead % | 
|---|---|---|---|
| Participant 1 audio | 8 | 1.4 | 17.9% | 
| Participant 1 video | 45 | 1.3 | 2.9% | 
| Participant 2 audio | 32 | 9 | 26.9% | 
| Participant 2 video | 1500 | 5 | 0.3% | 
| Total at SFU | 1585 | 16.5 | 1.0% | 

[Table 7](#table-7):

[SFrame Overhead for a Two-Person Conference](#name-sframe-overhead-for-a-two-p)

### 
[B.5.](#appendix-B.5) [SFrame over RTP](#name-sframe-over-rtp)
        

SFrame is a generic encapsulation format, but many of the applications in which
it is likely to be integrated are based on RTP.  This section discusses how an
integration between SFrame and RTP could be done, and some of the challenges
that would need to be overcome.[¶](#appendix-B.5-1)

As discussed in [Section 4.1](#application-context), there are two natural patterns for
integrating SFrame into an application: applying SFrame per frame or per packet.
In RTP-based applications, applying SFrame per packet means that the payload of
each RTP packet will be an SFrame ciphertext, starting with an SFrame header, as
shown in [Figure 11](#sframe-packet).  Applying SFrame per frame means that different
RTP payloads will have different formats: The first payload of a frame will
contain the SFrame headers, and subsequent payloads will contain further chunks
of the ciphertext, as shown in [Figure 12](#sframe-multi-packet).[¶](#appendix-B.5-2)

In order for these media payloads to be properly interpreted by receivers,
receivers will need to be configured to know which of the above schemes the
sender has  applied to a given sequence of RTP packets. SFrame does not provide
a mechanism for distributing this configuration information. In applications
that use SDP for negotiating RTP media streams [[RFC8866](#RFC8866)], an appropriate
extension to SDP could provide this function.[¶](#appendix-B.5-3)

Applying SFrame per frame also requires that packetization and depacketization
be done in a generic manner that does not depend on the media content of the
packets, since the content being packetized or depacketized will be opaque
ciphertext (except for the SFrame header).  In order for such a generic
packetization scheme to work interoperably, one would have to be defined, e.g.,
as proposed in [[RTP-PAYLOAD](#I-D.gouaillard-avtcore-codec-agn-rtp-payload)].[¶](#appendix-B.5-4)

## 
[Appendix C.](#appendix-C) [Test Vectors](#name-test-vectors)
      

This section provides a set of test vectors that implementations can use to
verify that they correctly implement SFrame encryption and decryption.  In
addition to test vectors for the overall process of SFrame
encrypti[Section 4.5.1](#aes-ctr-with-sha2).[¶](#appendix-C-1)

All values are either numeric or byte strings.  Numeric values are represented
as hex values, prefixed with `0x`.  Byte strings are represented in hex
encoding.[¶](#appendix-C-2)

Line breaks and whitespace within values are inserted to conform to the width
requirements of the RFC format.  They should be removed before use.[¶](#appendix-C-3)

These test vectors are also available in JSON format at [[TestVectors](#TestVectors)].  In the
JSON test vectors, numeric values are JSON numbers and byte string values are
JSON strings containing the hex encoding of the byte strings.[¶](#appendix-C-4)

### 
[C.1.](#appendix-C.1) [Header Encoding/Decoding](#name-header-encoding-decoding)
        

For each case, we provide:[¶](#appendix-C.1-1)

An implementation should verify that:[¶](#appendix-C.1-3)

- 
            Encoding a header with the KID and CTR results in the provided header value [¶](#appendix-C.1-4.1.1)
- 
            Decoding the provided header value results in the provided KID and CTR values [¶](#appendix-C.1-4.2.1)

kid: 0x0000000000000000
ctr: 0x0000000000000000
header: 00

[¶](#appendix-C.1-5)

kid: 0x0000000000000000
ctr: 0x0000000000000001
header: 01

[¶](#appendix-C.1-6)

kid: 0x0000000000000000
ctr: 0x00000000000000ff
header: 08ff

[¶](#appendix-C.1-7)

kid: 0x0000000000000000
ctr: 0x0000000000000100
header: 090100

[¶](#appendix-C.1-8)

kid: 0x0000000000000000
ctr: 0x000000000000ffff
header: 09ffff

[¶](#appendix-C.1-9)

kid: 0x0000000000000000
ctr: 0x0000000000010000
header: 0a010000

[¶](#appendix-C.1-10)

kid: 0x0000000000000000
ctr: 0x0000000000ffffff
header: 0affffff

[¶](#appendix-C.1-11)

kid: 0x0000000000000000
ctr: 0x0000000001000000
header: 0b01000000

[¶](#appendix-C.1-12)

kid: 0x0000000000000000
ctr: 0x00000000ffffffff
header: 0bffffffff

[¶](#appendix-C.1-13)

kid: 0x0000000000000000
ctr: 0x0000000100000000
header: 0c0100000000

[¶](#appendix-C.1-14)

kid: 0x0000000000000000
ctr: 0x000000ffffffffff
header: 0cffffffffff

[¶](#appendix-C.1-15)

kid: 0x0000000000000000
ctr: 0x0000010000000000
header: 0d010000000000

[¶](#appendix-C.1-16)

kid: 0x0000000000000000
ctr: 0x0000ffffffffffff
header: 0dffffffffffff

[¶](#appendix-C.1-17)

kid: 0x0000000000000000
ctr: 0x0001000000000000
header: 0e01000000000000

[¶](#appendix-C.1-18)

kid: 0x0000000000000000
ctr: 0x00ffffffffffffff
header: 0effffffffffffff

[¶](#appendix-C.1-19)

kid: 0x0000000000000000
ctr: 0x0100000000000000
header: 0f0100000000000000

[¶](#appendix-C.1-20)

kid: 0x0000000000000000
ctr: 0xffffffffffffffff
header: 0fffffffffffffffff

[¶](#appendix-C.1-21)

kid: 0x0000000000000001
ctr: 0x0000000000000000
header: 10

[¶](#appendix-C.1-22)

kid: 0x0000000000000001
ctr: 0x0000000000000001
header: 11

[¶](#appendix-C.1-23)

kid: 0x0000000000000001
ctr: 0x00000000000000ff
header: 18ff

[¶](#appendix-C.1-24)

kid: 0x0000000000000001
ctr: 0x0000000000000100
header: 190100

[¶](#appendix-C.1-25)

kid: 0x0000000000000001
ctr: 0x000000000000ffff
header: 19ffff

[¶](#appendix-C.1-26)

kid: 0x0000000000000001
ctr: 0x0000000000010000
header: 1a010000

[¶](#appendix-C.1-27)

kid: 0x0000000000000001
ctr: 0x0000000000ffffff
header: 1affffff

[¶](#appendix-C.1-28)

kid: 0x0000000000000001
ctr: 0x0000000001000000
header: 1b01000000

[¶](#appendix-C.1-29)

kid: 0x0000000000000001
ctr: 0x00000000ffffffff
header: 1bffffffff

[¶](#appendix-C.1-30)

kid: 0x0000000000000001
ctr: 0x0000000100000000
header: 1c0100000000

[¶](#appendix-C.1-31)

kid: 0x0000000000000001
ctr: 0x000000ffffffffff
header: 1cffffffffff

[¶](#appendix-C.1-32)

kid: 0x0000000000000001
ctr: 0x0000010000000000
header: 1d010000000000

[¶](#appendix-C.1-33)

kid: 0x0000000000000001
ctr: 0x0000ffffffffffff
header: 1dffffffffffff

[¶](#appendix-C.1-34)

kid: 0x0000000000000001
ctr: 0x0001000000000000
header: 1e01000000000000

[¶](#appendix-C.1-35)

kid: 0x0000000000000001
ctr: 0x00ffffffffffffff
header: 1effffffffffffff

[¶](#appendix-C.1-36)

kid: 0x0000000000000001
ctr: 0x0100000000000000
header: 1f0100000000000000

[¶](#appendix-C.1-37)

kid: 0x0000000000000001
ctr: 0xffffffffffffffff
header: 1fffffffffffffffff

[¶](#appendix-C.1-38)

kid: 0x00000000000000ff
ctr: 0x0000000000000000
header: 80ff

[¶](#appendix-C.1-39)

kid: 0x00000000000000ff
ctr: 0x0000000000000001
header: 81ff

[¶](#appendix-C.1-40)

kid: 0x00000000000000ff
ctr: 0x00000000000000ff
header: 88ffff

[¶](#appendix-C.1-41)

kid: 0x00000000000000ff
ctr: 0x0000000000000100
header: 89ff0100

[¶](#appendix-C.1-42)

kid: 0x00000000000000ff
ctr: 0x000000000000ffff
header: 89ffffff

[¶](#appendix-C.1-43)

kid: 0x00000000000000ff
ctr: 0x0000000000010000
header: 8aff010000

[¶](#appendix-C.1-44)

kid: 0x00000000000000ff
ctr: 0x0000000000ffffff
header: 8affffffff

[¶](#appendix-C.1-45)

kid: 0x00000000000000ff
ctr: 0x0000000001000000
header: 8bff01000000

[¶](#appendix-C.1-46)

kid: 0x00000000000000ff
ctr: 0x00000000ffffffff
header: 8bffffffffff

[¶](#appendix-C.1-47)

kid: 0x00000000000000ff
ctr: 0x0000000100000000
header: 8cff0100000000

[¶](#appendix-C.1-48)

kid: 0x00000000000000ff
ctr: 0x000000ffffffffff
header: 8cffffffffffff

[¶](#appendix-C.1-49)

kid: 0x00000000000000ff
ctr: 0x0000010000000000
header: 8dff010000000000

[¶](#appendix-C.1-50)

kid: 0x00000000000000ff
ctr: 0x0000ffffffffffff
header: 8dffffffffffffff

[¶](#appendix-C.1-51)

kid: 0x00000000000000ff
ctr: 0x0001000000000000
header: 8eff01000000000000

[¶](#appendix-C.1-52)

kid: 0x00000000000000ff
ctr: 0x00ffffffffffffff
header: 8effffffffffffffff

[¶](#appendix-C.1-53)

kid: 0x00000000000000ff
ctr: 0x0100000000000000
header: 8fff0100000000000000

[¶](#appendix-C.1-54)

kid: 0x00000000000000ff
ctr: 0xffffffffffffffff
header: 8fffffffffffffffffff

[¶](#appendix-C.1-55)

kid: 0x0000000000000100
ctr: 0x0000000000000000
header: 900100

[¶](#appendix-C.1-56)

kid: 0x0000000000000100
ctr: 0x0000000000000001
header: 910100

[¶](#appendix-C.1-57)

kid: 0x0000000000000100
ctr: 0x00000000000000ff
header: 980100ff

[¶](#appendix-C.1-58)

kid: 0x0000000000000100
ctr: 0x0000000000000100
header: 9901000100

[¶](#appendix-C.1-59)

kid: 0x0000000000000100
ctr: 0x000000000000ffff
header: 990100ffff

[¶](#appendix-C.1-60)

kid: 0x0000000000000100
ctr: 0x0000000000010000
header: 9a0100010000

[¶](#appendix-C.1-61)

kid: 0x0000000000000100
ctr: 0x0000000000ffffff
header: 9a0100ffffff

[¶](#appendix-C.1-62)

kid: 0x0000000000000100
ctr: 0x0000000001000000
header: 9b010001000000

[¶](#appendix-C.1-63)

kid: 0x0000000000000100
ctr: 0x00000000ffffffff
header: 9b0100ffffffff

[¶](#appendix-C.1-64)

kid: 0x0000000000000100
ctr: 0x0000000100000000
header: 9c01000100000000

[¶](#appendix-C.1-65)

kid: 0x0000000000000100
ctr: 0x000000ffffffffff
header: 9c0100ffffffffff

[¶](#appendix-C.1-66)

kid: 0x0000000000000100
ctr: 0x0000010000000000
header: 9d0100010000000000

[¶](#appendix-C.1-67)

kid: 0x0000000000000100
ctr: 0x0000ffffffffffff
header: 9d0100ffffffffffff

[¶](#appendix-C.1-68)

kid: 0x0000000000000100
ctr: 0x0001000000000000
header: 9e010001000000000000

[¶](#appendix-C.1-69)

kid: 0x0000000000000100
ctr: 0x00ffffffffffffff
header: 9e0100ffffffffffffff

[¶](#appendix-C.1-70)

kid: 0x0000000000000100
ctr: 0x0100000000000000
header: 9f01000100000000000000

[¶](#appendix-C.1-71)

kid: 0x0000000000000100
ctr: 0xffffffffffffffff
header: 9f0100ffffffffffffffff

[¶](#appendix-C.1-72)

kid: 0x000000000000ffff
ctr: 0x0000000000000000
header: 90ffff

[¶](#appendix-C.1-73)

kid: 0x000000000000ffff
ctr: 0x0000000000000001
header: 91ffff

[¶](#appendix-C.1-74)

kid: 0x000000000000ffff
ctr: 0x00000000000000ff
header: 98ffffff

[¶](#appendix-C.1-75)

kid: 0x000000000000ffff
ctr: 0x0000000000000100
header: 99ffff0100

[¶](#appendix-C.1-76)

kid: 0x000000000000ffff
ctr: 0x000000000000ffff
header: 99ffffffff

[¶](#appendix-C.1-77)

kid: 0x000000000000ffff
ctr: 0x0000000000010000
header: 9affff010000

[¶](#appendix-C.1-78)

kid: 0x000000000000ffff
ctr: 0x0000000000ffffff
header: 9affffffffff

[¶](#appendix-C.1-79)

kid: 0x000000000000ffff
ctr: 0x0000000001000000
header: 9bffff01000000

[¶](#appendix-C.1-80)

kid: 0x000000000000ffff
ctr: 0x00000000ffffffff
header: 9bffffffffffff

[¶](#appendix-C.1-81)

kid: 0x000000000000ffff
ctr: 0x0000000100000000
header: 9cffff0100000000

[¶](#appendix-C.1-82)

kid: 0x000000000000ffff
ctr: 0x000000ffffffffff
header: 9cffffffffffffff

[¶](#appendix-C.1-83)

kid: 0x000000000000ffff
ctr: 0x0000010000000000
header: 9dffff010000000000

[¶](#appendix-C.1-84)

kid: 0x000000000000ffff
ctr: 0x0000ffffffffffff
header: 9dffffffffffffffff

[¶](#appendix-C.1-85)

kid: 0x000000000000ffff
ctr: 0x0001000000000000
header: 9effff01000000000000

[¶](#appendix-C.1-86)

kid: 0x000000000000ffff
ctr: 0x00ffffffffffffff
header: 9effffffffffffffffff

[¶](#appendix-C.1-87)

kid: 0x000000000000ffff
ctr: 0x0100000000000000
header: 9fffff0100000000000000

[¶](#appendix-C.1-88)

kid: 0x000000000000ffff
ctr: 0xffffffffffffffff
header: 9fffffffffffffffffffff

[¶](#appendix-C.1-89)

kid: 0x0000000000010000
ctr: 0x0000000000000000
header: a0010000

[¶](#appendix-C.1-90)

kid: 0x0000000000010000
ctr: 0x0000000000000001
header: a1010000

[¶](#appendix-C.1-91)

kid: 0x0000000000010000
ctr: 0x00000000000000ff
header: a8010000ff

[¶](#appendix-C.1-92)

kid: 0x0000000000010000
ctr: 0x0000000000000100
header: a90100000100

[¶](#appendix-C.1-93)

kid: 0x0000000000010000
ctr: 0x000000000000ffff
header: a9010000ffff

[¶](#appendix-C.1-94)

kid: 0x0000000000010000
ctr: 0x0000000000010000
header: aa010000010000

[¶](#appendix-C.1-95)

kid: 0x0000000000010000
ctr: 0x0000000000ffffff
header: aa010000ffffff

[¶](#appendix-C.1-96)

kid: 0x0000000000010000
ctr: 0x0000000001000000
header: ab01000001000000

[¶](#appendix-C.1-97)

kid: 0x0000000000010000
ctr: 0x00000000ffffffff
header: ab010000ffffffff

[¶](#appendix-C.1-98)

kid: 0x0000000000010000
ctr: 0x0000000100000000
header: ac0100000100000000

[¶](#appendix-C.1-99)

kid: 0x0000000000010000
ctr: 0x000000ffffffffff
header: ac010000ffffffffff

[¶](#appendix-C.1-100)

kid: 0x0000000000010000
ctr: 0x0000010000000000
header: ad010000010000000000

[¶](#appendix-C.1-101)

kid: 0x0000000000010000
ctr: 0x0000ffffffffffff
header: ad010000ffffffffffff

[¶](#appendix-C.1-102)

kid: 0x0000000000010000
ctr: 0x0001000000000000
header: ae01000001000000000000

[¶](#appendix-C.1-103)

kid: 0x0000000000010000
ctr: 0x00ffffffffffffff
header: ae010000ffffffffffffff

[¶](#appendix-C.1-104)

kid: 0x0000000000010000
ctr: 0x0100000000000000
header: af0100000100000000000000

[¶](#appendix-C.1-105)

kid: 0x0000000000010000
ctr: 0xffffffffffffffff
header: af010000ffffffffffffffff

[¶](#appendix-C.1-106)

kid: 0x0000000000ffffff
ctr: 0x0000000000000000
header: a0ffffff

[¶](#appendix-C.1-107)

kid: 0x0000000000ffffff
ctr: 0x0000000000000001
header: a1ffffff

[¶](#appendix-C.1-108)

kid: 0x0000000000ffffff
ctr: 0x00000000000000ff
header: a8ffffffff

[¶](#appendix-C.1-109)

kid: 0x0000000000ffffff
ctr: 0x0000000000000100
header: a9ffffff0100

[¶](#appendix-C.1-110)

kid: 0x0000000000ffffff
ctr: 0x000000000000ffff
header: a9ffffffffff

[¶](#appendix-C.1-111)

kid: 0x0000000000ffffff
ctr: 0x0000000000010000
header: aaffffff010000

[¶](#appendix-C.1-112)

kid: 0x0000000000ffffff
ctr: 0x0000000000ffffff
header: aaffffffffffff

[¶](#appendix-C.1-113)

kid: 0x0000000000ffffff
ctr: 0x0000000001000000
header: abffffff01000000

[¶](#appendix-C.1-114)

kid: 0x0000000000ffffff
ctr: 0x00000000ffffffff
header: abffffffffffffff

[¶](#appendix-C.1-115)

kid: 0x0000000000ffffff
ctr: 0x0000000100000000
header: acffffff0100000000

[¶](#appendix-C.1-116)

kid: 0x0000000000ffffff
ctr: 0x000000ffffffffff
header: acffffffffffffffff

[¶](#appendix-C.1-117)

kid: 0x0000000000ffffff
ctr: 0x0000010000000000
header: adffffff010000000000

[¶](#appendix-C.1-118)

kid: 0x0000000000ffffff
ctr: 0x0000ffffffffffff
header: adffffffffffffffffff

[¶](#appendix-C.1-119)

kid: 0x0000000000ffffff
ctr: 0x0001000000000000
header: aeffffff01000000000000

[¶](#appendix-C.1-120)

kid: 0x0000000000ffffff
ctr: 0x00ffffffffffffff
header: aeffffffffffffffffffff

[¶](#appendix-C.1-121)

kid: 0x0000000000ffffff
ctr: 0x0100000000000000
header: afffffff0100000000000000

[¶](#appendix-C.1-122)

kid: 0x0000000000ffffff
ctr: 0xffffffffffffffff
header: afffffffffffffffffffffff

[¶](#appendix-C.1-123)

kid: 0x0000000001000000
ctr: 0x0000000000000000
header: b001000000

[¶](#appendix-C.1-124)

kid: 0x0000000001000000
ctr: 0x0000000000000001
header: b101000000

[¶](#appendix-C.1-125)

kid: 0x0000000001000000
ctr: 0x00000000000000ff
header: b801000000ff

[¶](#appendix-C.1-126)

kid: 0x0000000001000000
ctr: 0x0000000000000100
header: b9010000000100

[¶](#appendix-C.1-127)

kid: 0x0000000001000000
ctr: 0x000000000000ffff
header: b901000000ffff

[¶](#appendix-C.1-128)

kid: 0x0000000001000000
ctr: 0x0000000000010000
header: ba01000000010000

[¶](#appendix-C.1-129)

kid: 0x0000000001000000
ctr: 0x0000000000ffffff
header: ba01000000ffffff

[¶](#appendix-C.1-130)

kid: 0x0000000001000000
ctr: 0x0000000001000000
header: bb0100000001000000

[¶](#appendix-C.1-131)

kid: 0x0000000001000000
ctr: 0x00000000ffffffff
header: bb01000000ffffffff

[¶](#appendix-C.1-132)

kid: 0x0000000001000000
ctr: 0x0000000100000000
header: bc010000000100000000

[¶](#appendix-C.1-133)

kid: 0x0000000001000000
ctr: 0x000000ffffffffff
header: bc01000000ffffffffff

[¶](#appendix-C.1-134)

kid: 0x0000000001000000
ctr: 0x0000010000000000
header: bd01000000010000000000

[¶](#appendix-C.1-135)

kid: 0x0000000001000000
ctr: 0x0000ffffffffffff
header: bd01000000ffffffffffff

[¶](#appendix-C.1-136)

kid: 0x0000000001000000
ctr: 0x0001000000000000
header: be0100000001000000000000

[¶](#appendix-C.1-137)

kid: 0x0000000001000000
ctr: 0x00ffffffffffffff
header: be01000000ffffffffffffff

[¶](#appendix-C.1-138)

kid: 0x0000000001000000
ctr: 0x0100000000000000
header: bf010000000100000000000000

[¶](#appendix-C.1-139)

kid: 0x0000000001000000
ctr: 0xffffffffffffffff
header: bf01000000ffffffffffffffff

[¶](#appendix-C.1-140)

kid: 0x00000000ffffffff
ctr: 0x0000000000000000
header: b0ffffffff

[¶](#appendix-C.1-141)

kid: 0x00000000ffffffff
ctr: 0x0000000000000001
header: b1ffffffff

[¶](#appendix-C.1-142)

kid: 0x00000000ffffffff
ctr: 0x00000000000000ff
header: b8ffffffffff

[¶](#appendix-C.1-143)

kid: 0x00000000ffffffff
ctr: 0x0000000000000100
header: b9ffffffff0100

[¶](#appendix-C.1-144)

kid: 0x00000000ffffffff
ctr: 0x000000000000ffff
header: b9ffffffffffff

[¶](#appendix-C.1-145)

kid: 0x00000000ffffffff
ctr: 0x0000000000010000
header: baffffffff010000

[¶](#appendix-C.1-146)

kid: 0x00000000ffffffff
ctr: 0x0000000000ffffff
header: baffffffffffffff

[¶](#appendix-C.1-147)

kid: 0x00000000ffffffff
ctr: 0x0000000001000000
header: bbffffffff01000000

[¶](#appendix-C.1-148)

kid: 0x00000000ffffffff
ctr: 0x00000000ffffffff
header: bbffffffffffffffff

[¶](#appendix-C.1-149)

kid: 0x00000000ffffffff
ctr: 0x0000000100000000
header: bcffffffff0100000000

[¶](#appendix-C.1-150)

kid: 0x00000000ffffffff
ctr: 0x000000ffffffffff
header: bcffffffffffffffffff

[¶](#appendix-C.1-151)

kid: 0x00000000ffffffff
ctr: 0x0000010000000000
header: bdffffffff010000000000

[¶](#appendix-C.1-152)

kid: 0x00000000ffffffff
ctr: 0x0000ffffffffffff
header: bdffffffffffffffffffff

[¶](#appendix-C.1-153)

kid: 0x00000000ffffffff
ctr: 0x0001000000000000
header: beffffffff01000000000000

[¶](#appendix-C.1-154)

kid: 0x00000000ffffffff
ctr: 0x00ffffffffffffff
header: beffffffffffffffffffffff

[¶](#appendix-C.1-155)

kid: 0x00000000ffffffff
ctr: 0x0100000000000000
header: bfffffffff0100000000000000

[¶](#appendix-C.1-156)

kid: 0x00000000ffffffff
ctr: 0xffffffffffffffff
header: bfffffffffffffffffffffffff

[¶](#appendix-C.1-157)

kid: 0x0000000100000000
ctr: 0x0000000000000000
header: c00100000000

[¶](#appendix-C.1-158)

kid: 0x0000000100000000
ctr: 0x0000000000000001
header: c10100000000

[¶](#appendix-C.1-159)

kid: 0x0000000100000000
ctr: 0x00000000000000ff
header: c80100000000ff

[¶](#appendix-C.1-160)

kid: 0x0000000100000000
ctr: 0x0000000000000100
header: c901000000000100

[¶](#appendix-C.1-161)

kid: 0x0000000100000000
ctr: 0x000000000000ffff
header: c90100000000ffff

[¶](#appendix-C.1-162)

kid: 0x0000000100000000
ctr: 0x0000000000010000
header: ca0100000000010000

[¶](#appendix-C.1-163)

kid: 0x0000000100000000
ctr: 0x0000000000ffffff
header: ca0100000000ffffff

[¶](#appendix-C.1-164)

kid: 0x0000000100000000
ctr: 0x0000000001000000
header: cb010000000001000000

[¶](#appendix-C.1-165)

kid: 0x0000000100000000
ctr: 0x00000000ffffffff
header: cb0100000000ffffffff

[¶](#appendix-C.1-166)

kid: 0x0000000100000000
ctr: 0x0000000100000000
header: cc01000000000100000000

[¶](#appendix-C.1-167)

kid: 0x0000000100000000
ctr: 0x000000ffffffffff
header: cc0100000000ffffffffff

[¶](#appendix-C.1-168)

kid: 0x0000000100000000
ctr: 0x0000010000000000
header: cd0100000000010000000000

[¶](#appendix-C.1-169)

kid: 0x0000000100000000
ctr: 0x0000ffffffffffff
header: cd0100000000ffffffffffff

[¶](#appendix-C.1-170)

kid: 0x0000000100000000
ctr: 0x0001000000000000
header: ce010000000001000000000000

[¶](#appendix-C.1-171)

kid: 0x0000000100000000
ctr: 0x00ffffffffffffff
header: ce0100000000ffffffffffffff

[¶](#appendix-C.1-172)

kid: 0x0000000100000000
ctr: 0x0100000000000000
header: cf01000000000100000000000000

[¶](#appendix-C.1-173)

kid: 0x0000000100000000
ctr: 0xffffffffffffffff
header: cf0100000000ffffffffffffffff

[¶](#appendix-C.1-174)

kid: 0x000000ffffffffff
ctr: 0x0000000000000000
header: c0ffffffffff

[¶](#appendix-C.1-175)

kid: 0x000000ffffffffff
ctr: 0x0000000000000001
header: c1ffffffffff

[¶](#appendix-C.1-176)

kid: 0x000000ffffffffff
ctr: 0x00000000000000ff
header: c8ffffffffffff

[¶](#appendix-C.1-177)

kid: 0x000000ffffffffff
ctr: 0x0000000000000100
header: c9ffffffffff0100

[¶](#appendix-C.1-178)

kid: 0x000000ffffffffff
ctr: 0x000000000000ffff
header: c9ffffffffffffff

[¶](#appendix-C.1-179)

kid: 0x000000ffffffffff
ctr: 0x0000000000010000
header: caffffffffff010000

[¶](#appendix-C.1-180)

kid: 0x000000ffffffffff
ctr: 0x0000000000ffffff
header: caffffffffffffffff

[¶](#appendix-C.1-181)

kid: 0x000000ffffffffff
ctr: 0x0000000001000000
header: cbffffffffff01000000

[¶](#appendix-C.1-182)

kid: 0x000000ffffffffff
ctr: 0x00000000ffffffff
header: cbffffffffffffffffff

[¶](#appendix-C.1-183)

kid: 0x000000ffffffffff
ctr: 0x0000000100000000
header: ccffffffffff0100000000

[¶](#appendix-C.1-184)

kid: 0x000000ffffffffff
ctr: 0x000000ffffffffff
header: ccffffffffffffffffffff

[¶](#appendix-C.1-185)

kid: 0x000000ffffffffff
ctr: 0x0000010000000000
header: cdffffffffff010000000000

[¶](#appendix-C.1-186)

kid: 0x000000ffffffffff
ctr: 0x0000ffffffffffff
header: cdffffffffffffffffffffff

[¶](#appendix-C.1-187)

kid: 0x000000ffffffffff
ctr: 0x0001000000000000
header: ceffffffffff01000000000000

[¶](#appendix-C.1-188)

kid: 0x000000ffffffffff
ctr: 0x00ffffffffffffff
header: ceffffffffffffffffffffffff

[¶](#appendix-C.1-189)

kid: 0x000000ffffffffff
ctr: 0x0100000000000000
header: cfffffffffff0100000000000000

[¶](#appendix-C.1-190)

kid: 0x000000ffffffffff
ctr: 0xffffffffffffffff
header: cfffffffffffffffffffffffffff

[¶](#appendix-C.1-191)

kid: 0x0000010000000000
ctr: 0x0000000000000000
header: d0010000000000

[¶](#appendix-C.1-192)

kid: 0x0000010000000000
ctr: 0x0000000000000001
header: d1010000000000

[¶](#appendix-C.1-193)

kid: 0x0000010000000000
ctr: 0x00000000000000ff
header: d8010000000000ff

[¶](#appendix-C.1-194)

kid: 0x0000010000000000
ctr: 0x0000000000000100
header: d90100000000000100

[¶](#appendix-C.1-195)

kid: 0x0000010000000000
ctr: 0x000000000000ffff
header: d9010000000000ffff

[¶](#appendix-C.1-196)

kid: 0x0000010000000000
ctr: 0x0000000000010000
header: da010000000000010000

[¶](#appendix-C.1-197)

kid: 0x0000010000000000
ctr: 0x0000000000ffffff
header: da010000000000ffffff

[¶](#appendix-C.1-198)

kid: 0x0000010000000000
ctr: 0x0000000001000000
header: db01000000000001000000

[¶](#appendix-C.1-199)

kid: 0x0000010000000000
ctr: 0x00000000ffffffff
header: db010000000000ffffffff

[¶](#appendix-C.1-200)

kid: 0x0000010000000000
ctr: 0x0000000100000000
header: dc0100000000000100000000

[¶](#appendix-C.1-201)

kid: 0x0000010000000000
ctr: 0x000000ffffffffff
header: dc010000000000ffffffffff

[¶](#appendix-C.1-202)

kid: 0x0000010000000000
ctr: 0x0000010000000000
header: dd010000000000010000000000

[¶](#appendix-C.1-203)

kid: 0x0000010000000000
ctr: 0x0000ffffffffffff
header: dd010000000000ffffffffffff

[¶](#appendix-C.1-204)

kid: 0x0000010000000000
ctr: 0x0001000000000000
header: de01000000000001000000000000

[¶](#appendix-C.1-205)

kid: 0x0000010000000000
ctr: 0x00ffffffffffffff
header: de010000000000ffffffffffffff

[¶](#appendix-C.1-206)

kid: 0x0000010000000000
ctr: 0x0100000000000000
header: df0100000000000100000000000000

[¶](#appendix-C.1-207)

kid: 0x0000010000000000
ctr: 0xffffffffffffffff
header: df010000000000ffffffffffffffff

[¶](#appendix-C.1-208)

kid: 0x0000ffffffffffff
ctr: 0x0000000000000000
header: d0ffffffffffff

[¶](#appendix-C.1-209)

kid: 0x0000ffffffffffff
ctr: 0x0000000000000001
header: d1ffffffffffff

[¶](#appendix-C.1-210)

kid: 0x0000ffffffffffff
ctr: 0x00000000000000ff
header: d8ffffffffffffff

[¶](#appendix-C.1-211)

kid: 0x0000ffffffffffff
ctr: 0x0000000000000100
header: d9ffffffffffff0100

[¶](#appendix-C.1-212)

kid: 0x0000ffffffffffff
ctr: 0x000000000000ffff
header: d9ffffffffffffffff

[¶](#appendix-C.1-213)

kid: 0x0000ffffffffffff
ctr: 0x0000000000010000
header: daffffffffffff010000

[¶](#appendix-C.1-214)

kid: 0x0000ffffffffffff
ctr: 0x0000000000ffffff
header: daffffffffffffffffff

[¶](#appendix-C.1-215)

kid: 0x0000ffffffffffff
ctr: 0x0000000001000000
header: dbffffffffffff01000000

[¶](#appendix-C.1-216)

kid: 0x0000ffffffffffff
ctr: 0x00000000ffffffff
header: dbffffffffffffffffffff

[¶](#appendix-C.1-217)

kid: 0x0000ffffffffffff
ctr: 0x0000000100000000
header: dcffffffffffff0100000000

[¶](#appendix-C.1-218)

kid: 0x0000ffffffffffff
ctr: 0x000000ffffffffff
header: dcffffffffffffffffffffff

[¶](#appendix-C.1-219)

kid: 0x0000ffffffffffff
ctr: 0x0000010000000000
header: ddffffffffffff010000000000

[¶](#appendix-C.1-220)

kid: 0x0000ffffffffffff
ctr: 0x0000ffffffffffff
header: ddffffffffffffffffffffffff

[¶](#appendix-C.1-221)

kid: 0x0000ffffffffffff
ctr: 0x0001000000000000
header: deffffffffffff01000000000000

[¶](#appendix-C.1-222)

kid: 0x0000ffffffffffff
ctr: 0x00ffffffffffffff
header: deffffffffffffffffffffffffff

[¶](#appendix-C.1-223)

kid: 0x0000ffffffffffff
ctr: 0x0100000000000000
header: dfffffffffffff0100000000000000

[¶](#appendix-C.1-224)

kid: 0x0000ffffffffffff
ctr: 0xffffffffffffffff
header: dfffffffffffffffffffffffffffff

[¶](#appendix-C.1-225)

kid: 0x0001000000000000
ctr: 0x0000000000000000
header: e001000000000000

[¶](#appendix-C.1-226)

kid: 0x0001000000000000
ctr: 0x0000000000000001
header: e101000000000000

[¶](#appendix-C.1-227)

kid: 0x0001000000000000
ctr: 0x00000000000000ff
header: e801000000000000ff

[¶](#appendix-C.1-228)

kid: 0x0001000000000000
ctr: 0x0000000000000100
header: e9010000000000000100

[¶](#appendix-C.1-229)

kid: 0x0001000000000000
ctr: 0x000000000000ffff
header: e901000000000000ffff

[¶](#appendix-C.1-230)

kid: 0x0001000000000000
ctr: 0x0000000000010000
header: ea01000000000000010000

[¶](#appendix-C.1-231)

kid: 0x0001000000000000
ctr: 0x0000000000ffffff
header: ea01000000000000ffffff

[¶](#appendix-C.1-232)

kid: 0x0001000000000000
ctr: 0x0000000001000000
header: eb0100000000000001000000

[¶](#appendix-C.1-233)

kid: 0x0001000000000000
ctr: 0x00000000ffffffff
header: eb01000000000000ffffffff

[¶](#appendix-C.1-234)

kid: 0x0001000000000000
ctr: 0x0000000100000000
header: ec010000000000000100000000

[¶](#appendix-C.1-235)

kid: 0x0001000000000000
ctr: 0x000000ffffffffff
header: ec01000000000000ffffffffff

[¶](#appendix-C.1-236)

kid: 0x0001000000000000
ctr: 0x0000010000000000
header: ed01000000000000010000000000

[¶](#appendix-C.1-237)

kid: 0x0001000000000000
ctr: 0x0000ffffffffffff
header: ed01000000000000ffffffffffff

[¶](#appendix-C.1-238)

kid: 0x0001000000000000
ctr: 0x0001000000000000
header: ee0100000000000001000000000000

[¶](#appendix-C.1-239)

kid: 0x0001000000000000
ctr: 0x00ffffffffffffff
header: ee01000000000000ffffffffffffff

[¶](#appendix-C.1-240)

kid: 0x0001000000000000
ctr: 0x0100000000000000
header: ef010000000000000100000000000000

[¶](#appendix-C.1-241)

kid: 0x0001000000000000
ctr: 0xffffffffffffffff
header: ef01000000000000ffffffffffffffff

[¶](#appendix-C.1-242)

kid: 0x00ffffffffffffff
ctr: 0x0000000000000000
header: e0ffffffffffffff

[¶](#appendix-C.1-243)

kid: 0x00ffffffffffffff
ctr: 0x0000000000000001
header: e1ffffffffffffff

[¶](#appendix-C.1-244)

kid: 0x00ffffffffffffff
ctr: 0x00000000000000ff
header: e8ffffffffffffffff

[¶](#appendix-C.1-245)

kid: 0x00ffffffffffffff
ctr: 0x0000000000000100
header: e9ffffffffffffff0100

[¶](#appendix-C.1-246)

kid: 0x00ffffffffffffff
ctr: 0x000000000000ffff
header: e9ffffffffffffffffff

[¶](#appendix-C.1-247)

kid: 0x00ffffffffffffff
ctr: 0x0000000000010000
header: eaffffffffffffff010000

[¶](#appendix-C.1-248)

kid: 0x00ffffffffffffff
ctr: 0x0000000000ffffff
header: eaffffffffffffffffffff

[¶](#appendix-C.1-249)

kid: 0x00ffffffffffffff
ctr: 0x0000000001000000
header: ebffffffffffffff01000000

[¶](#appendix-C.1-250)

kid: 0x00ffffffffffffff
ctr: 0x00000000ffffffff
header: ebffffffffffffffffffffff

[¶](#appendix-C.1-251)

kid: 0x00ffffffffffffff
ctr: 0x0000000100000000
header: ecffffffffffffff0100000000

[¶](#appendix-C.1-252)

kid: 0x00ffffffffffffff
ctr: 0x000000ffffffffff
header: ecffffffffffffffffffffffff

[¶](#appendix-C.1-253)

kid: 0x00ffffffffffffff
ctr: 0x0000010000000000
header: edffffffffffffff010000000000

[¶](#appendix-C.1-254)

kid: 0x00ffffffffffffff
ctr: 0x0000ffffffffffff
header: edffffffffffffffffffffffffff

[¶](#appendix-C.1-255)

kid: 0x00ffffffffffffff
ctr: 0x0001000000000000
header: eeffffffffffffff01000000000000

[¶](#appendix-C.1-256)

kid: 0x00ffffffffffffff
ctr: 0x00ffffffffffffff
header: eeffffffffffffffffffffffffffff

[¶](#appendix-C.1-257)

kid: 0x00ffffffffffffff
ctr: 0x0100000000000000
header: efffffffffffffff0100000000000000

[¶](#appendix-C.1-258)

kid: 0x00ffffffffffffff
ctr: 0xffffffffffffffff
header: efffffffffffffffffffffffffffffff

[¶](#appendix-C.1-259)

kid: 0x0100000000000000
ctr: 0x0000000000000000
header: f00100000000000000

[¶](#appendix-C.1-260)

kid: 0x0100000000000000
ctr: 0x0000000000000001
header: f10100000000000000

[¶](#appendix-C.1-261)

kid: 0x0100000000000000
ctr: 0x00000000000000ff
header: f80100000000000000ff

[¶](#appendix-C.1-262)

kid: 0x0100000000000000
ctr: 0x0000000000000100
header: f901000000000000000100

[¶](#appendix-C.1-263)

kid: 0x0100000000000000
ctr: 0x000000000000ffff
header: f90100000000000000ffff

[¶](#appendix-C.1-264)

kid: 0x0100000000000000
ctr: 0x0000000000010000
header: fa0100000000000000010000

[¶](#appendix-C.1-265)

kid: 0x0100000000000000
ctr: 0x0000000000ffffff
header: fa0100000000000000ffffff

[¶](#appendix-C.1-266)

kid: 0x0100000000000000
ctr: 0x0000000001000000
header: fb010000000000000001000000

[¶](#appendix-C.1-267)

kid: 0x0100000000000000
ctr: 0x00000000ffffffff
header: fb0100000000000000ffffffff

[¶](#appendix-C.1-268)

kid: 0x0100000000000000
ctr: 0x0000000100000000
header: fc01000000000000000100000000

[¶](#appendix-C.1-269)

kid: 0x0100000000000000
ctr: 0x000000ffffffffff
header: fc0100000000000000ffffffffff

[¶](#appendix-C.1-270)

kid: 0x0100000000000000
ctr: 0x0000010000000000
header: fd0100000000000000010000000000

[¶](#appendix-C.1-271)

kid: 0x0100000000000000
ctr: 0x0000ffffffffffff
header: fd0100000000000000ffffffffffff

[¶](#appendix-C.1-272)

kid: 0x0100000000000000
ctr: 0x0001000000000000
header: fe010000000000000001000000000000

[¶](#appendix-C.1-273)

kid: 0x0100000000000000
ctr: 0x00ffffffffffffff
header: fe0100000000000000ffffffffffffff

[¶](#appendix-C.1-274)

```
kid: 0x0100000000000000
ctr: 0x0100000000000000
header: ff010000000000000001000000000000
        00
```
[¶](#appendix-C.1-275)

```
kid: 0x0100000000000000
ctr: 0xffffffffffffffff
header: ff0100000000000000ffffffffffffff
        ff
```
[¶](#appendix-C.1-276)

kid: 0xffffffffffffffff
ctr: 0x0000000000000000
header: f0ffffffffffffffff

[¶](#appendix-C.1-277)

kid: 0xffffffffffffffff
ctr: 0x0000000000000001
header: f1ffffffffffffffff

[¶](#appendix-C.1-278)

kid: 0xffffffffffffffff
ctr: 0x00000000000000ff
header: f8ffffffffffffffffff

[¶](#appendix-C.1-279)

kid: 0xffffffffffffffff
ctr: 0x0000000000000100
header: f9ffffffffffffffff0100

[¶](#appendix-C.1-280)

kid: 0xffffffffffffffff
ctr: 0x000000000000ffff
header: f9ffffffffffffffffffff

[¶](#appendix-C.1-281)

kid: 0xffffffffffffffff
ctr: 0x0000000000010000
header: faffffffffffffffff010000

[¶](#appendix-C.1-282)

kid: 0xffffffffffffffff
ctr: 0x0000000000ffffff
header: faffffffffffffffffffffff

[¶](#appendix-C.1-283)

kid: 0xffffffffffffffff
ctr: 0x0000000001000000
header: fbffffffffffffffff01000000

[¶](#appendix-C.1-284)

kid: 0xffffffffffffffff
ctr: 0x00000000ffffffff
header: fbffffffffffffffffffffffff

[¶](#appendix-C.1-285)

kid: 0xffffffffffffffff
ctr: 0x0000000100000000
header: fcffffffffffffffff0100000000

[¶](#appendix-C.1-286)

kid: 0xffffffffffffffff
ctr: 0x000000ffffffffff
header: fcffffffffffffffffffffffffff

[¶](#appendix-C.1-287)

kid: 0xffffffffffffffff
ctr: 0x0000010000000000
header: fdffffffffffffffff010000000000

[¶](#appendix-C.1-288)

kid: 0xffffffffffffffff
ctr: 0x0000ffffffffffff
header: fdffffffffffffffffffffffffffff

[¶](#appendix-C.1-289)

kid: 0xffffffffffffffff
ctr: 0x0001000000000000
header: feffffffffffffffff01000000000000

[¶](#appendix-C.1-290)

kid: 0xffffffffffffffff
ctr: 0x00ffffffffffffff
header: feffffffffffffffffffffffffffffff

[¶](#appendix-C.1-291)

```
kid: 0xffffffffffffffff
ctr: 0x0100000000000000
header: ffffffffffffffffff01000000000000
        00
```
[¶](#appendix-C.1-292)

```
kid: 0xffffffffffffffff
ctr: 0xffffffffffffffff
header: ffffffffffffffffffffffffffffffff
        ff
```
[¶](#appendix-C.1-293)

### 
[C.2.](#appendix-C.2) [AEAD Encryption/Dec](#name-aead-encryption-decryption-)
        

For each case, we provide:[¶](#appendix-C.2-1)

- 
            `cipher_` : The index of the cipher suite in use (seesuite [Section 8.1](#sframe-cipher-suites) )[¶](#appendix-C.2-2.1.1)
- 
            `key` : The`key` input to encryption/dec ryption [¶](#appendix-C.2-2.2.1)
- 
            `enc_` : The encryption subkey produced by thekey `derive_` algorithmsubkeys() [¶](#appendix-C.2-2.3.1)
- 
            `auth_` : The encryption subkey produced by thekey `derive_` algorithmsubkeys() [¶](#appendix-C.2-2.4.1)
- 
            `nonce` : The`nonce` input to encryption/dec ryption [¶](#appendix-C.2-2.5.1)
- 
            `aad` : The`aad` input to encryption/dec ryption [¶](#appendix-C.2-2.6.1)
- 
            `pt` : The plaintext[¶](#appendix-C.2-2.7.1)
- 
            `ct` : The ciphertext[¶](#appendix-C.2-2.8.1)

An implementation should verify that the following are true, where
`AEAD` and `AEAD` are as defined in [Section 4.5.1](#aes-ctr-with-sha2):[¶](#appendix-C.2-3)

The other values in the test vector are intermediate values provided to
facilitate debugging of test failures.[¶](#appendix-C.2-5)

```
cipher_suite: 0x0001
key: 000102030405060708090a0b0c0d0e0f
     101112131415161718191a1b1c1d1e1f
     202122232425262728292a2b2c2d2e2f
enc_key: 000102030405060708090a0b0c0d0e0f
auth_key: 101112131415161718191a1b1c1d1e1f
          202122232425262728292a2b2c2d2e2f
nonce: 101112131415161718191a1b
aad: 4945544620534672616d65205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 6339af04ada1d064688a442b8dc69d5b
    6bfa40f4bef0583e8081069cc60705
```
[¶](#appendix-C.2-6)

```
cipher_suite: 0x0002
key: 000102030405060708090a0b0c0d0e0f
     101112131415161718191a1b1c1d1e1f
     202122232425262728292a2b2c2d2e2f
enc_key: 000102030405060708090a0b0c0d0e0f
auth_key: 101112131415161718191a1b1c1d1e1f
          202122232425262728292a2b2c2d2e2f
nonce: 101112131415161718191a1b
aad: 4945544620534672616d65205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 6339af04ada1d064688a442b8dc69d5b
    6bfa40f4be6e93b7da076927bb
```
[¶](#appendix-C.2-7)

```
cipher_suite: 0x0003
key: 000102030405060708090a0b0c0d0e0f
     101112131415161718191a1b1c1d1e1f
     202122232425262728292a2b2c2d2e2f
enc_key: 000102030405060708090a0b0c0d0e0f
auth_key: 101112131415161718191a1b1c1d1e1f
          202122232425262728292a2b2c2d2e2f
nonce: 101112131415161718191a1b
aad: 4945544620534672616d65205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 6339af04ada1d064688a442b8dc69d5b
    6bfa40f4be09480509
```
[¶](#appendix-C.2-8)

### 
[C.3.](#appendix-C.3) [SFrame Encryption/Dec](#name-sframe-encryption-decryptio)
        

For each case, we provide:[¶](#appendix-C.3-1)

- 
            `cipher_` : The index of the cipher suite in use (seesuite [Section 8.1](#sframe-cipher-suites) )[¶](#appendix-C.3-2.1.1)
- 
            `kid` : A KID value[¶](#appendix-C.3-2.2.1)
- 
            `ctr` : A CTR value[¶](#appendix-C.3-2.3.1)
- 
            `base_` : Thekey `base_` input to thekey `derive_` algorithmkey_ salt [¶](#appendix-C.3-2.4.1)
- 
            `sframe_` : The label used to derivekey_ label `sframe_` in thekey `derive_` algorithmkey_ salt [¶](#appendix-C.3-2.5.1)
- 
            `sframe_` : The label used to derivesalt_ label `sframe_` in thesalt `derive_` algorithmkey_ salt [¶](#appendix-C.3-2.6.1)
- 
            `sframe_` : Thesecret `sframe_` variable in thesecret `derive_` algorithmkey_ salt [¶](#appendix-C.3-2.7.1)
- 
            `sframe_` : Thekey `sframe_` value produced by thekey `derive_` algorithmkey_ salt [¶](#appendix-C.3-2.8.1)
- 
            `sframe_` : Thesalt `sframe_` value produced by thesalt `derive_` algorithmkey_ salt [¶](#appendix-C.3-2.9.1)
- 
            `metadata` : The`metadata` input to the SFrame`encrypt` algorithm[¶](#appendix-C.3-2.10.1)
- 
            `pt` : The plaintext[¶](#appendix-C.3-2.11.1)
- 
            `ct` : The SFrame ciphertext[¶](#appendix-C.3-2.12.1)

An implementation should verify that the following are true, where
`encrypt` and `decrypt` are as defined in [Section 4.4](#encryption-schema), using an SFrame
context initialized with `base_` assigned to `kid`:[¶](#appendix-C.3-3)

The other values in the test vector are intermediate values provided to
facilitate debugging of test failures.[¶](#appendix-C.3-5)

```
cipher_suite: 0x0001
kid: 0x0000000000000123
ctr: 0x0000000000004567
base_key: 000102030405060708090a0b0c0d0e0f
sframe_key_label: 534672616d6520312e30205365637265
                  74206b65792000000000000001230001
sframe_salt_label: 534672616d6520312e30205365637265
                   742073616c7420000000000000012300
                   01
sframe_secret: d926952ca8b7ec4a95941d1ada3a5203
               ceff8cceee34f574d23909eb314c40c0
sframe_key: 3f7d9a7c83ae8e1c8a11ae695ab59314
            b367e359fadac7b9c46b2bc6f81f46e1
            6b96f0811868d59402b7e870102720b3
sframe_salt: 50b29329a04dc0f184ac3168
metadata: 4945544620534672616d65205747
nonce: 50b29329a04dc0f184ac740f
aad: 99012345674945544620534672616d65
     205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 9901234567449408b6f490086165b9d6
    f62b24ae1a59a56486b4ae8ed036b889
    12e24f11
```
[¶](#appendix-C.3-6)

```
cipher_suite: 0x0002
kid: 0x0000000000000123
ctr: 0x0000000000004567
base_key: 000102030405060708090a0b0c0d0e0f
sframe_key_label: 534672616d6520312e30205365637265
                  74206b65792000000000000001230002
sframe_salt_label: 534672616d6520312e30205365637265
                   742073616c7420000000000000012300
                   02
sframe_secret: d926952ca8b7ec4a95941d1ada3a5203
               ceff8cceee34f574d23909eb314c40c0
sframe_key: e2ec5c797540310483b16bf6e7a570d2
            a27d192fe869c7ccd8584a8d9dab9154
            9fbe553f5113461ec6aa83bf3865553e
sframe_salt: e68ac8dd3d02fbcd368c5577
metadata: 4945544620534672616d65205747
nonce: e68ac8dd3d02fbcd368c1010
aad: 99012345674945544620534672616d65
     205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 99012345673f31438db4d09434e43afa
    0f8a2f00867a2be085046a9f5cb4f101
    d607
```
[¶](#appendix-C.3-7)

```
cipher_suite: 0x0003
kid: 0x0000000000000123
ctr: 0x0000000000004567
base_key: 000102030405060708090a0b0c0d0e0f
sframe_key_label: 534672616d6520312e30205365637265
                  74206b65792000000000000001230003
sframe_salt_label: 534672616d6520312e30205365637265
                   742073616c7420000000000000012300
                   03
sframe_secret: d926952ca8b7ec4a95941d1ada3a5203
               ceff8cceee34f574d23909eb314c40c0
sframe_key: 2c5703089cbb8c583475e4fc461d97d1
            8809df79b6d550f78eb6d50ffa80d892
            11d57909934f46f5405e38cd583c69fe
sframe_salt: 38c16e4f5159700c00c7f350
metadata: 4945544620534672616d65205747
nonce: 38c16e4f5159700c00c7b637
aad: 99012345674945544620534672616d65
     205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 990123456717fc8af28a5a695afcfc6c
    8df6358a17e26b2fcb3bae32e443
```
[¶](#appendix-C.3-8)

```
cipher_suite: 0x0004
kid: 0x0000000000000123
ctr: 0x0000000000004567
base_key: 000102030405060708090a0b0c0d0e0f
sframe_key_label: 534672616d6520312e30205365637265
                  74206b65792000000000000001230004
sframe_salt_label: 534672616d6520312e30205365637265
                   742073616c7420000000000000012300
                   04
sframe_secret: d926952ca8b7ec4a95941d1ada3a5203
               ceff8cceee34f574d23909eb314c40c0
sframe_key: d34f547f4ca4f9a7447006fe7fcbf768
sframe_salt: 75234edefe07819026751816
metadata: 4945544620534672616d65205747
nonce: 75234edefe07819026755d71
aad: 99012345674945544620534672616d65
     205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 9901234567b7412c2513a1b66dbb4884
    1bbaf17f598751176ad847681a69c6d0
    b091c07018ce4adb34eb
```
[¶](#appendix-C.3-9)

```
cipher_suite: 0x0005
kid: 0x0000000000000123
ctr: 0x0000000000004567
base_key: 000102030405060708090a0b0c0d0e0f
sframe_key_label: 534672616d6520312e30205365637265
                  74206b65792000000000000001230005
sframe_salt_label: 534672616d6520312e30205365637265
                   742073616c7420000000000000012300
                   05
sframe_secret: 0fc3ea6de6aac97a35f194cf9bed94d4
               b5230f1cb45a785c9fe5dce9c188938a
               b6ba005bc4c0a19181599e9d1bcf7b74
               aca48b60bf5e254e546d809313e083a3
sframe_key: d3e27b0d4a5ae9e55df01a70e6d4d28d
            969b246e2936f4b7a5d9b494da6b9633
sframe_salt: 84991c167b8cd23c93708ec7
metadata: 4945544620534672616d65205747
nonce: 84991c167b8cd23c9370cba0
aad: 99012345674945544620534672616d65
     205747
pt: 64726166742d696574662d736672616d
    652d656e63
ct: 990123456794f509d36e9beacb0e261d
    99c7d1e972f1fed787d4049f17ca2135
    3c1cc24d56ceabced279
```
[¶](#appendix-C.3-10)

## 
[Acknowledgements](#name-acknowledgements)
      

The authors wish to specially thank Dr. Alex Gouaillard as one of the early
contributors to the document. His passion and energy were key to the design and
development of SFrame.[¶](#appendix-D-1)

## 
[Contributors](#name-contributors)
      

        [frederic.jacobs](mailto:frederic.jacobs@apple.com)

[mulmarta@amazon](mailto:mulmarta@amazon.com)

[snandaku@cisco](mailto:snandaku@cisco.com)

[trigaux@cisco](mailto:trigaux@cisco.com)

[ietf@raphaelrobert](mailto:ietf@raphaelrobert.com)
