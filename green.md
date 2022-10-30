---
v: 3

cat: info
pi:
  toc: 'yes'
  symrefs: 'yes'
  sortrefs: 'yes'
  compact: 'yes'
  subcompact: 'no'
  rfcedstyle: 'yes'
  private: yes
wg: IAB e-impact Workshop
date: 2022-10-30
title: >
  CBOR is Greener than JSON
author:
- name: Brendan Moran
- name: Henk Birkholz
- name: Carsten Bormann
  org: Universität Bremen TZI
  street: Postfach 330440
  city: Bremen
  code: D-28359
  country: Germany
  phone: +49-421-218-63921
  email: cabo@tzi.org

informative:
  RFC8890:

--- abstract

This concise position paper illustrates energy use considerations for
data formats used in networks to support green-focused steering decisions for various Internet stakeholders.

--- middle

# Introduction

For encodings of predominantly non-text content, binary encodings should be preferred over textual encodings. ASCII representations of binary or numeric data are substantially larger than binary representations of the same data. While binary representations are often simpler to use in the design and debugging of protocols and documents, ultimately Internet Standards are for end users {{RFC8890}}. While implementers often prefer a certain simplicity and focus on the implementation quality of experience, end users do not care what is easier for design and debugging. They care about responsiveness, battery life, product lifetime, and ecological impact.

Binary encodings outperform textual representations across each of these metrics. They are simpler to decode, more energy efficient and consume less bandwidth. Therefore, Internet Standards should favour binary encodings over textual representations in any scenario where the content is not predominantly text. Compression should be an additional preference where it does not unduly raise the complexity.

# Comparison of Encodings

To demonstrate systemic energy savings through the use of binary encodings and, thus, the ecological impact of encodings, JSON energy consumption is compared to CBOR energy consumption across a range of examples. For the comparison illustrated in this document, transmission over LoRa is used. LoRa is a widely deployed IoT WAN networking protocol that is attractive due to its low power consumption, ease of deployment, and simple software stack.

There are numerous related protocols that deserve similar attention, but are not covered in this contribution:

* 6LoWPAN
* Bluetooth Mesh
* NB-IoT
* WiFi
* Ethernet

However, the scaling of energy use across all protocols is similar. The differences generally arise from packet overhead and maximum payload size. As a result, analysis based on a single IoT networking protocol provides adequate reference information for analyzing the impact of encoding on energy consumption and throughput.

# Impact of encoding based on data-type

Different data types can have different encoding impacts.

NOTE: CBOR encodes integers using the following rules:

Unsigned Integer value | encoding size
---|---
0-23 | 1
24-255 | 2
256 - 65535 | 3
65536 - 2^32-1 | 5
2^32 - 2^64-1 | 9

The differences between encodings are shown below. Where UINT(arg) is shown in the CBOR column, the encoding size above is used based on the value of arg.

Type | JSON Size | CBOR Size
---|---|---
string | strlen+2 | strlen + UINT(strlen)
octets (hex) | size * 2 | size + UINT(size)
octets (b64) | size * 4/3 | size + UINT(size)
int8 | 1 to 3 | 1 or 2 |
int16 | 1 to 5 | 3 |
int32 | 1 to 10 | 5 |
int64 | 1 to 19 | 9 |
float32 | 3 to 16 | 5 |
float64 | 3 to 23 | 9 |
Date | 12 | 2 + UINT(days since 1970)
Array | 2 + count-1  | UINT(count)

This does not include any whitespace or separators in JSON (commas, colons, array and map designators) and other characters to enhance 'human-readable' representations.

When choosing an encoding, binary encodings should be selected for any data structure that is not primarily composed of textual data. Using a rather crude simplification, messages can be separated in their 'scaffolding' and the 'value payload' they transport. In most cases, the proportion of scaffold and values is another selection decision.

## Example preferences

While many dualities exist between JSON-encoded data and CBOR-encoded data, there are some key examples where CBOR structures should clearly be used instead of their JSON counterparts.

