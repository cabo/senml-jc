---
v: 3
ipr: none

cat: info
wg: IAB e-impact Workshop
date: 2022-10-30
title: >
  CBOR is Greener than JSON
author:
- name: Brendan Moran
  organization: Arm Limited
  email: brendan.moran.ietf@gmail.com
- name: Henk Birkholz
  organization: Fraunhofer SIT
  email: henk.birkholz@sit.fraunhofer.de
- name: Carsten Bormann
  org: Universität Bremen TZI
  street: Postfach 330440
  city: Bremen
  code: D-28359
  country: Germany
  phone: +49-421-218-63921
  email: cabo@tzi.org

informative:
  RFC8428:
  RFC9193:
  RFC8890:
  SX1262:
    target: https://www.semtech.com/products/wireless-rf/lora-connect/sx1262
    title: Product Details — SX1262
  LoRa:
    target: https://www.semtech.com/lora/what-is-lora
    title: What Is LoRa®?


--- abstract

This short position paper illustrates energy use considerations for
data formats used in networks.
It is intended to support green-focused steering decisions for various Internet stakeholders.

--- middle

# Introduction

For encodings of predominantly non-text content, binary encodings
provide performance benefits over textual encodings.
ASCII representations of binary or numeric data are substantially
larger than binary representations of the same data.
Different representation formats are often said to differ in their
simplicity of use in the design and debugging of protocols and
documents; however, ultimately Internet Standards are for end users
{{RFC8890}}.
Implementers often prefer a certain simplicity and focus on the
implementation quality of experience, but end users do not care
what is perceived to be easier for design and debugging.
End users, people who own or operate IoT devices, particularly those
that are powered by primary cells, care that:

* The battery is easily replaceable OR the battery will last the full service life of the device.
* The device has a small ecological footprint (this may not be true for all end users, but it is a growing concern and the topic of this IAB workshop).
* The device completes any tasks it is given in a "reasonable" time.

Binary encodings outperform textual representations across each of
these metrics. They are simpler to encode and decode, more energy
efficient and consume less bandwidth.
Therefore, Internet Standards should favor binary encodings over
textual representations in any scenario where textual representation
does not confer specific benefits.
In general, this is only the case where the entire content is predominantly text.
Data compression technologies are not discussed in this memo; they can
offer additional size benefits but their use also can increase
memory and processing requirements and overall complexity.

# Comparison of Encodings

To demonstrate systemic energy savings through the use of binary encodings and, thus, the ecological impact of encodings, JSON energy consumption is compared to CBOR energy consumption across a range of examples.
This comparison is based on the assumption that, in energy-constrained
environments, processing requirements are dominated by the energy
expenditure for transmission and reception.

For the comparison illustrated in this document, transmission over
LoRa is used {{LoRa}}.
LoRa is a widely deployed IoT WAN networking protocol that is
attractive due to its low power consumption, ease of deployment, and
simple software stack.

There are numerous related protocols that deserve similar attention, but are not covered in this contribution:

* 6LoWPAN
* Bluetooth Mesh
* NB-IoT
* WiFi
* Ethernet

However, the scaling properties of energy use across all protocols are
likely to be similar.
The differences generally arise from packet overhead and maximum
payload size.
As a result, analysis based on a single IoT networking protocol
provides adequate reference information for analyzing the impact of
encoding on energy consumption and throughput.

# Impact of encoding based on data-type

Different data types can have different encoding impacts.

For instance, CBOR encodes integers using the following rules:

