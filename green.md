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

This short position paper looks at energy use considerations for
data formats used in networks.

--- middle


# Introduction

For encodings of predominantly non-text content, binary encodings should be preferred over textual encodings. ASCII representations of binary or numeric data are substantially larger than binary representations of the same data. While binary representations are often simpler to use in the design and debugging of protocols and documents, internet standards are for end users {{RFC8890}}. End users do not care what is easier for design and debugging. They care about responsiveness, battery life, product lifetime, and ecological impact.

Binary encodings outperform textual representations across each of these metrics. They are simpler to decode, more energy efficient and consume less bandwidth. Therefore, internet standards should prefer binary encodings over textual representations in any scenario where the content is not predominantly text. Compression should be preferred where it does not unduly raise the complexity.

# Comparison of Encodings

To demonstrate the energy saved through the use of binary encodings and, thus, the ecological impact of encodings, JSON energy consumption is compared to CBOR energy consumption across a range of examples. For this comparison, transmission over LoRa is used. LoRa is a widely deployed IoT networking protocol that is attractive due to its low power consumption, ease of deployment, and simple software stack.

Other protocols that should be considered include:

* 6LoWPAN
* Bluetooth Mesh
* NB-IoT
* WiFi
* Ethernet

However, the scaling of energy use across all protocols is similar. The differences generally arise from packet overhead and maximum payload size. As a result, analysis based on a single IoT networking protocol should provide adequate information for analyzing the impact of encoding on energy consumption and througput.

# Impact of encoding based on data-type

Each data type has a different encoding impact.

NOTE: CBOR encodes integers using the following rules:

Positive Integer value | encoding size
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

This does not include any whitespace or separators in JSON (commas, colons, array and map designators).

When choosing an encoding, binary encodings should be selected for any data structure that is not primarily composed of textual data. 

## Example preferences

While many dualities exist between JSON-encoded data and CBOR-encoded data, there are some key examples where CBOR structures should clearly be used instead of their JSON counterparts.

* COSE should always be prefered over JOSE
* TODO: Add more!

# LoRa energy consumption

The LoRa configuration used in the following analysis is based on using SX1262 as the leaf node and SX1302 + SX1250 as the LoRa concentrator.

The energy consumption calculations in the following tables are based on the following additional assumptions:

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

These assumptions are intended to be best-case scenarios wherever possible. Regardless, most impacts scale proportionally with encoding size reduction.

Due to channel utilization, there are secondary energy effects that are caused by larger data encodings: As network utilisation increases, there there is more channel contention, this causes more re-transmissions, which are more expensive. It also causes the requirement for additional concentrators, which consume more resources and more energy.

LoRa leaf-node Receive Energy(mJ)

{::include lora-rx-leaf.md}

LoRa leaf-node Transmit Energy(mJ)

{::include lora-tx-leaf.md}

LoRa concentrator Transmit Energy(mJ)

{::include lora-tx-concentrator.md}

## Indirect Impacts of higher energy use.

LoRa nodes are frequently arranged to transmit data periodically, for example every 10 minutes. Suppose there is a coin-cell powered LoRa node that is designed to report a message containing either a JSON structure or a CBOR structure each time it wakes up. LoRa has a maximum packet size of 255 bytes. Two examples are given below; they are based on example 2 and example 3 data.

For this example, the assumption is reports every 10 minutes with a CR2032 coin cell battery; 3V @ 220mAh, which is 2376J. It is assumed that the primary source of energy consumption is the LoRa radio, so no other energy consumption is used. This forms a baseline. All real-world applications will be worse than the figures quoted in these examples.

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