* COSE should always be preferred over JOSE
* CBOR should be used for conveyance, while 'human-readability' should be off-loaded to higher layer tools
* CBOR should always be used where stable semantics exist that are designed with build-in extensibility

# LoRa energy consumption

The LoRa configuration used in the following analysis is based on using SX1262 as the leaf node and SX1302 + SX1250 as the LoRa concentrator.

The energy consumption calculations in the following tables are based on the following additional premise:

* The leaf node is based on the SX1262, with DC-DC enabled
* Spreading Factor is 7
* Bandwidth is 125kHz
* Frequency is 868MHz
* Preamble length is 16
* CRC is enabled
* Coding Rate is 4/5
* Transmit power is +14dBm with optimal settings (3.3V)
* Receiver is also 3.3V
* Large payloads are split into packets with no additional framing
* RX Waiting time is ignored
* Calculations are based on the SX1262 datasheet, Section 6.1.4: LoRa® Time-on-Air. See [https://www.semtech.com/products/wireless-rf/lora-connect/sx1262]
* No LoRa concentrator RX calculations are provided because a LoRa concentrator is always receiving.
* LoRa concentrator TX calculations are based on the SX1250 LoRa front-end with the SX1302 baseband processor.

These premise are selected in the context of this contribution to reflect best-case scenarios wherever possible. Regardless, most impacts scale proportionally with encoding size reduction.

Due to channel utilization, there are secondary energy consumption impacts that are caused by larger data encodings: as network utilisation increases, there there is more channel contention causing more re-transmissions due to congestion control mechanisms, which in practice are typically more expensive. The need for additional concentrators is a related consecutive requirement that can cause again additional resources or results in more energy consumption.

LoRa leaf-node Receive Energy(mJ)

{::include lora-rx-leaf.md}

LoRa leaf-node Transmit Energy(mJ)

{::include lora-tx-leaf.md}

LoRa concentrator Transmit Energy(mJ)

{::include lora-tx-concentrator.md}

## Indirect Impacts of higher energy use.

LoRa nodes are frequently arranged to transmit data periodically, for example, every 10 minutes. This contribution is based on the assumption of using a coin-cell powered LoRa node that is designed to report a message containing either a JSON structure or a CBOR structure each time it wakes up. LoRa has a maximum packet size of 255 bytes. Two detailed examples are illustrated below; they are based on example 2 and example 3 data.

Another assumption in the example used is that the interval of one report every 10 minutes utilizes a CR2032 coin cell battery; 3V @ 220mAh, which is 2376J. A consecutive assumption is that the primary source of energy consumption is the LoRa radio and no other significant energy consumption occurs. This forms the baseline for this contribution. These are optimistic assumptions. All real-world applications will be worse than the figures quoted in the examples.

### LoRa reports with example 2 data

Each report is 115 bytes for JSON or 82 bytes for CBOR. From the LoRa leaf-node Transmit Energy table, this means that each report consumes 30.1mJ for JSON or 22.5mJ for CBOR.

| JSON | CBOR
---|---|---
Data Size | 115 | 82
Transmit Energy | 30.1mJ | 22.5mJ
Total Messages | 78936 | 105600
Total Days | 548 | 733

This means that batteries or devices using CBOR to send example 2 data last 33% longer than those using JSON, contributing to less e-waste and battery waste.

### LoRa reports with example 3 data

Each report is 293 bytes for JSON or 195 bytes for CBOR. From the LoRa leaf-node Transmit Energy table, this means that each report consumes 74mJ for JSON or 46.9mJ for CBOR.

| JSON | CBOR
---|---|---
Data Size | 293 | 195
Transmit Energy | 74mJ | 46.9mJ
Total Messages | 32108 | 50660
Total Days | 222 | 351

This means that batteries or devices using CBOR to send example 3 data last 58% longer than those using JSON, contributing to less e-waste and battery waste.

# Appendix: Lora Calculations

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

These calculations are derived from the SX1262 datasheet, section 6.1.4. See here: [https://www.semtech.com/products/wireless-rf/lora-connect/sx1262]


