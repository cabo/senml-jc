#!/usr/bin/env python3
import math as m
import sys
import click

def lora_toa(n_payload_total, BW=125e3, SF=7):
    # print('===================')
    # print('Payload: {}'.format(n_payload_total))
    toa = 0

    DR = BW/(2**SF)

    symbols = 0

    while n_payload_total > 0:
        n_payload = min(n_payload_total, 255)
        n_payload_total -= n_payload

        Npreamble = 16
        Ncrc = 16
        Nheader = 20
        CR = 1

        NSymbol_Packet = m.ceil(max(0, 8 * n_payload + Ncrc - 4*SF + Nheader)/(4 * SF)) * (CR + 4)
        NSymbol_coding = Npreamble + 4.25 + 8
        ToA = (NSymbol_coding + NSymbol_Packet)/DR

        #ToA = (2**SF)/BW * (Npreamble + 4.25 + 8 + m.ceil(max(0, 8 * n_payload + Ncrc - 4*SF + Nheader)/(4 * SF)) * (CR + 4))

        symbols += NSymbol_Packet + NSymbol_coding
        toa += ToA

    # print('ToA: {}'.format(toa))
    # print('DR: {}'.format(DR))
    # print('Symbols: {}'.format(symbols))

    return toa


    # return e


def energy_lora_rx(n_payload_total, SF=7):
    Volts = 3.3
    Amps = 0.0046
    P = Volts * Amps

    ToA = lora_toa(n_payload_total, SF=SF)
    e = ToA * P
    # print('Power: {}'.format(P))
    # print('Energy: {}'.format(e))
    return e

def energy_lora_tx(n_payload_total, SF=7):
    '''SX1262 868MHz, +14dBm, Optimal Settings TX power calculation'''
    Volts = 3.3
    Amps = 0.045
    P = Volts * Amps

    ToA = lora_toa(n_payload_total, SF=SF)
    e = ToA * P
    # print('Power: {}'.format(P))
    # print('Energy: {}'.format(e))
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


@click.command()
@click.option('-t', '--type', 'energy_type', type=click.Choice(['leaf-rx', 'leaf-tx'], case_sensitive=False),
    default='leaf-rx')
def main(energy_type):
    rows=[]
    header=None
    for row in sys.stdin:
        if not header:
            header = [e.strip() for e in row.split('|')]
        else:
            r = {header[i]:v.strip() for i,v in enumerate(row.split('|')) }
            rows.append(r)

    # print('LoRa leaf-node Receive Energy(mJ)')
    print('{:>20} | {:>5} | {:>5} | {:>5} | {}'.format(*header))
    lora_rows = size2mJ(rows,{'leaf-rx':energy_lora_rx, 'leaf-tx':energy_lora_tx}[energy_type])
    for row in lora_rows:
        print('{example:>20} | {json:5.1f} | {cbor:5.1f} | {half:5.1f} | {red:2.0f} %'.format(
            **row
        ))


if __name__=='__main__':
    main()
