## WCCONTROL - Watts Clever Switch Control

This is a Raspberry Pi command line program and Python module to switch
on and off a Watts Clever RF Switch via a cheap 433 MHz transmitter
module. I also have a higher level program
[`wcscheduler`](https://github.com/bulletmark/wcscheduler) which imports
this module and can be used to schedule one or more switches on/off at
specified times and days of week.

The `wccontrol` module implements the protocol which was reverse
engineered in the excellent posts
[here](https://goughlui.com/2016/04/10/reverse-eng-watts-clever-easy-off-sockets-wsmart-box-es-aus1103/)
and
[here](https://goughlui.com/2016/04/13/reverse-eng-pt-2-watts-clever-easy-off-wsmart-box-es-aus1103/).

The latest version of this document and code is available at
https://github.com/bulletmark/wccontrol.

### Watts Clever Switch

You need one or more of these:

![Watts Clever RF Switch](http://i.imgur.com/mILcB6m.jpg)

Often this is purchased in a pack with 2 or 4 such switches, and an IR
(infra-red) receiver box which allows you to operate the remote switches using a
standard TV remote which talks IR to the receiver, then the receiver
talks RF 433 MHz to the switches. E.g the pack is:

![Watts Clever Easy Off Pack](http://i.imgur.com/uqLBL8f.jpg)

The `wccontrol` module allows your Raspberry Pi to talk directly via RF
to the switches. You do not need the IR receiver box at all (i.e. you do
not need the blue box in above image), neither to operate or initially
program the switches. `wccontrol` can be used to fully program
switch group and addresses, and then to operate the switches on and off.

### RF Transmitter

You also need a 433 MHz RF transmitter.

![RF Transmitter](http://i.imgur.com/UHoh3Px.jpg)

RF modules for Raspberry Pi and similar devices are purchased for only a
few bucks on ebay etc, usually as a transmitter and receiver pair. To
use `wccontrol`, we only need the transmitter which is the smaller board
as shown above.

The transmitter has 3 pins which you directly connect to the RPi header
pins using push-on [female to female jumper
wires](https://cdn.solarbotics.com/products/photos/0044041262b3ac74afe434653a898da2/45030-IMG_6230wht.jpg)
as follows.

Tx pin | Description | Raspberry Pi GPIO header
------ | ----------- | ------------------------
Left   | Data        | GPIO4 (board pin 7)
Middle | VCC         | 5V power (e.g. board pin 4)
Right  | GND         | Ground  (e.g. board pin 6).

You can significantly increase the range of the transmitter by soldering
a 17.3 cm copper wire to the ANT pad in the corner of the PCB. Ideally,
orientate the wire parallel to the switches.

Note that `wccontrol` uses GPIO4 by default to drive the transmitter but
you can easily set it to use any of the other Raspberry Pi GPIO pins by
passing the `pin` argument.

### Installation

`wccontrol` is [available on PyPI](https://pypi.org/project/wccontrol/)
so install the usual way, e.g:

```bash
pip install wccontrol
```

Or explicitly from [github](https://github.com/bulletmark/wccontrol):

```bash
git clone https://github.com/bulletmark/wccontrol.git
cd wccontrol
sudo make install
```

#### Make GPIO Device Accessible

To be able to run this utility/module as your normal user you need to
install a udev rule and assign yourself to the `gpio` group.

As root, create `gpio` group:

    sudo groupadd -f -r gpio

Add your user to that group:

    sudo usermod -G gpio $USER

Install `gpio.rules`:

    sudo cp gpio.rules /etc/udev.rules.d/99-gpio.rules

Reboot your RPi and log back in again.

### Groups and Addresses

Before you can operate a switch on/off you must first program it to
respond to a specific _group_ and _address_.

A _group_ is a number 0 to 1023. An _address_ is a number 0 to 7 within
a group that you allocate to specific switches. Address number 6 is
special as it means "all addresses in same group", i.e. you can switch
all devices together in the same group by using address 6. So there are
actually only 7 unique addresses which you can use per group, 0->5 and
7. Thus there are potentially 1024 x 7 individually addressable devices
you can control.

#### Program Group and Address to Device

E.g. say you want to assign your first switch as address 0 in group 0.

1. Ensure power is applied to the switch.
1. Ensure switch is OFF, i.e. press button to turn LED OFF.
1. Press and hold the switch button until the LED fast flashes, then
   slow flashes, then release.
1. Execute the ON command `wccontrol 0 0 1` to program ON.
1. Execute the OFF command `wccontrol 0 0 0` to program OFF.
1. The LED will go OFF and the switch is now programmed.
1. Test using `wccontrol 0 0 1` to confirm the switch goes ON then 
   `wccontrol 0 0 0` to confirm the switch goes OFF.
1. Repeat the above steps for your other switches using a different group/address.

### Example Commands to Switch On and Off

Switch group 0, device 2 to ON:

    wccontrol 0 2 1

Switch group 0, device 2 to OFF:

    wccontrol 0 2 0

Switch group 0, device 3 to ON:

    wccontrol 0 3 1

Switch group 0, device 3 to OFF:

    wccontrol 0 3 0

Switch both (i.e. all) devices in group 0 to ON:

    wccontrol 0 6 1

Switch both (i.e. all) devices in group 0 to OFF:

    wccontrol 0 6 0

### Using as a Python Module

```python
import wccontrol
wccontrol.set(0, 2, 1)
```

See the stub main code in `wccontrol.py` for a more complete example.

<!-- vim: se ai syn=markdown: -->
