#!/usr/bin/python3
'Module/program to set a Watts Clever Smart switch on or off.'
# Author: Mark Blakeney, Nov 2018.

from time import sleep as _sleep
import RPi.GPIO as gpio

# This is a representation of the message protocol used by the Watts
# Clever switch. Embedded values in order are:
# group: 0 to 1023.
# value: 0 or 1 for on/off and second value.
# address: 0 to 7 where 6 = all in same group.
protocol = '0011010011{:010b}{:01b}{:03b}1'

# Default parameters. Times are all in secs.
pin = 4
retries = 10
bitshortgap = 406 / 1000000
bitlonggap = 937 / 1000000
msggap = 20 / 1000

def set(group, address, on, gpiopin=None):
    'Transmit given value to given address'
    if gpiopin is None:
        gpiopin = pin

    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(gpiopin, gpio.OUT)

    msg = protocol.format(group, 0 if on else 1, address)

    for r in range(retries):
        for c in msg:
            if c == '1':
                delay1 = bitshortgap
                delay2 = bitlonggap
            else:
                delay1 = bitlonggap
                delay2 = bitshortgap

            gpio.output(gpiopin, 1)
            _sleep(delay1)
            gpio.output(gpiopin, 0)
            _sleep(delay2)

        _sleep(msggap)

def main():
    global pin, retries, bitshortgap, bitlonggap, msggap
    # Process command line options
    import argparse
    opt = argparse.ArgumentParser(description=__doc__.strip(),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    opt.add_argument('-p', '--pin', type=int, default=pin,
            help='RPi BCM GPIO pin to output')
    opt.add_argument('-r', '--retries', type=int, default=retries,
            help='number of retries to send')
    opt.add_argument('-s', '--bitshortgap', type=int,
            default=int(bitshortgap * 1000000),
            help='inter bit short gap in microseconds')
    opt.add_argument('-l', '--bitlonggap', type=int,
            default=int(bitlonggap * 1000000),
            help='inter bit long gap in microseconds')
    opt.add_argument('-m', '--msggap', type=int,
            default=int(msggap * 1000),
            help='inter message gap in milliseconds')
    opt.add_argument('group',
            help='group, 0 to 1023')
    opt.add_argument('address',
            help='switch address to write to, 0 to 7 (6=all in same group)')
    opt.add_argument('value', type=int, choices=range(2),
            help='value 0=off, 1=on')
    args = opt.parse_args()

    retries = args.retries
    bitshortgap = args.bitshortgap / 1000000
    bitlonggap = args.bitlonggap / 1000000
    msggap = args.msggap / 1000

    groups = [int(g) for g in args.group.split(',')] \
            if ',' in str(args.group) else [int(args.group)]
    addresses = [int(a) for a in args.address.split(',')] \
            if ',' in str(args.address) else [int(args.address)]
    last = (groups[-1], addresses[-1])

    for group in groups:
        for addr in addresses:
            set(group, addr, args.value, args.pin)
            print('Set Watts Clever switch group {} + address {} to {}'.format(
                group, addr, args.value))
            if (group, addr) != last:
                _sleep(.2)

if __name__ == '__main__':
    main()
