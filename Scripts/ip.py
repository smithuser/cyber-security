
def add_to_iptables(mac):
    import subprocess
    subprocess_str = "/usr/sbin/iptables -A INPUT -m mac --mac-source " + mac +" -j REJECT"
    subprocess.run([subprocess_str], shell=True)