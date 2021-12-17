from netmiko import ConnectHandler
from netmiko import NetMikoAuthenticationException
from netmiko import NetMikoTimeoutException
import re
import netmiko

username = 'username'
password = 'password'  # getpass()
platform = 'arista_eos'

with open(r'\\path\to\hostlist\', 'r') as IPS:
    for line in IPS:
        try:
            IPS = line.strip()
            device = ConnectHandler(device_type=platform, ip=IPS, username=username, password=password)
            interfacelist = device.send_command("show int status")
            for i in range(1,53):
                output = device.send_command("show interface ethernet " +str(i))
                interface = 'Ethernet' , i
                print('Scanning Device: ' , IPS , 'Interface:' , interface)
                for line in output.split('\n'):
                    if 'notpresent' in line:
                        downtime = re.findall(r'Down \d+ \w+', output)[0]
                        daysdown = [int(daysdown) for daysdown in downtime.split() if daysdown.isdigit()]
                        for days in daysdown:
                            if days < 15:
                                print(days)
                            #    device.sendcommand('interface ethernet' +str(i))
                            #    device.sendcommand('switchport')
                            #    device.sendcommand('switchport access vlan 999')
                            #    device.sendcommand('no description')
                            #    device.sendcommand('shutdown')
                            else:
                                print('The interface: ', interface , 'has not been down for less than 15 days, Total days down:' , days , 'doing nothing')
        except NetMikoAuthenticationException:
            print('Authentication error: Failed to connect to {}'.format(IPS))
