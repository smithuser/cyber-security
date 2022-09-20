
def get_mac(mac):
    import re
  
    # joins elements of getnode() after each 2 digits.
    # using regex expression
    print ("The MAC address in formatted and less complex way is : ", end="")
    mac = ':'.join(re.findall('..', '%012x' % mac))
    print (mac)

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

get_mac(4035300005499567)