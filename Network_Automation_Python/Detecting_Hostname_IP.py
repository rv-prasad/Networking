import getpass
import sys
import telnetlib
import os
import xlrd
import xlwt 
from xlutils.copy import copy
import netmiko
from netmiko import ConnectHandler

#We had received a excel file with list of Vulnerable_IPs (Vulnerable_IPs.xls) where only IPs and few hostnames were given.
#We needed to identify the each hostname and Model of device in order to plan the upgrade. This required login to each IPs as there were multiple SVI,L3 IPs.
# Once the output was got, we furhter worked in Pivot Table to sort the list to make this easy and final list to upgrade. Sheet of OutputSheet contains the same.

def check_ping(str):
    hostname = str
    response = os.system("ping -n 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Active"
		
    else:
        pingstatus = "Ping failed"

    return pingstatus

rb = xlrd.open_workbook("Vulnerable_IPs.xls")
r_sheet = rb.sheet_by_index(0)
wb = copy(rb) 
sheet = wb.get_sheet(0) 
i=1
while  i<3:
 try:

        value=r_sheet.cell(i, 0).value
        print(value)
        HOST = value
        status=check_ping(HOST)
        if (status == "Active") : 
            cisco_881 = { 'device_type': 'cisco_ios', 'ip': 'x.x.x.x', 'username': 'XXXXXX','password': 'XXXXXXX','secret':'password'}  
            ##opening IP file
            cisco_881['username'] = 'LAN_ID'
            cisco_881['password'] = 'LAN_Password'
            cisco_881['secret'] = 'xxxxxx'
            cisco_881['ip']= HOST
            print("Logining in to device :"+cisco_881['ip'])
            net_connect = ConnectHandler(**cisco_881)
            hostn1 = net_connect.find_prompt()
            hostn=hostn1.replace('>','')
            print(hostn)
            net_connect.send_command("terminal length 0")
            config = net_connect.send_command("show ver | in Software")
            print(config)
            Mode = net_connect.send_command("show inventory | in PID")
            Model= Mode.split()
            print(Model[1])  
            value2=config
            sheet.write(i,1,hostn)
            sheet.write(i,2,Model[1])
            sheet.write(i,3,value2)
            wb.save('OutputSheet.xls')
            net_connect.disconnect()
            i+=1
 except:
        sheet.write(i,3,'Device Unable to login')
        wb.save('OutputSheet.xls')
        pass
        i+=1
		