| Unsigned Integer value             | encoding size |
| ---                                |          ---: |
| 0 .. 23                            |             1 |
| 24 .. 255                          |             2 |
| 256 .. 65535                       |             3 |
| 65536 .. 2<sup>32</sup>-1          |             5 |
| 2<sup>32</sup> .. 2<sup>64</sup>-1 |             9 |
{: #cbor-integer-sizes title="CBOR Encoding Sizes for Unsigned Integers"}

Based on this, the differences between encodings are shown below.
The JSON size column assumes no redundant blank space is sent to bring
about some readability by humans.
Where UINT(arg) is shown in the CBOR size column, the encoding size above
is used based on the value of arg.

| Type         | JSON Size           | CBOR Size                 |
| ---          | ---                 | ---                       |
| string       | strlen+2 + escaping | strlen + UINT(strlen)     |
| octets (hex) | bytesize * 2        | bytesize + UINT(bytesize) |
| octets (b64) | bytesize * 4/3      | bytesize + UINT(bytesize) |
| int8         | 1 to 3              | 1 or 2                    |
| int16        | 1 to 5              | 3                         |
| int32        | 1 to 10             | 5                         |
| int64        | 1 to 19             | 9                         |
| float32      | 3 to 16             | 5                         |
| float64      | 3 to 23             | 9                         |
| Date         | 12                  | 2 + UINT(days since 1970) |
| Array        | 2 + count-1         | UINT(count)               |
{: #json-cbor-sizes title="Comparing Encoding Sizes"}

# Example Data Structures

Example data structures are provided from {{RFC8428}} (ex_n_), as well
as from {{RFC9193}} and a weather data example (fmi).
The examples are encoded in both JSON and CBOR.
For information, the examples are also provided in an alternative form
that employs half-size float (float16) CBOR; the float16 values are
not used for the "reduction" calculations.

A summary of encoding sizes is provided in {{encoding-sizes}}.

{::include table.md}
{: #encoding-sizes title="Summary of Encoding Sizes for Example Data"}

# LoRa energy consumption

The LoRa configuration used in the following analysis is based on
using the SX1262 chip as the leaf node and SX1302 + SX1250 as the LoRa
concentrator.

The energy consumption calculations in the following tables are based on the following additional premises:

* The leaf node is based on the SX1262, with DC-DC enabled
* Spreading Factor is 7
* Bandwidth is 125 kHz
* Frequency is 868 MHz
* Preamble length is 16
* CRC is enabled
* Coding Rate is 4/5
* Transmit power is +14 dBm with optimal settings (3.3V)
* Receiver is also 3.3 V
* Large payloads are split into packets with no additional framing
* RX Waiting time is not considered
* Calculations are based on the SX1262 datasheet, Section 6.1.4: LoRa® Time-on-Air {{SX1262}}.
* No LoRa concentrator RX calculations are provided because a LoRa concentrator is always receiving.
* LoRa concentrator TX calculations are based on the SX1250 LoRa front-end with the SX1302 baseband processor.

These premises are selected in the context of this contribution to
reflect best-case scenarios wherever possible.
Regardless, most impacts scale proportionally with encoding size
reduction.

Due to channel utilization, there are secondary energy consumption
impacts that are caused by larger data encodings: as network
utilization increases, stronger channel contention causes more
re-transmissions as well as exercises congestion control mechanisms,
which in practice are typically more expensive.
A need for additional concentrators may result as a consequence, which
can result in further increases in energy consumption.

{::include lora-rx-leaf.md}
{: #lora-rx-leaf title="LoRa leaf-node Receive Energy (mJ)"}

{::include lora-tx-leaf.md}
{: #lora-tx-leaf title="LoRa leaf-node Transmit Energy (mJ)"}

{::include lora-tx-concentrator.md}
{: #lora-tx-concentrator title="LoRa concentrator Transmit Energy (mJ)"}

## Indirect Impacts of higher energy use.

LoRa nodes are frequently arranged to transmit data periodically, for example, every 10 minutes. This contribution is based on the assumption of using a coin-cell powered LoRa node that is designed to report a message containing either a JSON structure or a CBOR structure each time it wakes up. LoRa has a maximum packet size of 255 bytes. Two detailed examples are illustrated below; they are based on data from examples ex2 and ex3.

<!-- (* 3 .220 3600)2376.0 -->

We assume an inexpensive CR2032 coin cell battery; 3 V @ 220 mAh, which is 2376 J.
A simplifying assumption is that the primary source of energy
consumption is the LoRa radio and no other significant energy
consumption occurs.
This forms the baseline for this contribution. These are optimistic assumptions. All real-world applications will be worse than the figures quoted in the examples.

### LoRa Reports with Data from Example ex2

Each report is 115 bytes for JSON or 82 bytes for CBOR. From the LoRa leaf-node Transmit Energy table, this means that each report consumes 30.1 mJ for JSON or 22.5 mJ for CBOR.

|                      |  JSON |   CBOR |
| -------------------- | ----: | -----: |
| Data Size            |   115 |     82 |
| Transmit Energy (mJ) |  30.1 |   22.5 |
| Total Messages       | 78936 | 105600 |
| Total Days           |   548 |    733 |
{: #example-2-report title="Reports with Data from Example ex2"}

This means that batteries or devices using CBOR to send data from
example ex2 last 33% longer than those using JSON, contributing to
less e-waste and battery waste.

### LoRa reports with data from example ex3

Each report is 293 bytes for JSON or 195 bytes for CBOR. From the LoRa leaf-node Transmit Energy table, this means that each report consumes 74 mJ for JSON or 46.9 mJ for CBOR.
This example is interesting because the CBOR payload fits in one LoRa packet, while the JSON payload requires two. This means that the CBOR is both smaller overall and has a lower media access overhead.

|                      |  JSON |  CBOR |
| -------------------- | ----: | ----: |
| Data Size            |   293 |   195 |
| Transmit Energy (mJ) |    74 |  46.9 |
| Total Messages       | 32108 | 50660 |
| Total Days           |   222 |   351 |
{: #example-3-report title="Reports With Data from Example ex3"}

This means that batteries or devices using CBOR to send example 3 data last 58% longer than those using JSON, contributing to less e-waste and battery waste.

# Discussion

The findings reported here provide arguments for using concise binary
data representations in place of traditional text-based data formats.

Whether these arguments are considered compelling depends on how
compelling the counterarguments are.  Many developers consider
JSON-based communication to be easier to debug than concise binary
communication.
In practice, non-trivial amounts of JSON need a tool to look at the
data just as a tool is required to look at binary data.
To strengthen the argument here, the findings documented need to be
augmented with data from other parties and additional examples,
preferably including real-world measurements of power consumed by 
transmission, reception, encoding and decoding of messages.

On the other hand, it should be clear from first principles that a
more concise message encoding provides advantages in transmission and
reception power spent.
The examples here provide a rough indication of how significant these
advantages can be in messages that may be typical for IoT
environments.
Larger corpora of such messages need to be collected to obtain a
quantitatively stronger statement.

## cemetery

\[Text saved from above that didn't belong there]:
When choosing an encoding, binary encodings should be selected for any data structure that is not primarily composed of textual data. Using a rather crude simplification, messages can be separated in their 'scaffolding' and the 'value payload' they transport. In most cases, the proportion of scaffold and values is another selection decision.


..## Example preferences

While many dualities exist between JSON-encoded data and CBOR-encoded data, there are some key examples where CBOR structures should clearly be used instead of their JSON counterparts.

* COSE should always be preferred over JOSE
* CBOR should be used for conveyance, while 'human-readability' should be off-loaded to higher layer tools
* CBOR should always be used where stable semantics exist that are designed with built-in extensibility



# Conclusion

In direct comparison, the typical overhead introduced by a 'human-readable' representation in contrast to a binary representation for message transport has been presented as significant in this short contribution.

A generic approach of establishing binary message transfer supported with tooling for human readability will provide resource savings and therefore constitutes a paramount near term goal.
Future evaluation and large scale measurements are required to underpin and establish this as a principal approach.

Internet Standards should use binary encoding as the primary choice. 'Human-readable' encodings should only be used where the nature of the encoded content is predominantly human-readable text.

--- back

# Lora Calculations

LoRa power consumption is calculated with the following equations:

~~~ math
Energy = I \times V \times ToA
~~~

Where:

* I is the current consumed by the transceiver
* V is the voltage applied to the transceiver

~~~ math
ToA = \frac{2^{SF}}{BW}\times N_{symbol}
~~~

Where: 

* SF: Spreading Factor (5 to 12)
* BW: Bandwidth (in Hz)
* ToA: the Time on Air in seconds
* Nsymbol: number of symbols

~~~ math
N_{symbol} = N_{symbol\_preamble}+4.25+8+\left \lceil \frac{max\left ( 8\times N_{byte\_payload}+N_{bit\_CRC}-4\times SF+8+N_{symbol\_header},0 \right )}{4\times SF} \right \rceil\times(CR+4)
~~~

Where:

* N_bit_CRC = 16 if CRC activated, 0 if not
* N_symbol_header = 20 with explicit header, 0 with implicit header
* CR is 1, 2, 3 or 4 for respective coding rates 4/5, 4/6, 4/7 or 4/8

These calculations are derived from the SX1262 datasheet, Section
6.1.4 {{SX1262}}.


<!--  LocalWords:  concentrator baseband concentrators LoRa
 -->
<!--  LocalWords:  deterministically
 -->
