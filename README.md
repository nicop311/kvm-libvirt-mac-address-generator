# kvm-libvirt-mac-address-generator
Python script that creates random MAC addresses for libvirt/qemu/KVM  VMs to facilitate the use of static DHCP entries.

## Usage

### Run this script:
```bash
   $ ./generate_mac.py
   $ ./generate_mac.py -p aa:bb:cc -n 3 -i 4
```

### Get help:
```bash
   $ ./generate_mac.py -h

```

## Why this script ?

1. Imagine you want to create a VM in libvirt/qemu/KVM.
2. And you want to use custom network bridges.
3. And for some reason, you want to set static DHCP entries
so that your VMs get static IP addresses with DHCP.

To set static DHCP entries, you need to know MAC addresses.

You have already configured and started your custom KVM network bridges.

But in KVM and when using tools such as `virt-install` to create
your VMs, MAC addresses are generated when you start the `virt-install`
script. And at the same time, your VMs are linked to your KVM network bridges.

Because you already have configured your network bridges, you must 
first find the MAC addresses of your VM. Then you modify your bridges.
This is not the easy way.


But there is a way to choose the MAC addresses of your VMs.

```bash
virt-install \
    [...]
    --network NETWORK,mac=12:34:56:78:9A:BC"
    [...]
```

Now you can use the script to create a list of unique MAC addresses
for your VMs and you can customize your DHCP and network bridge setup
with static entries.

Below is an example of KVM network bridges XML descriptor:
you can put your MAC addresses in here. Then you create your VMs.

```bash
<ip address="192.168.122.1" netmask="255.255.255.0" localPtr="yes">
  <dhcp>
    <range start="192.168.122.100" end="192.168.122.254"/>
    <host mac="00:16:3e:77:e2:ed" name="foo.example.com" ip="192.168.122.10"/>
    <host mac="00:16:3e:3e:a9:1a" name="bar.example.com" ip="192.168.122.11"/>
  </dhcp>
</ip>
```

Source: https://libvirt.org/formatnetwork.html
