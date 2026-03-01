import getpass
import sys
import telnetlib
import os
import xlrd
import xlwt 
from xlutils.copy import copy
import netmiko
from netmiko import ConnectHandler
import ast
import re
import xlrd
import xlwt 

# These codes can be used to push other commands as well. Simply replace the command.

def check_ping(str):
    hostname = str
    response = os.system("ping -n 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Active"
		
    else:
        pingstatus = "Ping failed"

    return pingstatus

rb = xlrd.open_workbook("device.xls")
r_sheet = rb.sheet_by_index(0)
wb = copy(rb) 
sheet = wb.get_sheet(0) 
i=1

while  i<3:

 try:
    #value=sheet.cell(1, 3).value
        value=r_sheet.cell(i, 0).value
        print(value)
        HOST = value
        status=check_ping(HOST)
        if (status == "Active") : 
            cisco_881 = { 'device_type': 'cisco_ios', 'ip': '10.148.232.84', 'username': 'XXXXXX','password': 'XXXXXXX','secret':'password'}  
            ##opening IP file
            cisco_881['username'] = input("Enter Username")
            cisco_881['password'] = getpass("Enter Password")
            cisco_881['secret'] = getpass("Enter Enable Secret")
            cisco_881['ip']= HOST
            print("Logining in to device :"+cisco_881['ip'])
            net_connect = ConnectHandler(**cisco_881)
            net_connect.send_command("terminal length 0")
            net_connect.enable()
            print(net_connect.find_prompt())
            #output=net_connect.send_command("Clear counters\n")
            net_connect.send_command("config t")
            net_connect.send_command("snmp-server group SNMPV3RWGroup v3 priv context vlan")
            net_connect.send_command("snmp-server group SNMPV3RWGroup v3 priv context vlan- match prefix")
            net_connect.send_command("end")
            net_connect.send_command("Write")
            output=net_connect.send_command("show run | in snmp-server group SNMPV3RWGroup v3 priv")
            print(output)
            
            #wb.save('DataPortland_Port.xls')
            net_connect.disconnect()
            i+=1
 except:
        #sheet.write(i,3,'Device Unable to login')
        #wb.save('Data1.xls')
        pass
        i+=1
		
