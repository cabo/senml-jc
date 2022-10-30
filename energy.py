#!/usr/bin/env python3
import math as m
import sys

def energy_lora_rx(n_payload_total, SF=7):

    e = 0
    while n_payload_total > 0:
        n_payload = min(n_payload_total, 255)
        n_payload_total -= n_payload

        Npreamble = 16
        BW = 125e3
        Ncrc = 16
        Nheader = 20
        CR = 1

        ToA = 2**SF/BW * (Npreamble + 4.25 + 8 + m.ceil(max(0,8 * n_payload + Ncrc - 4*SF + Nheader)/(4 * SF))) * (CR + 4)

        Volts = 1.8
        Amps = 0.0082

        e += ToA * Volts * Amps

    return e

def size2mJ(rows, energy_fn):
    e_rows = []
    for row in rows:
        r = {'example':row['example']}
        for k in ['json','cbor','half']:
            r[k] = energy_fn(int(row[k])) * 1000
        r['red'] = (r['json']-r['half'])/r['json'] * 100
        e_rows.append(r)
    return e_rows


def main():
    rows=[]
    header=None
    for row in sys.stdin:
        if not header:
            header = [e.strip() for e in row.split('|')]
        else:
            r = {header[i]:v.strip() for i,v in enumerate(row.split('|')) }
            rows.append(r)

    print('LoRa leaf-node Receive Energy(mJ)')
    print('{:>20} | {:>5} | {:>5} | {:>5} | {}'.format(*header))
    lora_rx_rows = size2mJ(rows,energy_lora_rx)
    for row in lora_rx_rows:
        print('{example:>20} | {json:5.1f} | {cbor:5.1f} | {half:5.1f} | {red:2.0f} %'.format(
            **row
        ))


if __name__=='__main__':
    main()
