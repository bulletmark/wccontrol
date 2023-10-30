#!/usr/bin/python3
'Module/program to set a Watts Clever Smart switch on or off.'
# Author: Mark Blakeney, Nov 2018.
from time import sleep

import RPi.GPIO as gpio

# This is a representation of the message protocol used by the Watts
# Clever switch. Embedded values in order are:
# group: 0 to 1023.
# value: 0 or 1 for on/off and second value.
# address: 0 to 7 where 6 = all in same group.
PROTOCOL = '0011010011{:010b}{:01b}{:03b}1'

# Default parameters. Times are all in secs.
PIN = 4
RETRIES = 15
MSGGAP = 20 / 1000

# The following are the bit times for the protocol in secs
BIT_ON_TIMES = (938 / 1_000_000, 407 / 1_000_000)
BIT_TOT_TIME = 1188 / 1_000_000

DELAYS = tuple((b, BIT_TOT_TIME - b) for b in BIT_ON_TIMES)

class _WCcontrol:
    'Class to control a Watts Clever Smart switch'
    pins = {}
    gpio_is_setup = False

    def __init__(self, pin):
        if not self.gpio_is_setup:
            self.gpiosetup = True
            gpio.setwarnings(False)
            gpio.setmode(gpio.BCM)

        gpio.setup(pin, gpio.OUT)
        self.pin = pin

    def set(self, group, address, on, retries=RETRIES):
        'Transmit given value to given address'
        pin = self.pin
        msg = PROTOCOL.format(group, 0 if on else 1, address)
        for r in range(retries):
            for c in msg:
                delay1, delay2 = DELAYS[c == '1']
                gpio.output(pin, 1)
                sleep(delay1)
                gpio.output(pin, 0)
                sleep(delay2)

            sleep(MSGGAP)

def WCcontrol(pin=PIN):
    'Create a new instance or return existing one for this same pin'
    if pin is None:
        pin = PIN

    instance = _WCcontrol.pins.get(pin)
    if not instance:
        instance = _WCcontrol.pins[pin] = _WCcontrol(pin)

    return instance

def main():
    # Process command line options
    import argparse
    opt = argparse.ArgumentParser(description=__doc__.strip(),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    opt.add_argument('-p', '--pin', type=int, default=PIN,
            help='RPi BCM GPIO pin to output')
    opt.add_argument('-r', '--retries', type=int, default=RETRIES,
            help='number of retries to send')
    opt.add_argument('group',
            help='group, 0 to 1023')
    opt.add_argument('address',
            help='switch address to write to, 0 to 7 (6=all in same group)')
    opt.add_argument('value', type=int, choices=range(2),
            help='value 0=off, 1=on')
    args = opt.parse_args()

    groups = [int(g) for g in args.group.split(',')] \
            if ',' in str(args.group) else [int(args.group)]
    addresses = [int(a) for a in args.address.split(',')] \
            if ',' in str(args.address) else [int(args.address)]
    last = (groups[-1], addresses[-1])

    wc = WCcontrol(args.pin)

    for group in groups:
        for addr in addresses:
            wc.set(group, addr, args.value, args.retries)
            print(f'Set Watts Clever switch group {group} + '
                    f'address {addr} to {args.value}')
            if (group, addr) != last:
                sleep(.2)

if __name__ == '__main__':
    main()
