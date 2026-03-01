import pandas as pd
from netmiko import ConnectHandler
import re
import getpass
import subprocess
import platform

input_excel_file = 'devices.xlsx'
output_excel_file = 'devices_output2.xlsx'

route_command = 'show ip route vrf INET-PUBLIC connected'
description_template = 'show interface {} description'
media_type_template = 'show int {} | in media type'

def ping_host(hostname, count=2, timeout=2):
    """
    Ping the host and return True if reachable, False if not.
    Works across Windows and Unix-like systems.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Windows uses -w for timeout (in ms), Linux uses -W (in seconds)
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    command = ['ping', param, str(count), timeout_param, str(timeout), hostname]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

def extract_info_from_line(line):
    """Extract IP/mask and interface from a route line."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})'
    ip_match = re.search(ip_pattern, line)
    ip_address = ip_match.group(1) if ip_match else "Not Found"
    interface = line.strip().split(',')[-1].strip() if ',' in line else "Not Found"
    return ip_address, interface

def extract_description(output):
    """Extract Description from interface description output."""
    lines = output.strip().splitlines()
    for line in lines[1:]:  # Skip header line
        parts = line.split()
        if len(parts) >= 4:
            return ' '.join(parts[3:])
    return "Not Found"

def extract_media_type(output):
    """Extract media type from output."""
    match = re.search(r'media type is (\w+)', output, re.IGNORECASE)
    return match.group(1) if match else "Not Found"

def main():
    try:
        df = pd.read_excel(input_excel_file)
        if 'hostname' not in df.columns:
            print(f"Error: Input file '{input_excel_file}' must have a 'hostname' column.")
            return
    except FileNotFoundError:
        print(f"Error: Input file '{input_excel_file}' not found.")
        return

    username = input("Enter SSH username: ")
    password = getpass.getpass("Enter SSH password: ")

    results = []

    for hostname in df['hostname']:
        print(f"Checking connectivity to {hostname}...")
        if not ping_host(hostname):
            print(f"Skipping {hostname}: Ping failed.")
            results.append({
                'Hostname': hostname,
                'Subnet': 'Unreachable',
                'Local': 'Unreachable',
                'Interface': 'Unreachable',
                'Description': 'Unreachable',
                'Media Type': 'Unreachable'
            })
            continue

        print(f"Connecting to {hostname}...")
        device_config = {
            'device_type': 'cisco_ios',
            'host': hostname,
            'username': username,
            'password': password,
        }

        subnet_ip = local_ip = interface = description = media_type = "Not Found"

        try:
            with ConnectHandler(**device_config) as net_connect:
                # Run route command
                route_output = net_connect.send_command(route_command)
                for line in route_output.splitlines():
                    clean_line = line.strip()
                    if clean_line.startswith('C') and '/' in clean_line:
                        subnet_ip, _ = extract_info_from_line(clean_line)
                    elif clean_line.startswith('L') and '/' in clean_line:
                        local_ip, interface = extract_info_from_line(clean_line)

                # If interface is found, fetch description & media type
                if interface != "Not Found":
                    desc_command = description_template.format(interface)
                    description_output = net_connect.send_command(desc_command)
                    description = extract_description(description_output)

                    media_command = media_type_template.format(interface)
                    media_output = net_connect.send_command(media_command)
                    media_type = extract_media_type(media_output)
                else:
                    print(f"No interface found for local route on {hostname}")

        except Exception as e:
            print(f"Error connecting to {hostname}: {e}")
            subnet_ip = local_ip = interface = description = media_type = "Error"

        results.append({
            'Hostname': hostname,
            'Subnet': subnet_ip,
            'Local': local_ip,
            'Interface': interface,
            'Description': description,
            'Media Type': media_type
        })

    pd.DataFrame(results).to_excel(output_excel_file, index=False)
    print(f"\nProcessing completed. Results saved to '{output_excel_file}'.")

if __name__ == "__main__":
    main()
