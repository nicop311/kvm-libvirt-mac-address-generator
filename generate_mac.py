#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : generate_mac.py
# Author            : nicop311
# Date              : 19.11.2018
# Last Modified Date: 19.11.2018
#
#
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
        nics (int): Quantity of MAC addresses (= Quantity of NICs) per VM.

    Attributes:
        name (str): The VM name.
        nics (int): Quantity of MAC addresses (= Quantity of NICs) per VM.
        list_nics (:obj:`list` of :obj:`str`): List of all MAC addresses for all NICs for 1 VM.
        
    """

    def __init__(self, name, nics):
        self.name = name
        self.nics = nics
        self.list_nics = []


    def addMac(self, mac):
        self.list_nics.append(mac) 


    def delMac(self, mac):
        self.list_nics.remove(mac)

    
    # TODO: must modify showVm
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
    Given a number of VMs and the quatity of NICs per VM, Maclist creates a 
    list of unique MAC addresses for all the VMs.

    The MAC addresses are derived from a 3 bytes long prefix.

    Args:
        vm_qtt (int): The quantity of VM needed.
        nics (int): Quantity of MAC addresses (= Quantity of NICs) per VM.
        prefix (str): 3 bytes long MAC address prefix.

    Attributes:
        vm_qtt (int): The quantity of VM needed.
        nics (int): Quantity of MAC addresses (= Quantity of NICs) per VM.
        prefix (str): 3 bytes long MAC address prefix.
        list_nics (:obj:`list` of :obj:`str`): List of all unique MAC addresses for all NICs.
        vms (:obj:`list` of :obj:`Vm`): List of all VMs

    """

    def __init__(self, vm_qtt, nics, prefix):
        self.vm_qtt = vm_qtt
        self.nics = nics
        self.prefix = prefix

        self.maclist = []
        self.vms = []
        now = datetime.datetime.now()
        self.datetime = now.strftime("%Y-%m-%d %H:%M:%S")


    def printTimeDateHeader(self):
        print ("\n#######################################"
        "########################################")
        print ("MAC Address list generated on: " + self.datetime)


    def randomMacGen(self):
        """
        Generate 1 random MAC address with the given 3 bytes prefix.
        """
        return (self.prefix + ":%02x:%02x:%02x" % (random.randint(0, 255), 
                                                   random.randint(0, 255), 
                                                   random.randint(0, 255)))

    
    def addVm(self, name):
        """
        Create a VM, and adds it to the list of VMs.
        
        Args:
            name (str): name of the VM.
        """
        self.vms.append(Vm(name, self.nics))


    def buildMacList(self):
        """
        Create a list of unique MAC addresses.
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
        Assign MAC addresses to each NICs of each VMs.
        """
        macCount = 0
        while macCount < self.vm_qtt*self.nics: 
            for i in range(0,self.vm_qtt):
                self.addVm("VM #%03s" % (i+1))
                for j in range(0, self.nics):
                    self.vms[i].addMac(self.maclist[macCount])
                    macCount = macCount + 1


    def displayAllMacPerVm(self):
        """
        Displays only the MAC address list in terminal per VMs.

        Example:
             VM #  1
            aa:bb:cc:c9:a2:8b
            aa:bb:cc:81:d5:d3
            aa:bb:cc:fc:b0:fd
            aa:bb:cc:91:e7:83
             
             VM #  2
            aa:bb:cc:3c:b6:19
            aa:bb:cc:32:81:00
            aa:bb:cc:ef:30:18
            aa:bb:cc:03:44:8e
        """
        vmCount=1
        self.printTimeDateHeader()
        print ("\n \nMAC addresses list for %03s VMs "
               "with %02s NICs per VM." % (self.vm_qtt, self.nics))

        for i in range(0, len(self.maclist), self.nics):
            print ("\n VM #%03s" % vmCount)
            print ("\n".join(self.maclist[i:i+self.nics]))
            vmCount=vmCount + 1
        print ("\n \n End of MAC addresses list for %03s VMs "
               "with %02s NICs per VM." % (self.vm_qtt, self.nics))
        print ("#######################################"
               "########################################")


    # TODO: use the method "showVm" to simplify
    def displayAllXmlMacPerVM(self):
        """
        Shows the XML libvirt network static DHCP entries configuration
        per VMs.

        Example:
              VM #  1
            <host mac="aa:bb:cc:c9:a2:8b" name="VM #  1" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:81:d5:d3" name="VM #  1" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:fc:b0:fd" name="VM #  1" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:91:e7:83" name="VM #  1" ip="x.x.x.x"/>
    
              VM #  2
            <host mac="aa:bb:cc:3c:b6:19" name="VM #  2" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:32:81:00" name="VM #  2" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:ef:30:18" name="VM #  2" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:03:44:8e" name="VM #  2" ip="x.x.x.x"/>

        """
        self.printTimeDateHeader()
        print ("\n \n Libvirt XML config for each VM:")
        for i in range(0, self.vm_qtt):
            print ("\n  VM #%03s" % (i+1))
            self.vms[i].showVmDhcpXmlAllItf()
        print ("\n \n End of Libvirt XML config for each VM")
        print ("#######################################"
               "########################################")


    def displayAllMacPerItf(self):
        """
        Displays only the MAC address list in terminal per NIC interface,
        i.e. per bridge.

        """
        self.printTimeDateHeader()
        print ("\n \n Displays the MAC address list per NIC, "
               "i.e. for each libvirt network bridge:")
        for i in range(0, self.nics):
            print ("\n  Bridge/NIC number %02s" % (i+1))
            for j in range(0, self.vm_qtt):
                print (self.vms[j].list_nics[i])
        print ("\n \n End of Displays the MAC address list per NIC ")
        print ("#######################################"
               "########################################")


    def displayAllXmlMacPerItf(self):
        """
        Shows the XML libvirt network static DHCP entries configuration
        per NIC interfaces, i.e. per network bridge.

        Example:
          Bridge/NIC number  1
            <host mac="aa:bb:cc:c9:a2:8b" name="VM #  1" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:3c:b6:19" name="VM #  2" ip="x.x.x.x"/>
            
              Bridge/NIC number  2
            <host mac="aa:bb:cc:81:d5:d3" name="VM #  1" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:32:81:00" name="VM #  2" ip="x.x.x.x"/>
            
              Bridge/NIC number  3
            <host mac="aa:bb:cc:fc:b0:fd" name="VM #  1" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:ef:30:18" name="VM #  2" ip="x.x.x.x"/>
            
              Bridge/NIC number  4
            <host mac="aa:bb:cc:91:e7:83" name="VM #  1" ip="x.x.x.x"/>
            <host mac="aa:bb:cc:03:44:8e" name="VM #  2" ip="x.x.x.x"/>

        """
        self.printTimeDateHeader()
        print ("\n \n Libvirt XML config for each NIC, "
               "i.e. for each libvirt network bridge:")
        for i in range(0, self.nics):
            print ("\n  Bridge/NIC number %02s" % (i+1))
            for j in range(0, self.vm_qtt):
                self.vms[j].showVmDhcpXmlOneItf(i)
        print ("\n \n End of Libvirt XML config for each NIC, "
               "i.e. for each libvirt network bridge:")
        print ("#######################################"
               "########################################")







