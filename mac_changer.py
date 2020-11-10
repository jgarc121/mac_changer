#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface,", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify an new_mac, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    pattern = b"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w"
    mac_address_search_result = re.search(pattern, ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0).decode("utf-8")
    else:
        print("[-] Could not read MAC address")


def check_mac_changed(pre_mac, post_mac):
    if pre_mac == post_mac:
        return True
    else:
        return False


options = get_arguments()

current_mac = current_mac_address(options.interface)
print("Current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac = current_mac_address(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")


