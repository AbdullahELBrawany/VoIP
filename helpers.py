import socket
from contextlib import closing
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import dns.zone
import dns.ipv4
import dns.rdataset
import dns.rdtypes.IN.A
import dns.update

import os.path

def load_DNSZones(str_filename):
    """
    Loads the DNS Zones file and returns the Zone class object.
    :str_filename: Full path of the dns zones file.
    :return: Zone Class
    :rtype: zone Class
    """    
    try:
        zone = dns.zone.from_file(str_filename, os.path.basename(str_filename), relativize=False)
        return zone
    except Exception as e:
        print('load_DNSZones Error: ' + str(e) + ' - Line: ' + str(e.__traceback__.tb_lineno))
        raise    

def load_ARecords(obj_zone, str_hostname):
    """
    Loads/fetches a specific A Record entry from the zone file.
    :obj_zone: Zone class object already loaded.
    :str_hostname: Type A record name/DNS
    :return: Dataset with record data.
    :rtype: rdataset Class
    """    
    try:
        rdataset = obj_zone.find_rdataset(str_hostname, dns.rdatatype.A, create=True)
        return rdataset
    except Exception as e:
        print('load_ARecords Error: ' + str(e) + ' - Line: ' + str(e.__traceback__.tb_lineno))
        raise    

def add_ARecords(obj_rdataset, str_ipaddr, int_TTL):
    """
    Adds a specific record of type A to the Zones file, the record will be the same as the one loaded/searched for in load_ARecords().
    :obj_rdataset: rdataset object returned from load_ARecords() function.
    :str_ipaddr: Destination host IP (A).
    :int_TTL: DNS TLS
    :return: None.
    """        
    try:
        rdata = dns.rdtypes.IN.A.A(dns.rdataclass.IN, dns.rdatatype.A, str_ipaddr)
        obj_rdataset.add(rdata, int_TTL)
        #zone.to_file('devops-db.info', relativize=False, want_comments=True)
    except Exception as e:
        print('add_ARecords Error: ' + str(e) + ' - Line: ' + str(e.__traceback__.tb_lineno))
        raise    

def remove_ARecords(obj_zone, str_hostname):
    """
    Deletes a specific type A record.
    :obj_zone: Zone class object already loaded.
    :str_hostname: Type A record name/DNS
    :return: None.
    """            
    try:
        rdataset_remove = obj_zone.delete_rdataset(str_hostname, dns.rdatatype.A)
        #zone.to_file('devops-db.info', relativize=False, want_comments=True)
        return rdataset_remove
    except Exception as e:
        print('remove_ARecords Error: ' + str(e) + ' - Line: ' + str(e.__traceback__.tb_lineno))
        raise    

def write_DNSZones(obj_zone):
    """
    DNS changes persist in the Zones configuration file loaded in the load_DNSZones() function.
    :obj_zone: Zone class object already loaded.
    :return: None.
    """            
    try:
        obj_zone.to_file('devops-db.info', relativize=False, want_comments=True)
    except Exception as e:
        print('write_DNSZones Error: ' + str(e) + ' - Line: ' + str(e.__traceback__.tb_lineno))
        raise    

def get_ARecords(obj_zone):
    """
    Returns the list of type A DNS records from the loaded zone file.
    :obj_zone: Zone class object already loaded.
    :return: List of Type A Records.
    :rtype: List of Dictionaries.
    """            
    try:
        lst_ARecords = []
        for a_records in obj_zone.iterate_rdatas('A'):
            dict_ARecord = {'domain': a_records[0].parent().to_text(), 'dns': a_records[0].relativize(a_records[0].parent()).to_text(), 
                            'ttl': str(a_records[1]), 'A': a_records[2].to_text()}
            lst_ARecords.append(dict_ARecord)
        return lst_ARecords
    except Exception as e:
        print('get_ARecords Error: ' + str(e) + ' - Line: ' + str(e.__traceback__.tb_lineno))
        raise    

def ping(host):
    """
    Returns host if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = 'ping '+str(param)+' 1 '+str(host)
    output = os.popen(command).read().lower()
    return (True, host) if not "unreachable" in output and not "100% packet loss" in output else (False, None)

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP