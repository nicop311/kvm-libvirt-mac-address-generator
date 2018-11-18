#!/usr/bin/python
# -*- coding: utf-8 -*-

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


class Vm:
    """
    The VM class represent 1 qemu/KVM VM with its Network Interface Cards
    (NICs.)
    
    Args:
        name (str): The VM name.
        nics (int): Quantity of MAC addresses (= Quantity of NICs).

    Attributes:
        name (str): The VM name.
        nics (int): Quantity of MAC addresses (= Quantity of NICs).
        list_nics (:obj:`list` of :obj:`str`): List of all MAC addresses for all NICs.
        
    """

    def __init__(self, name, nics):
        self.name = name
        self.nics = nics
        self.list_nics = []


    def addMac(self, mac):
        self.list_nics.append(mac) 

    def delMac(self, mac):
        self.list_nics.remove(mac)


    def showVm(self):
        print ("\n" + self.name)
        for i in range(0, self.nics):
            print ("\n".join(self.list_nics))
    
    def showVmDhcpXmlOneItf(self, itf):
        """
        Display an xml line for libvirt's network bridge configuration file 
        for a given NIC (the NIC is chosen with its location `itf` in the
        `list_nics`.).

        The line looks like this:
        <host mac="00:16:3e:3e:a9:1a" name="bar.example.com" ip="192.168.122.11"/>


        Args:
            itf (int): the location of the itf^th NIC in the list.
        """
        if itf < self.nics:
            print ("<host mac=\"" + self.list_nics[itf] + "\"" +
                   " name=\"" + self.name + "\"" + " ip=\"x.x.x.x\"/>")


    def showVmDhcpXmlAllItf(self):
        for i in range(0, self.nics):
            self.showVmDhcpXmlOneItf(i)



class Maclist:
    """
    Maclist is a dictionnary of Vm. Given a number of VMs and the quatity of
    NICs per VM, Maclist creates a list of MAC addresses for all the VMs.

    Args:
        vm_qtt (int): The quantity of VM needed.
        nics (int): Quantity of MAC addresses (= Quantity of NICs) per VM.

    Attributes:
        vm_qtt (int): The quantity of VM needed.
        nics (int): Quantity of MAC addresses (= Quantity of NICs) per VM.
        list_nics (:obj:`list` of :obj:`str`): List of all MAC addresses for all NICs.
    """

    def __init__(self, vm_qtt, nics, prefix):
        self.vm_qtt = vm_qtt
        self.nics = nics
        self.prefix = prefix

        self.maclist = []
        self.vms = []


    def randomMacGen(self):
        """
        Generate 1 random MAC address with the given 3 bytes prefix.
        Args:
            prefix (str): The 3 bytes long MAC address prefix.
        """
        return (self.prefix + ":%02x:%02x:%02x" % (random.randint(0, 255), 
                                                   random.randint(0, 255), 
                                                   random.randint(0, 255)))
    def addVm(self, name):
        self.vms.append(Vm(name, self.nics))

    def buildMacList(self):
        """
        """
        totalMac = self.vm_qtt*self.nics 
        i=0
        while i < totalMac:
            macbuffer = self.randomMacGen()
            if macbuffer not in self.maclist:
                self.maclist.append(macbuffer)
                i=i+1

    def populateVm(self):
        """
        """
        macCount = 0
        while macCount < self.vm_qtt*self.nics: 
            for i in range(0,self.vm_qtt):
                self.addVm("VM %s" % (i+1))
                for j in range(0, self.nics):
                    self.vms[i].addMac(self.maclist[macCount])
                    macCount = macCount + 1


    def displayAllMac(self):
        """
        Displays the MAC address list in terminal.
        """
        vmCount=1
        print ()
        now = datetime.datetime.now()
        print ("MAC addresses list for %03s VMs "
               "with %02s NICs per VM." % (self.vm_qtt, self.nics))
        print (now.strftime("%Y-%m-%d %H:%M:%S"))

        for i in range(0, len(self.maclist), self.nics):
            print ("\n VM #%03s" % vmCount)
            print ("\n".join(self.maclist[i:i+self.nics]))
            vmCount=vmCount + 1
        print ("\nEOF")

    def displayAllVms(self):
        print ("\n \n XML config for each NIC, i.e. for each network bridge:")
        for i in range(0, self.vm_qtt):
            self.vms[i].showVmDhcpXmlAllItf()


    def displayAllMacPerItf(self):
        print ("\n \n XML config for each NIC, i.e. for each network bridge:")
        for i in range(0, self.nics):
            print ("\n  Bridge/NIC number %02s" % (i+1))
            for j in range(0, self.vm_qtt):
                self.vms[j].showVmDhcpXmlOneItf(i)


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
#    vm1 = Vm("maVM1", args.interface)
#    vm1.showVm()
#    vm1.addMac("OSEF")
#    vm1.addMac("OSEF")
#    vm1.showVm()
#    vm1.showVmDhcpXmlOneItf(0)
    
    list1 = Maclist(args.number, args.interface, args.prefix)
    list1.buildMacList()
    list1.populateVm()
    list1.displayAllMac()
#    list1.displayAllVms()
    list1.displayAllMacPerItf()

if __name__=="__main__":
    main()
