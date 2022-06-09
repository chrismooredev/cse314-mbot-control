#!/usr/bin/python3

import time
import pywifi

TGT='ARRIS-CD12'

def stat2str(status):
    if isinstance(status, pywifi.iface.Interface):
        status = status.status()
    assert isinstance(status, int), "provided status isn't int or pywifi.Profile! got " + str(type(status))
    for k,v in pywifi.const.__dict__.items():
        if k.startswith('IFACE_'):
            if v == status:
                return k[6:]
    return "unknown(" + str(status) + ")"

    

wifi = pywifi.PyWiFi()
ifs = wifi.interfaces()

# for iface in ifs: print(stat2str(iface))
# for iface in ifs: iface.scan()
# for iface in ifs: print(stat2str(iface))

# time.sleep(1)

found_nets = []
for iface in ifs:
    scan = iface.scan_results()
    for p in scan:
        if p.ssid == TGT:
            print(p.signal)
            break
    else: # not found
        found_nets.extend(scan)
        continue
    break
else:
    print(TGT + " network not found:")
    for p in found_nets:
        print("\t" + str(p.signal) + "dB = " + p.ssid)