def main():
    parser = argparse.ArgumentParser(description="Generate a list of random "
                        "and unique MAC addresses for all your "
                        "VMs.\nThe MAC addresses are derived from "
                        "a given prefix XX:XX:XX (the \nfirst 3 "
                        "bytes) pattern."
                        " \n \n"
                        "This is useful when you want to create "
                        "VMs with a libvirt/KVM tool \nsuch as " 
                        "`virt-install` and set `static` MAC "
                        "addresses to configure \na DHCP server "
                        "for these VMs.\n \n"
                        "Run this script:\n"
                        "  $ ./generate_mac.py\n"
                        "  $ ./generate_mac.py -p aa:bb:cc -n 3 -i 4\n \n"
                        "Get help:\n"
                        "  $ ./generate_mac.py -h\n",
                        formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument("-p","--prefix",
                        help="Choose MAC address prefix (3 bytes) patern.\n"
                        "Format is xx:xx:xx where x is hex value (0 to f).\n"
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
    # vm1 = Vm("maVM1", args.interface)
    # vm1.showVm()
    # vm1.addMac("OSEF")
    # vm1.addMac("OSEF")
    # vm1.showVm()
    # vm1.showVmDhcpXmlOneItf(0)
    
    list1 = Maclist(args.number, args.interface, args.prefix)
    list1.buildMacList()
    list1.populateVm()
    list1.displayAllMacPerVm()
    list1.displayAllXmlMacPerVM()
    list1.displayAllMacPerItf()
    list1.displayAllXmlMacPerItf()

if __name__=="__main__":
    main()
