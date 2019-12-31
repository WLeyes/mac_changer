#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more information.")
    elif not options.new_mac:
        parser.error("[-] Please specify a MAC address, use --help for more information.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


# get interface and MAC address
options = get_arguments()

# get the current MAC of interface
current_mac = get_current_mac(options.interface)
print("Current MAC: " + str(current_mac))

# Change the current MAC address to new MAC address
change_mac(options.interface, options.new_mac)

# Check that the MAC address has been changed
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address has been successfully changed to " + current_mac)
else:
    print("[-] MAC address was not changed.")
