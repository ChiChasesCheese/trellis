---
title: 'RFC 9309: Robots Exclusion Protocol | RFC Editor'
source: https://www.rfc-editor.org/rfc/rfc9309
author: M Koster; G Illyes; H Zeller; L Sassman
published: '2022-09-09'
site: rfc-editor.org
clipped: '2026-09-20'
---

# RFC 9309: Robots Exclusion Protocol | RFC Editor

- [Home](/)
- **RFC 9309**

# RFC 9309: Robots Exclusion Protocol

- M. Koster,
- G. Illyes,
- H. Zeller,
- L. Sassman

## [Abstract](#abstract)

 This document specifies and extends the "Robots Exclusion Protocol"
          method originally defined by Martijn Koster in 1994 for service owners
          to control how content served by their services may be accessed, if at
          all, by automatic clients known as crawlers. Specifically, it adds
          definition language for the protocol, instructions for handling
          errors, and instructions for caching.[¶](#section-abstract-1)

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
            [https://](/info/rfc9309).[¶](#section-boilerplate.1-3)

## 
[Copyright Notice](#name-copyright-notice)
        

            Copyright (c) 2022 IETF Trust and the persons identified as the
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
      

 This document applies to services that provide resources that clients
          can access through URIs as defined in [[RFC3986](#RFC3986)]. For example,
          in the context of HTTP, a browser is a client that displays the content of a
          web page.[¶](#section-1-1)

 Crawlers are automated clients. Search engines, for instance, have crawlers to
          recursively traverse links for indexing as defined in
          [[RFC8288](#RFC8288)].[¶](#section-1-2)

 It may be inconvenient for service owners if crawlers visit the entirety of
          their URI space. This document specifies the rules originally defined by
          the "Robots Exclusion Protocol" [[ROBOTSTXT](#ROBOTSTXT)] that crawlers
          are requested to honor when accessing URIs.[¶](#section-1-3)

 These rules are not a form of access authorization.[¶](#section-1-4)

### 
[1.1.](#section-1.1) [Requirements Language](#name-requirements-language)
        

The key words "MUST", "MUST NOT",
        "REQUIRED", "SHALL",
        "SHALL NOT", "SHOULD",
        "SHOULD NOT",
        "RECOMMENDED", "NOT RECOMMENDED",
        "MAY", and "OPTIONAL" in this document
        are to be interpreted as described in BCP 14
        [[RFC2119](#RFC2119)] [[RFC8174](#RFC8174)] when, and only
        when, they appear in all capitals, as shown here.[¶](#section-1.1-1)

## 
[2.](#section-2) [Specification](#name-specification)
      

### 
[2.1.](#section-2.1) [Protocol Definition](#name-protocol-definition)
        

 The protocol language consists of rule(s) and group(s) that the service
            makes available in a file named "robots[Section 2.3](#access-method):[¶](#section-2.1-1)

- Rule:
-  A line with a key-value pair that defines how a
                crawler may access URIs. See
                [Section 2.2.2](#the-allow-and-disallow-lines) .[¶](#section-2.1-2.2)
- Group:
-  One or more user-agent lines that are followed by
                one or more rules. The group is terminated by a user-agent line
                or end of file. See [Section 2.2.1](#the-user-agent-line) .
                The last group may have no rules, which means it implicitly
                allows everything.[¶](#section-2.1-2.4)

### 
[2.2.](#section-2.2) [Formal Syntax](#name-formal-syntax)
        

 Below is an Augmented Backus-Naur Form (ABNF) description, as described
            in [[RFC5234](#RFC5234)].[¶](#section-2.2-1)

```
 robotstxt = *(group / emptyline)
 group = startgroupline                ; We start with a user-agent
                                       ; line
        *(startgroupline / emptyline)  ; ... and possibly more
                                       ; user-agent lines
        *(rule / emptyline)            ; followed by rules relevant
                                       ; for the preceding
                                       ; user-agent lines
 startgroupline = *WS "user-agent" *WS ":" *WS product-token EOL
 rule = *WS ("allow" / "disallow") *WS ":"
       *WS (path-pattern / empty-pattern) EOL
 ; parser implementors: define additional lines you need (for
 ; example, Sitemaps).
 product-token = identifier / "*"
 path-pattern = "/" *UTF8-char-noctl ; valid URI path pattern
 empty-pattern = *WS
 identifier = 1*(%x2D / %x41-5A / %x5F / %x61-7A)
 comment = "#" *(UTF8-char-noctl / WS / "#")
 emptyline = EOL
 EOL = *WS [comment] NL ; end-of-line may have
                        ; optional trailing comment
 NL = %x0D / %x0A / %x0D.0A
 WS = %x20 / %x09
 ; UTF8 derived from RFC 3629, but excluding control characters
 UTF8-char-noctl = UTF8-1-noctl / UTF8-2 / UTF8-3 / UTF8-4
 UTF8-1-noctl = %x21 / %x22 / %x24-7F ; excluding control, space, "#"
 UTF8-2 = %xC2-DF UTF8-tail
 UTF8-3 = %xE0 %xA0-BF UTF8-tail / %xE1-EC 2UTF8-tail /
          %xED %x80-9F UTF8-tail / %xEE-EF 2UTF8-tail
 UTF8-4 = %xF0 %x90-BF 2UTF8-tail / %xF1-F3 3UTF8-tail /
          %xF4 %x80-8F 2UTF8-tail
 UTF8-tail = %x80-BF
```
[¶](#section-2.2-2)

#### 
[2.2.1.](#section-2.2.1) [The User-Agent Line](#name-the-user-agent-line)
          

 Crawlers set their own name, which is called a product token, to find
              relevant groups. The product token MUST contain only
              uppercase and lowercase letters ("a-z" and "A-Z"),
              underscores ("_"), and hyphens ("-").
              The product token SHOULD
              be a substring of the identification string that the crawler sends to
              the service. For example, in the case of HTTP
              [[RFC9110](#RFC9110)], the product token
              SHOULD be a substring in the User-Agent header.
              The identification string SHOULD describe the purpose of
              the crawler. Here's an example of a User-Agent HTTP request header
              with a link pointing to a page describing the purpose of the
              ExampleBot crawler, which appears as a substring in the User-Agent HTTP
              header and as a product token in the robots[¶](#section-2.2.1-1)

 Note that the product token (ExampleBot) is a substring of
            the User-Agent HTTP header.[¶](#section-2.2.1-3)

 Crawlers MUST use case-[Section 2.2.2](#the-allow-and-disallow-lines).[¶](#section-2.2.1-4)

 If no matching group exists, crawlers MUST obey the group
              with a user-agent line with the "*" value, if present.[¶](#section-2.2.1-6)

 If no group matches the product token and there is no group with a user-agent
              line with the "*" value, or no groups are present at all, no
              rules apply.[¶](#section-2.2.1-8)

#### 
[2.2.2.](#section-2.2.2) [The "Allow" and "Disallow" Lines](#name-the-allow-and-disallow-line)
          

 These lines indicate whether accessing a URI that matches the
              corresponding path is allowed or disallowed.[¶](#section-2.2.2-1)

 To evaluate if access to a URI is allowed, a crawler MUST
              match the paths in "allow" and "disallow" rules against the URI.
              The matching SHOULD be case sensitive. The matching
              MUST start with the first octet of the path. The most
              specific match found MUST be used. The most specific
              match is the match that has the most octets. Duplicate rules in a
              group MAY be deduplicated. If an "allow" rule and a "disallow"
              rule are equivalent, then the "allow" rule SHOULD be used. If no
              match is found amongst the rules in a group for a matching user-agent
              or there are no rules in the group, the URI is allowed. The
              /robots[¶](#section-2.2.2-2)

 Octets in the URI and robots[RFC3986](#RFC3986)], MUST be percent-[RFC3986](#RFC3986)] prior to comparison.[¶](#section-2.2.2-3)

 If a percent-[RFC3986](#RFC3986)]
              or the character is outside the unreserved character range. The match
              evaluates positively if and only if the end of the path from the rule
              is reached before a difference in octets is encountered.[¶](#section-2.2.2-4)

 For example:[¶](#section-2.2.2-5)

 The crawler SHOULD ignore "disallow" and
              "allow" rules that are not in any group (for example, any
              rule that precedes the first user-agent line).[¶](#section-2.2.2-7)

 Implementors MAY bridge encoding mismatches if they
              detect that the robots[¶](#section-2.2.2-8)

#### 
[2.2.3.](#section-2.2.3) [Special Characters](#name-special-characters)
          

 Crawlers MUST support the following special characters:[¶](#section-2.2.3-1)

 If crawlers match special characters verbatim in the URI, crawlers
              SHOULD use "%" encoding. For example:[¶](#section-2.2.3-3)

#### 
[2.2.4.](#section-2.2.4) [Other Records](#name-other-records)
          

 Crawlers MAY interpret other records that are not
              part of the robots[SITEMAPS](#SITEMAPS)]. Crawlers MAY be lenient when
              interpreting other records. For example, crawlers may accept
              common misspellings of the record.[¶](#section-2.2.4-1)

 Parsing of other records
              MUST NOT interfere with the parsing of explicitly
              defined records in [Section 2](#specification).
              For example, a "Sitemaps" record MUST NOT terminate a
              group.[¶](#section-2.2.4-2)

### 
[2.3.](#section-2.3) [Access Method](#name-access-method)
        

 The rules MUST be accessible in a file named
          "/robots[RFC3629](#RFC3629)]) and Internet Media Type
          "text/plain"
          (as defined in [[RFC2046](#RFC2046)]).[¶](#section-2.3-1)

 As per [[RFC3986](#RFC3986)], the URI of the robots[¶](#section-2.3-2)

 "scheme:[[¶](#section-2.3-3)

 For example, in the context of HTTP or FTP, the URI is:[¶](#section-2.3-4)

```
          https://www.example.com/robots.txt
          ftp://ftp.example.com/robots.txt
```
[¶](#section-2.3-5)

#### 
[2.3.1.](#section-2.3.1) [Access Results](#name-access-results)
          

##### 
[2.3.1.1.](#section-2.3.1.1) [Successful Access](#name-successful-access)
            

 If the crawler successfully downloads the robots[¶](#section-2.3.1.1-1)

##### 
[2.3.1.2.](#section-2.3.1.2) [Redirects](#name-redirects)
            

 It's possible that a server responds to a robots[¶](#section-2.3.1.2-1)

 If a robots[¶](#section-2.3.1.2-2)

 If there are more than five consecutive redirects, crawlers
              MAY assume that the robots[¶](#section-2.3.1.2-3)

##### 
[2.3.1.4.](#section-2.3.1.4) ["Unreachable" Status](#name-unreachable-status)
            

 If the robots[¶](#section-2.3.1.4-1)

 If the robots[Section 2.3.1.3](#unavailable-status) or continue to use a cached
              copy.[¶](#section-2.3.1.4-2)

##### 
[2.3.1.5.](#section-2.3.1.5) [Parsing Errors](#name-parsing-errors)
            

 Crawlers MUST try to parse each line of the
              robots[¶](#section-2.3.1.5-1)

## 
[3.](#section-3) [Security Considerations](#name-security-considerations)
      

 The Robots Exclusion Protocol is not a substitute for valid
          content security measures. Listing paths in the robots[RFC9110](#RFC9110)].[¶](#section-3-1)

 To protect against attacks against their system, implementors
          of robots[¶](#section-3-2)

- Memory management:
- 
          [Section 2.5](#limits) defines the lower
              limit of bytes that must be processed, which inherently also
              protects the parser from out-of-memory scenarios.[¶](#section-3-3.2)
- Invalid characters:
- 
          [Section 2.2](#formal-syntax) defines
              a set of characters that parsers and matchers can expect in
              robots.txt files. Out-of-bound characters should be rejected as invalid, which limits the available attack vectors that attempt to compromise the system. [¶](#section-3-3.4)
- Untrusted content:
-  Implementors should treat the content of
              a robots.txt file as untrusted content, as defined by the specification of the application layer used. For example, in the context of HTTP, implementors should follow the Security Considerations section of [ [RFC9110](#RFC9110) ].[¶](#section-3-3.6)

## 
[4.](#section-4) [IANA Considerations](#name-iana-considerations)
      

 This document has no IANA actions.[¶](#section-4-1)

## 
[5.](#section-5) [Examples](#name-examples)
      

### 
[5.1.](#section-5.1) [Simple Example](#name-simple-example)
        

 The following example shows:[¶](#section-5.1-1)

- *:
-  A group that's relevant to all user agents that
                don't have an explicitly defined matching group. It allows
                access to the URLs with the /publications/ path prefix, and it
                restricts access to the URLs with the /example/ path prefix
                and to all URLs with a .gif suffix. The "*" character designates
                any character, including the otherwise-required forward slash; see [Section 2.2](#formal-syntax) .[¶](#section-5.1-2.2)
- foobot:
-  A regular case. A single user agent followed
                by rules. The crawler only has access to two URL path
                prefixes on the site -- /example/page .html and /example /allowed .gif. The rules of the group are missing the optional space character, which is acceptable as defined in [Section 2.2](#formal-syntax) .[¶](#section-5.1-2.4)
- barbot and bazbot:
-  A group that's relevant for more
                than one user agent. The crawlers are not allowed to access
                the URLs with the /example/page .html path prefix but otherwise have unrestricted access to the rest of the URLs on the site. [¶](#section-5.1-2.6)
- quxbot:
-  An empty group at the end of the file. The crawler has
                unrestricted access to the URLs on the site.[¶](#section-5.1-2.8)

```
            User-Agent: *
            Disallow: *.gif$
            Disallow: /example/
            Allow: /publications/
            User-Agent: foobot
            Disallow:/
            Allow:/example/page.html
            Allow:/example/allowed.gif
            User-Agent: barbot
            User-Agent: bazbot
            Disallow: /example/page.html
            User-Agent: quxbot
            EOF
```
[¶](#section-5.1-3)

### 
[5.2.](#section-5.2) [Longest Match](#name-longest-match)
        

 The following example shows that in the case of two rules, the
            longest one is used for matching. In the following case,
            /example[¶](#section-5.2-1)

```
            User-Agent: foobot
            Allow: /example/page/
            Disallow: /example/page/disallowed.gif
```
[¶](#section-5.2-2)

## 
[6.](#section-6) [References](#name-references)
      

### 
[6.1.](#section-6.1) [Normative References](#name-normative-references)
        

- [RFC2046]
- 
Freed, N. and N. Borenstein, "Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types", RFC 2046, DOI 10.17487/RFC2046 , , <[https://](/info/rfc2046) >.www .rfc- editor .org /info /rfc2046
- [RFC2119]
- 
Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119 , , <[https://](/info/rfc2119) >.www .rfc- editor .org /info /rfc2119
- [RFC3629]
- 
Yergeau, F., "UTF-8, a transformation format of ISO 10646", STD 63, RFC 3629, DOI 10.17487/RFC3629 , , <[https://](/info/rfc3629) >.www .rfc- editor .org /info /rfc3629
- [RFC3986]
- 
Berners-Lee, T., Fielding, R., and L. Masinter, "Uniform Resource Identifier (URI): Generic Syntax", STD 66, RFC 3986, DOI 10.17487/RFC3986 , , <[https://](/info/rfc3986) >.www .rfc- editor .org /info /rfc3986
- [RFC5234]
- 
Crocker, D., Ed. and P. Overell, "Augmented BNF for Syntax Specifications: ABNF", STD 68, RFC 5234, DOI 10.17487/RFC5234 , , <[https://](/info/rfc5234) >.www .rfc- editor .org /info /rfc5234
- [RFC8174]
- 
Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174 , , <[https://](/info/rfc8174) >.www .rfc- editor .org /info /rfc8174
- [RFC8288]
- 
Nottingham, M., "Web Linking", RFC 8288, DOI 10.17487/RFC8288 , , <[https://](/info/rfc8288) >.www .rfc- editor .org /info /rfc8288
- [RFC9110]
- 
Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke, Ed., "HTTP Semantics", STD 97, RFC 9110, DOI 10.17487/RFC9110 , , <[https://](/info/rfc9110) >.www .rfc- editor .org /info /rfc9110
- [RFC9111]
- 
Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke, Ed., "HTTP Caching", STD 98, RFC 9111, DOI 10.17487/RFC9111 , , <[https://](/info/rfc9111) >.www .rfc- editor .org /info /rfc9111

### 
[6.2.](#section-6.2) [Informative References](#name-informative-references)
        

- [KiB]
- 
"Kibibyte", Simple English Wikipedia, the free encyclopedia, , <[https://](https://simple.wikipedia.org/wiki/Kibibyte) >.simple .wikipedia .org /wiki /Kibibyte
- [ROBOTSTXT]
- 
"The Web Robots Pages (including /robots.txt)" , 2007, <[https://](https://www.robotstxt.org/) >.www .robotstxt .org/
- [SITEMAPS]
- 
"What are Sitemaps? (Sitemap protocol)", April 2020, <[https://](https://www.sitemaps.org/index.html) >.www .sitemaps .org /index .html
