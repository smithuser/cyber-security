# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 09:58:31 2022

@author:
"""
import sys
import scapy.all as scapy
import scapy.config as sConf

def get_interface():
    try:
        iface = sys.argv[1]
    except IndexError:
        iface = sConf.conf.iface  
        
    return iface

# A function to sniff packets from an interface
def sniff_packets(interface):
    scapy.sniff(filter= "arp", iface=interface, prn=analyze_packet, store=False)

 
def analyze_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        
        try:
            actual_mac = get_MAC(packet[scapy.ARP].psrc)
            packet_mac =packet[scapy.ARP].hwsrc
        
            if actual_mac != packet_mac:
                format_mac(packet_mac)
                print("[-] You are under ARP Spoof Attack!")
                
        except IndexError:
            pass
        
def get_MAC(target_IP):
    arp_request = scapy.ARP(pdst=target_IP) #instantiates an object of class ARP (ARP packet)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_arp_request = broadcast/arp_request
    answered_list=scapy.srp(broadcast_arp_request, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def format_mac(mac):
    import re
  
    # joins elements of getnode() after each 2 digits.
    # using regex expression
    # print ("The MAC address in formatted and less complex way is : ", end="")
    mac = ':'.join(re.findall('..', '%012x' % mac))
    # print (mac)

    add_to_iptables(mac)
    log_address(mac)

def log_address(formatted_mac):
    import psycopg2

    new_mac = formatted_mac.split(':')
    db_mac = '_'.join(new_mac)

    con = psycopg2.connect(
        host = 'localhost',
        database = 'airportmgt',
        user = 'postgres',
        password = 'postgres'
    )

    # cursor
    cur = con.cursor()

    cur.execute("insert into airportmgt_bannedmac (address) values (%s)", (db_mac,))

    con.commit()

    # close the cursor
    cur.close()

    # close the connection
    con.close()


def add_to_iptables(mac):
    import subprocess
    subprocess_str = "/usr/sbin/iptables -A INPUT -m mac --mac-source " + mac +" -j DROP"
    subprocess.run([subprocess_str], shell=True)

    print("%s has been added to the iptables: " % mac)


iface = get_interface()
sniff_packets(iface)
