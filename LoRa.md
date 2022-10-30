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

LoRa leaf-node Receive Energy(mJ)

{::include lora-rx-leaf.md}

LoRa leaf-node Transmit Energy(mJ)

{::include lora-tx-leaf.md}
