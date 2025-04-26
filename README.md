# MP71077x
An UNOFFICIAL Python library for controlling Multicomp MP71077x and Korad KEL20x0 electronic loads over Ethernet

### Works with:
- Multicomp MP710772 (150V/40A/500W), tested on Windows 11 machine with Python 3.12.2

### Not tested, but should work with:
- Multicomp MP710771 and Korad KEL2010 (150V/40A/300W)
- Korad KEL2020 (150V/40A/500W)
- Multicomp MP710773 and Korad KEL2030 (150V/40A/1000W)
- Multicomp MP710778 and Korad KEL2040  (150V/40A/1500W)

## Usage requirements and flow

1. Install recent colorama (for colorized debug outputs) - `pip3 install colorama`
2. Set proper IP address, netmask and gateway on your electronic load (since I had problems when enabling DHCP client on my load). If your network uses DHCP server, create some small address region with reserved IP range and set IP adress of your load to any value in this reserved range.
3. Try to ping the device (must be turned on!) from command line using `ping` command with device IP following. You should get response, if your device network settings are OK. Your code should look somehow like this:
```
import MP71077x
import time

load = MP71077x.MP71077x("192.168.88.82", verbosity=True)
load.openSocket()

load.setCVvoltage(20.000, True)
load.turnInputON(True)
time.sleep(2)
load.turnInputOFF(True)

print(load.getVoltageLimits())

load.closeSocket()
```
You should see following output in your terminal:
```
MP71077x(192.168.88.82): Setting CV voltage to 20.0
MP71077x(192.168.88.82): Asking for CV voltage
MP71077x(192.168.88.82): Load input has been turned on
MP71077x(192.168.88.82): Load input has been turned off
MP71077x(192.168.88.82): Asking for both voltage limits
MP71077x(192.168.88.82): Asking for lower voltage limit
MP71077x(192.168.88.82): Asking for upper voltage limit
(0.1, 20.0)
```
5. Feel free to use the library :)

## Some remarks

I was a little bit frustrated with lack of documentation after buying of my electronic load, because there was no CD attached to my device nor UDP comands communication description available on device supplier's website (Farnell). After some investigation I found out, that Multicomp and Korad electronic loads have probably the same manufacturer and work the same way. I can supply to you following links with documentation or software I have found:

- Some software is available on Multicomp distributor's website [Farnell - software V4.1, USB driver, basics of IP protocol, ...](https://www.farnell.com/software/4155422.zip)
- UDP Ethernet and Serial communication protocol is available on Korad distributor's website [eleshop.eu - Communication Protocol v1.10](https://static.eleshop.nl/mage/media/downloads/KEL2000SeriesCommunicationProtocolV1.10.pdf)
- Some interesting facts about these electronic loads [EEVblog](https://www.eevblog.com/forum/testgear/korad-kel2010-multicomp-mp710771-review/)

## Future & TODO

This is only preliminary version of the library, I can say it is only a teaser. 
More and more functionalities will be added in the future.
I am looking forward to your requests, test reports etc. 
