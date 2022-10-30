# LoRa energy consumption

The energy consumption calculations in the following tables are based on the following assumptions:

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

Due to channel utilization, there are secondary energy effects that are caused by larger data encodings.

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

