#!/usr/bin/python

# Run this script:
#   $ ./generate_mac.py
#   $ ./generate_mac.py -p aa:bb:cc -n 3 -i 4
#
# Get help:
#   $ ./generate_mac.py -h

import random
import argparse
import datetime

maxVMs = 500
maxNICs = 10

def randomMacGen(prefix):
    """
    Generate 1 random MAC address with the given 3 bytes prefix.
    """
    return (prefix + ":%02x:%02x:%02x" % (random.randint(0, 255), 
                                          random.randint(0, 255), 
                                          random.randint(0, 255)))



def listAllMac(prefix, vm, nic):
    """
    Create all MAC addresses that are needed. They are unique.
    Stores all MAC addresses in a list.
    """
    totalMac = vm*nic
    listMac = []
    i=0
    while i < totalMac:
        if randomMacGen(prefix) not in listMac:
            listMac.append(randomMacGen(prefix))
            i=i+1
    return listMac



def displayAllMac(listMac, vm, nic):
    """
    Displays the MAC address list in terminal.
    """
    vmCount=1
    print ()
    now = datetime.datetime.now()
    print ("MAC addresses list for %03s VMs "
           "with %02s NICs per VM." % (vm, nic))
    print (now.strftime("%Y-%m-%d %H:%M:%S"))

    for i in range(0, len(listMac), nic):
        print ("\n VM #%03s" % vmCount)
        print ("\n".join(listMac[i:i+nic]))
        vmCount=vmCount + 1
    print ("\nEOF")




def main():
    parser = argparse.ArgumentParser(description="Generate a list of random "
                                     "and unique MAC addresses for all your "
                                     "VMs. The MAC addresses are derived from "
                                     "a given prefix XX:XX:XX (the first 3 "
                                     "bytes) pattern."
                                     " "
                                     "This is useful when you want to create "
                                     "VMs with a libvirt/KVM tool such as " 
                                     "virt-install and set 'static' MAC "
                                     "addresses to configure a DHCP server "
                                     "for these VMs.")
    parser.add_argument("-p","--prefix",
                        help="Choose MAC address prefix (3 bytes) patern. "
                        "Format is xx:xx:xx where x is hex value (0 to f). "
                        "Default is aa:aa:aa.",
                        default="aa:aa:aa")
    parser.add_argument("-n","--number",
                        type=int,
                        help="Total number of MAC addresses you need,"
                        " defaul = 1.",
                        default=1)
    parser.add_argument("-i","--interface",
                        type=int,
                        help="Total number of NIC interfaces per VMs, "
                        "defaul = 1.",
                        default=1)
    args = parser.parse_args()


    # Make some verification about input values
    if args.prefix == "00:00:00":
        parser.error("Prefix should not be 00:00:00.")
    if len(args.prefix) < 8:
        parser.error("Prefix is not valid.")
    if args.number < 1:
        parser.error("Minimun number of VMs is 1.")
    if args.number > maxVMs:
        parser.error("Maximum number of VM is %s" % maxVMs)
    if args.interface < 1:
        parser.error("Minimun number of NIC per VM is 1.")
    if args.interface > maxNICs:
        parser.error("Maximum number of NICs per VM is %s." % maxNICs)
    
    # Create the MAC address list and displays it in terminal
    finallist = listAllMac(args.prefix, args.number, args.interface)
    displayAllMac(finallist, args.number, args.interface)

if __name__=="__main__":
    main()
