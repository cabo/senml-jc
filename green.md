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


Type | JSON Size | CBOR Size
---|---|---
string | strlen+2 | strlen + (1, 2, 3, 5, 9)
octets (hex) | size * 2 | size + (1, 2, 3, 5, 9)
octets (b64) | size * 4/3 | size + (1, 2, 3, 5, 9)
int8 | 1 to 3 | 1 or 2 |
int16 | 1 to 5 | 3 |
int32 | 1 to 10 | 5 |
int64 | 1 to 19 | 9 |
float32 | 3 to 16 | 5 |
float64 | 3 to 23 | 9 |
Date | 12 | CARSTEN TODO

When choosing an encoding, 

{::include-nested-dedent LoRa.md}

